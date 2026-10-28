# UI draft selection harness

Use this after gathering evidence for a substantive visual explanation and before
finishing the explainer. Honor text-only requests and supplied final designs;
simple factual answers do not need a UI comparison.
Run the bundled script from the installed skill directory; write generated files
to the target project's authorized output directory, not into the skill package.
The shared validation and selection commands need only Python 3.9+, with no
package installation. A browser is needed only if the user selects the HTML
gallery and an in-host HTML preview is unavailable.

The shared contract is SVG drafts + `manifest.json` + `selection.json`. Presentation
adapts to the current host; neither a browser nor a vendor-specific question tool
is part of the contract. The user selects the presentation method; neither method
is an automatic default. A local server is optional even for HTML review.

## Let the user choose the presentation method

Before generating or presenting the drafts, reuse a method already specified in
the task. Otherwise ask one single-choice question using a native picker when
available in the current session and mode:

**시안을 어떤 방식으로 비교할까요?**

| Choice | Label | Description |
| --- | --- | --- |
| 1 | 호스트 내부에서 보기 | 현재 앱의 이미지·미리보기로 살펴보고 대화에서 선택합니다. |
| 2 | HTML 갤러리로 보기 | 비교 갤러리에서 시안을 확대하고 선택합니다. |

If a picker is unavailable, show these choices in ordinary conversation and
accept a numbered reply. Do not make up a vendor-specific tool or change modes
just to show a picker. Do not silently choose a method because it is convenient
or describe either choice as mandatory. Preserve the user's choice in task
context and reuse it when resuming; ask again only if they want to change it or
the chosen method is no longer available.

Check actual display capabilities before offering the choices. Explain known
limitations alongside a choice, or mark it unavailable if the picker supports
that. If the requested method cannot work, let the user choose another method or
review the generated files. Do not switch automatically. The presentation choice
and the later design choice are separate: choosing HTML or in-host review does
not select a draft.

## Prepare meaningful alternatives

Choose the count from the user's request and the useful design directions.
Around six is a starting reference when unspecified, not a quota or limit. Fewer
strong alternatives are better than padded duplicates; add more when they serve
a real comparison. If the user already specifies one design, follow that direction
as described in `SKILL.md` instead of forcing a comparison.

Keep the same central answer, evidence, relationships, examples, and uncertainty
across drafts. If an analogy helps, preserve its meaning across the alternatives.
Include enough subject-appropriate detail for the user to assess the design.
Strengths, risks, and next moves belong only where the topic calls for them. Do
not substitute text descriptions, placeholder diagrams, or color variants of the
same composition.

Possible directions (examples to draw from, not a required set):

| ID | Direction | Distinguishing composition |
| --- | --- | --- |
| 1 | Layered overview | Main parts and their relationships in stacked bands |
| 2 | Chronological journey | A dominant sequence with context and supporting details |
| 3 | Relationship map | A central concept with surrounding parts and dependencies |
| 4 | Responsibility lanes | Lanes emphasize ownership and cross-boundary handoffs |
| 5 | Technical blueprint | A precise topology with direct labels and operational callouts |
| 6 | Editorial overview | A dominant diagram paired with examples, evidence, and limits |

Use stable, unique positive integer IDs. IDs need not be consecutive: keep existing
numbers when adding or removing drafts so chat references stay clear. The count
comes from the manifest's `options` list; any non-empty list is supported, without
a fixed maximum. Keep every draft self-contained and follow the SVG readability
and accessibility requirements in `SKILL.md`. Inspect every draft before presenting
them. The harness checks valid IDs, unique SVG content, XML, and portable assets;
it cannot judge whether the facts match or the layouts meaningfully differ.

Place `manifest.json` beside the SVGs, with this shape (this example contains three
options; replace the list, labels, and filenames with the actual drafts):

```json
{
  "title": "Visual explanation · UI 시안 선택",
  "options": [
    {"id": 1, "name": "Layered atlas", "description": "Layers emphasize the system boundary.", "svg": "01-layered.svg"},
    {"id": 2, "name": "Request journey", "description": "Follow a request through the system.", "svg": "02-journey.svg"},
    {"id": 3, "name": "System hub", "description": "Compare internal and external roles.", "svg": "03-hub.svg"}
  ]
}
```

