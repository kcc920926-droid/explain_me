import contextlib
import http.client
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import threading
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ui_harness", ROOT / "scripts" / "ui_harness.py")
harness = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(harness)


class SelectionHarnessTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.manifest = self.directory / "manifest.json"
        self.data = {"title": "테스트 architecture", "options": []}
        self.set_options(range(1, 7))

    def set_options(self, ids):
        self.data["options"] = []
        for number in ids:
            filename = f"{number:02}.svg"
            (self.directory / filename).write_text(
                f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 736 440">'
                f'<title>Draft {number}</title><desc>A test architecture map.</desc>'
                f'<rect width="736" height="440" fill="#fff"/>'
                f'<text x="40" y="80" font-size="28">Layout {number}</text></svg>',
                encoding="utf-8",
            )
            self.data["options"].append({
                "id": number, "name": f"시안 {number}",
                "description": f"구성 {number}", "svg": filename,
            })
        self.write_manifest()

    def write_manifest(self):
        self.manifest.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")

    def run_cli(self, *args):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = harness.main(list(args))
        return code, stdout.getvalue(), stderr.getvalue()

    def test_portable_gallery_embeds_options_and_escapes_manifest_text(self):
        self.data["title"] = '</script><script>alert("title")</script> __OPTION_COUNT__'
        self.write_manifest()
        code, output, error = self.run_cli("build", str(self.manifest))
        self.assertEqual((code, error), (0, ""))
        html = Path(output.strip()).read_text(encoding="utf-8")
        payload = re.search(r'<script id="gallery-data" type="application/json">(.*?)</script>', html, re.S)[1]
        data = json.loads(payload)
        self.assertEqual(data["title"], self.data["title"])
        self.assertEqual(len(data["options"]), len(self.data["options"]))
        self.assertTrue(all(option["image"].startswith("data:image/svg+xml;base64,") for option in data["options"]))
        self.assertNotIn("<script>", payload)
        self.assertIsNone(data["token"])
        self.assertEqual(data["saved"]["state"], "pending")

    def test_variable_counts_and_sparse_ids_can_build_choose_and_resume(self):
        cases = [list(range(1, count + 1)) for count in (1, 3, 6, 8, 12)]
        cases.append([19, 2, 7])
        for ids in cases:
            with self.subTest(ids=ids):
                self.set_options(ids)
                code, output, error = self.run_cli("build", str(self.manifest))
                self.assertEqual((code, error), (0, ""))
                html = Path(output.strip()).read_text(encoding="utf-8")
                payload = json.loads(re.search(r'<script id="gallery-data" type="application/json">(.*?)</script>', html, re.S)[1])
                self.assertEqual([option["id"] for option in payload["options"]], sorted(ids))
                self.assertIn(f'aria-label="UI 시안 {len(ids)}개"', html)
                self.assertIn(f"같은 분석, {len(ids)}가지 표현.", html)
                selected_id = max(ids)
                self.assertEqual(self.run_cli("choose", str(self.manifest), str(selected_id))[0], 0)
                code, output, _ = self.run_cli("status", str(self.manifest))
                self.assertEqual(code, 0)
                selection = json.loads(output)["selection"]
                self.assertEqual((selection["selected_id"], selection["svg"]),
                                 (selected_id, f"{selected_id:02}.svg"))
                # Membership, rather than a hard-coded numeric range, controls choices.
                self.assertEqual(self.run_cli("choose", str(self.manifest), str(selected_id + 1))[0], 1)

    def test_native_inspect_choose_and_resume_need_no_html_template(self):
        self.set_options([2, 7, 19])
        with patch.object(harness, "TEMPLATE", self.directory / "no-template.html"):
            code, output, error = self.run_cli("inspect", str(self.manifest))
            self.assertEqual((code, error), (0, ""))
            data = json.loads(output)
            self.assertEqual(data["title"], self.data["title"])
            self.assertEqual([option["id"] for option in data["options"]], [2, 7, 19])
            self.assertEqual(data["options"][-1]["svg"], "19.svg")
            self.assertTrue(data["fingerprint"])
            self.assertNotIn("data:image/", output)
            self.assertFalse((self.directory / "compare.html").exists())
            self.assertFalse((self.directory / "selection.json").exists())
            self.assertEqual(self.run_cli("choose", str(self.manifest), "19")[0], 0)
            code, output, _ = self.run_cli("status", str(self.manifest))
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(output)["selection"]["selected_id"], 19)

    def test_rejects_missing_duplicate_and_noninteger_options(self):
        originals = self.data["options"][:]
        invalid = [[], None, "not a list", [None], originals + [originals[0]]]
        invalid.extend([{**originals[0], "id": value}] + originals[1:]
                       for value in (True, 0, -1, "1", 1.5))
        for options in invalid:
            with self.subTest(options=options):
                self.data["options"] = options
                self.write_manifest()
                with self.assertRaises(ValueError):
                    harness.load_gallery(self.manifest)
        self.data["options"] = originals
        self.write_manifest()
        (self.directory / "02.svg").write_bytes((self.directory / "01.svg").read_bytes())
        with self.assertRaisesRegex(ValueError, "different content"):
            harness.load_gallery(self.manifest)

    def test_svg_must_be_portable_and_accessible(self):
        path = self.directory / "01.svg"
        original = path.read_text(encoding="utf-8")
        invalid = (
            original.replace('viewBox="0 0 736 440"', 'viewBox="0 0 0 440"'),
            original.replace("<title>Draft 1</title>", ""),
            original.replace("</svg>", '<image href="https://example.com/image.png"/></svg>'),
            original.replace("</svg>", '<style>rect{fill:url(https://example.com/x)}</style></svg>'),
            original.replace("</svg>", '<script>alert(1)</script></svg>'),
            '<!DOCTYPE svg [<!ENTITY x "hello">]>' + original,
        )
        for svg in invalid:
            with self.subTest(svg=svg):
                path.write_text(svg, encoding="utf-8")
                with self.assertRaises(ValueError):
                    harness.load_gallery(self.manifest)

    def test_svg_path_cannot_escape_output_directory(self):
        for path in ("../outside.svg", str(self.directory / "01.svg")):
            with self.subTest(path=path):
                self.data["options"][0]["svg"] = path
                self.write_manifest()
                with self.assertRaisesRegex(ValueError, "within"):
                    harness.load_gallery(self.manifest)

    def test_selection_resumes_and_any_changed_draft_invalidates_it(self):
        self.assertEqual(self.run_cli("status", str(self.manifest))[0], 2)
        self.assertEqual(self.run_cli("choose", str(self.manifest), "3")[0], 0)
        code, output, _ = self.run_cli("status", str(self.manifest))
        self.assertEqual(code, 0)
        selection = json.loads(output)["selection"]
        self.assertEqual((selection["selected_id"], selection["svg"]), (3, "03.svg"))
        self.assertTrue(selection["selected_at"])
        # Even changing an unselected draft must not reuse a stale approval.
        path = self.directory / "06.svg"
        path.write_text(path.read_text(encoding="utf-8").replace("Layout 6", "New layout"), encoding="utf-8")
        code, output, _ = self.run_cli("status", str(self.manifest))
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output)["state"], "stale")

    def test_changing_option_count_requires_a_new_choice(self):
        self.assertEqual(self.run_cli("choose", str(self.manifest), "3")[0], 0)
        self.data["options"] = self.data["options"][:3]
        self.write_manifest()
        code, output, _ = self.run_cli("status", str(self.manifest))
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(output)["state"], "stale")
        self.assertEqual(self.run_cli("choose", str(self.manifest), "2")[0], 0)
        self.assertEqual(self.run_cli("status", str(self.manifest))[0], 0)

    def test_downloaded_choice_import_and_invalid_import_preserves_choice(self):
        gallery = harness.load_gallery(self.manifest)
        download = self.directory / "download.json"
        download.write_text(json.dumps({"fingerprint": gallery["fingerprint"], "selected_id": 6}))
        self.assertEqual(self.run_cli("import", str(self.manifest), str(download))[0], 0)
        self.assertEqual(harness.selection_state(self.manifest, gallery)["selection"]["selected_id"], 6)
        for choice in ({"fingerprint": "old", "selected_id": 1},
                       {"fingerprint": gallery["fingerprint"], "selected_id": True}, [], None):
            with self.subTest(choice=choice):
                download.write_text(json.dumps(choice))
                self.assertEqual(self.run_cli("import", str(self.manifest), str(download))[0], 1)
                self.assertEqual(harness.selection_state(self.manifest, gallery)["selection"]["selected_id"], 6)

    def test_browser_can_save_and_reselect_but_stale_page_cannot_save(self):
        self.set_options([2, 7, 19])
        server = harness.create_server(self.manifest)
        worker = threading.Thread(target=server.serve_forever, daemon=True)
        worker.start()
        self.addCleanup(server.server_close)
        self.addCleanup(worker.join)
        self.addCleanup(server.shutdown)

        def request(method, route, payload=None, token=None):
            connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
            headers = {"Content-Type": "application/json"}
            if token:
                headers["X-Selection-Token"] = token
            connection.request(method, route, body=json.dumps(payload) if payload is not None else None, headers=headers)
            response = connection.getresponse()
            result = response.status, response.read().decode("utf-8")
            connection.close()
            return result

        status, html = request("GET", "/")
        self.assertEqual(status, 200)
        payload = json.loads(re.search(r'<script id="gallery-data" type="application/json">(.*?)</script>', html, re.S)[1])
        choice = {"fingerprint": payload["fingerprint"], "selected_id": 7}
        self.assertEqual(request("POST", "/select", choice)[0], 403)
        self.assertFalse((self.directory / "selection.json").exists())
        self.assertEqual(request("POST", "/select", choice, payload["token"])[0], 200)
        self.assertEqual(json.loads(request("GET", "/selection")[1])["selection"]["selected_id"], 7)
        choice["selected_id"] = 19
        self.assertEqual(request("POST", "/select", choice, payload["token"])[0], 200)
        self.data["title"] = "Revised comparison"
        self.write_manifest()
        self.assertEqual(request("POST", "/select", choice, payload["token"])[0], 409)
        self.assertEqual(json.loads(request("GET", "/selection")[1])["state"], "stale")


if __name__ == "__main__":
    unittest.main()
