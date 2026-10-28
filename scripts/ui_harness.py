#!/usr/bin/env python3
"""Inspect and select SVG drafts, with an optional HTML comparison gallery."""

import argparse
import base64
from datetime import datetime, timezone
import hashlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import math
import os
from pathlib import Path
import re
import secrets
import sys
import tempfile
import xml.etree.ElementTree as ET


TEMPLATE = Path(__file__).resolve().parents[1] / "assets" / "ui-selection.html"
SVG_NS = "{http://www.w3.org/2000/svg}"


def read_json(path):
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def required_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be non-empty text")
    return value.strip()


def validate_svg(raw, path):
    text = raw.decode("utf-8")
    if re.search(r"<!\s*(DOCTYPE|ENTITY)\b", text, re.I):
        raise ValueError(f"{path}: XML entities and doctypes are unsupported")
    root = ET.fromstring(raw)
    if root.tag != SVG_NS + "svg":
        raise ValueError(f"{path}: expected an SVG root with its namespace")
    box = [float(part) for part in re.split(r"[\s,]+", root.get("viewBox", "").strip()) if part]
    if len(box) != 4 or not all(math.isfinite(n) for n in box) or min(box[2:]) <= 0:
        raise ValueError(f"{path}: expected a positive viewBox")
    for tag in ("title", "desc"):
        node = root.find(SVG_NS + tag)
        if node is None or not "".join(node.itertext()).strip():
            raise ValueError(f"{path}: missing {tag}")
    for node in root.iter():
        tag = node.tag.rsplit("}", 1)[-1]
        if tag in {"script", "foreignObject"}:
            raise ValueError(f"{path}: scripts and embedded HTML are unsupported")
        for attr, value in node.attrib.items():
            attr = attr.rsplit("}", 1)[-1]
            if attr.lower().startswith("on"):
                raise ValueError(f"{path}: event handlers are unsupported")
            if attr in {"href", "src", "base"} and not value.startswith("#"):
                raise ValueError(f"{path}: references must be local SVG fragments")
        css = " ".join(node.attrib.values())
        if tag == "style":
            css += " " + "".join(node.itertext())
        if "@import" in css.lower() or any(
            not ref.strip(" \t\r\n\"'").startswith("#")
            for ref in re.findall(r"url\s*\((.*?)\)", css, re.I | re.S)
        ):
            raise ValueError(f"{path}: external CSS resources are unsupported")


def load_gallery(manifest):
    manifest = Path(manifest).resolve()
    data = read_json(manifest)
    if not isinstance(data, dict):
        raise ValueError("manifest must be a JSON object")
    title = required_text(data.get("title"), "title")
    options = data.get("options")
    if not isinstance(options, list) or not options:
        raise ValueError("provide at least one option")
    if any(not isinstance(option, dict) for option in options):
        raise ValueError("each option must be an object")
    ids = [option.get("id") for option in options]
    if any(type(value) is not int or value < 1 for value in ids) or len(set(ids)) != len(ids):
        raise ValueError("option IDs must be unique positive integers")
    gallery = {"title": title, "options": []}
    seen = set()
    for option in sorted(options, key=lambda item: item["id"]):
        relative = required_text(option.get("svg"), "svg")
        path = (manifest.parent / relative).resolve()
        if Path(relative).is_absolute() or not path.is_relative_to(manifest.parent):
            raise ValueError("SVG paths must stay within the manifest directory")
        if path.suffix.lower() != ".svg":
            raise ValueError(f"{relative}: expected an .svg file")
        raw = path.read_bytes()
        validate_svg(raw, relative)
        digest = hashlib.sha256(raw).hexdigest()
        if digest in seen:
            raise ValueError("all SVG drafts must have different content")
        seen.add(digest)
        gallery["options"].append({
            "id": option["id"],
            "name": required_text(option.get("name"), "name"),
            "description": required_text(option.get("description"), "description"),
            "svg": path.relative_to(manifest.parent).as_posix(),
            "image": "data:image/svg+xml;base64," + base64.b64encode(raw).decode("ascii"),
        })
    # Include raw manifest metadata too: a changed comparison needs a fresh choice.
    canonical = json.dumps({"manifest": data, "gallery": gallery}, sort_keys=True, ensure_ascii=False)
    gallery["fingerprint"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return gallery


def validate_choice(gallery, choice):
    if not isinstance(choice, dict) or choice.get("fingerprint") != gallery["fingerprint"]:
        raise ValueError("comparison changed; present the current drafts and choose again")
    selected_id = choice.get("selected_id")
    if type(selected_id) is int:
        for option in gallery["options"]:
            if option["id"] == selected_id:
                return option
    available = ", ".join(str(option["id"]) for option in gallery["options"])
    raise ValueError(f"selected_id must match a current option ID: {available}")


def selection_state(manifest, gallery):
    path = Path(manifest).resolve().with_name("selection.json")
    if not path.exists():
        return {"state": "pending"}
    try:
        choice = read_json(path)
        option = validate_choice(gallery, choice)
        if choice.get("svg") != option["svg"] or choice.get("selected_name") != option["name"]:
            raise ValueError("saved option metadata does not match the comparison")
    except (ValueError, TypeError) as exc:
        return {"state": "stale", "message": str(exc)}
    return {"state": "selected", "selection": choice}


def save_choice(manifest, gallery, choice):
    option = validate_choice(gallery, choice)
    selection = {
        "schema_version": 1,
        "fingerprint": gallery["fingerprint"],
        "selected_id": option["id"],
        "selected_name": option["name"],
        "svg": option["svg"],
        "selected_at": datetime.now(timezone.utc).isoformat(),
    }
    path = Path(manifest).resolve().with_name("selection.json")
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False) as handle:
            temp_path = Path(handle.name)
            json.dump(selection, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temp_path, path)
    finally:
        if temp_path and temp_path.exists():
            temp_path.unlink()
    return {"state": "selected", "selection": selection}