SVG paths are relative to the manifest directory and must stay inside it.
Each SVG needs a positive `viewBox`, `title`, and `desc`. Scripts, embedded HTML,
external references, external CSS, and XML entities are unsupported.

## Choice 1: Present inside the host

Follow this route when the user selects in-host review.

```bash
python3 /path/to/skill/scripts/ui_harness.py inspect /path/to/output/manifest.json
```

This validates the manifest and SVGs and returns the title, fingerprint, and
numbered options as JSON, without creating HTML or changing the saved choice.
`inspect`, `choose`, and `status` do not depend on the HTML template or a server.

- Inspect the tools actually available in the current session and mode. Prefer
  in-conversation image output or a local preview pane. When the host cannot
  display SVG directly, render PNG previews from the same SVGs with an available
  renderer. Preserve SVG as the canonical source. A numbered overview image can
  help compare many drafts, with individual previews for readable details.
- Present the actual previews with their stable IDs, names, and brief differences.
  A model reading an image is not proof that the user was shown that image.
- If an available native question tool can represent all options, use it to
  collect a choice in the host. Tool names, mode requirements, and picker limits
  differ; do not require a particular vendor's tool or reduce the design count to
  fit its controls. A normal numbered chat reply is the portable input fallback.
- Record an explicit human reply, whether it came from chat or a native picker,
  with the same command:

```bash
python3 /path/to/skill/scripts/ui_harness.py choose /path/to/output/manifest.json 3
```

Use the actual IDs when asking, such as “1·2·3번 중 어떤 시안으로 진행할까요?”
for the example above. A picker default, idle timeout, automated hook response,
or missing headless input is not an explicit human choice. Keep the task pending
when no choice has arrived.

If the surface cannot display previews, explain that limitation and offer the
SVG/PNG files for inspection or let the user select the HTML route below.
If the user explicitly wants no browser, keep the file-and-conversation workflow;
do not open a webpage anyway or claim that textual descriptions are visual drafts.

## Choice 2: Present an HTML gallery

Follow this route when the user selects HTML review.
HTML offers a consistent comparison layout in browsers, but does not guarantee
embedded rendering or selection callbacks inside every agent host. It is one
presentation of the shared state, not a prerequisite for selection.

```bash
python3 /path/to/skill/scripts/ui_harness.py build /path/to/output/manifest.json
```

This writes `compare.html`, a self-contained gallery with a responsive card grid,
full-size previews, keyboard-accessible radio choices, and no preselection. Visible
counts and accessibility labels follow the actual number of options.
Use an in-host HTML preview when available, or a browser if appropriate, and
include a link in the handoff. A plain chat reply remains valid in this mode too.

For local hosts, run the optional browser selection server in a background
terminal session:

```bash
python3 /path/to/skill/scripts/ui_harness.py serve /path/to/output/manifest.json
```

It prints a loopback URL with an automatically assigned port. Open that URL on
the same computer. Clicking **이 시안으로 진행** writes `selection.json` next to
the manifest. Keep the session alive while awaiting the user; stop it when the
selection is collected or the task is canceled. Do not poll in a blocking loop.

The standalone HTML works without the server. Its confirmation button downloads
a selection JSON file and clearly states that it must be handed back. If the
user supplies that file, import it with:

```bash
python3 /path/to/skill/scripts/ui_harness.py import /path/to/output/manifest.json /path/to/downloaded/selection.json
```

If the user has not chosen, hand off the current previews and wait. Do not invent
a choice to keep the workflow running. If they ask for a combination, adapt one
draft to that direction and collect a choice on the updated comparison, unless
their instruction already clearly specifies the final design.

## Resume and finish

```bash
python3 /path/to/skill/scripts/ui_harness.py status /path/to/output/manifest.json
```

Only `state: "selected"` permits finalization. Exit code `0` means selected; `2`
means pending or stale; `1` means invalid input or another error. A selected
record includes the number, name, SVG path, and a fingerprint of the entire
comparison. Editing any draft or manifest content invalidates the old
choice. Re-present the updated options in the current presentation method before
collecting a new choice. A valid saved choice can be reused after a restart without
asking again. Recheck status before finalizing if the user may have changed their choice.

Create the final SVG separately from the frozen drafts, preserving the selected
layout. Complete its evidence and visual checks, then deliver the final SVG with
at most the short handoff allowed by `SKILL.md`.