def render_gallery(manifest, gallery, token=None):
    payload = {
        **gallery,
        "saved": selection_state(manifest, gallery),
        "token": token,
    }
    # The JSON lives in a script element; never allow manifest text to close it.
    encoded = json.dumps(payload, ensure_ascii=False).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    template = TEMPLATE.read_text(encoding="utf-8").replace("__OPTION_COUNT__", str(len(gallery["options"])))
    return template.replace("/*__GALLERY_DATA__*/", encoded)


def create_server(manifest, port=0):
    manifest = Path(manifest).resolve()
    load_gallery(manifest)
    token = secrets.token_urlsafe(32)

    class Handler(BaseHTTPRequestHandler):
        def respond(self, status, data, content_type="application/json; charset=utf-8"):
            body = data.encode("utf-8") if isinstance(data, str) else json.dumps(data, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            try:
                if self.path == "/":
                    self.respond(200, render_gallery(manifest, load_gallery(manifest), token), "text/html; charset=utf-8")
                elif self.path == "/selection":
                    self.respond(200, selection_state(manifest, load_gallery(manifest)))
                else:
                    self.respond(404, {"error": "not found"})
            except (OSError, ValueError, ET.ParseError) as exc:
                self.respond(400, {"error": str(exc)})

        def do_POST(self):
            if self.path != "/select":
                self.respond(404, {"error": "not found"})
                return
            origin = self.headers.get("Origin")
            expected = f"http://127.0.0.1:{self.server.server_port}"
            if self.headers.get("X-Selection-Token") != token or (origin and origin != expected):
                self.respond(403, {"error": "open the local gallery to make a selection"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if not 0 < length <= 8192:
                    raise ValueError("invalid selection request size")
                choice = json.loads(self.rfile.read(length))
                result = save_choice(manifest, load_gallery(manifest), choice)
                self.respond(200, result)
            except (OSError, ValueError, ET.ParseError) as exc:
                self.respond(409, {"error": str(exc)})

        def log_message(self, *_args):
            pass

    return ThreadingHTTPServer(("127.0.0.1", port), Handler)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("inspect", "build", "serve", "choose", "import", "status"):
        command = commands.add_parser(name)
        command.add_argument("manifest", type=Path)
        if name == "serve":
            command.add_argument("--port", type=int, default=0)
        elif name == "choose":
            command.add_argument("id", type=int)
        elif name == "import":
            command.add_argument("selection", type=Path)
    args = parser.parse_args(argv)
    try:
        gallery = load_gallery(args.manifest)
        if args.command == "inspect":
            result = {key: gallery[key] for key in ("title", "fingerprint")}
            result["options"] = [
                {key: value for key, value in option.items() if key != "image"}
                for option in gallery["options"]
            ]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        elif args.command == "build":
            output = args.manifest.resolve().with_name("compare.html")
            output.write_text(render_gallery(args.manifest, gallery), encoding="utf-8")
            print(output)
        elif args.command == "serve":
            with create_server(args.manifest, args.port) as server:
                print(f"http://127.0.0.1:{server.server_port}/", flush=True)
                server.serve_forever()
        elif args.command == "choose":
            print(json.dumps(save_choice(args.manifest, gallery, {
                "fingerprint": gallery["fingerprint"], "selected_id": args.id,
            }), ensure_ascii=False))
        elif args.command == "import":
            print(json.dumps(save_choice(args.manifest, gallery, read_json(args.selection)), ensure_ascii=False))
        else:
            result = selection_state(args.manifest, gallery)
            print(json.dumps(result, ensure_ascii=False))
            return 0 if result["state"] == "selected" else 2
    except KeyboardInterrupt:
        return 0
    except (OSError, ValueError, ET.ParseError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
