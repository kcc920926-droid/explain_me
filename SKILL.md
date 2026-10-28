---
name: explain-me
description: Explain concepts, events, processes, comparisons, documents, and technical systems with evidence-grounded visual explanations adapted to the reader. Use when the user asks to understand a topic, see how or why it works, follow what happened, or compare alternatives. Prefer a compact SVG overview for substantive explanations; honor requests for text or another format. Do not turn simple factual answers or implementation-only tasks into an explainer.
---

# explain_me

Make a subject understandable: what it is, how it works or unfolded, and why it
matters. Use a compact visual explanation by default, with SVG as the portable
source. A complex subject may need an overview plus focused detail; do not force
it onto one unreadable page.

## Frame the explanation

- Follow the user's language, audience, purpose, and requested format. Without
  an audience cue, assume an interested adult with little background knowledge.
- Use the supplied question, text, document, link, image, data, or repository as
  the starting point. Do not require a repository for a non-code topic.
- Identify the central question and the smallest scope that answers it. Ask only
  when ambiguity would materially change the explanation; otherwise state a
  brief working assumption and proceed.
- Define essential terms where they first become useful. Use a concrete example
  when it explains more than another abstract definition.

## Choose a structure that fits

Use these as starting points, not compulsory sections. Combine structures only
when the question needs them.

| Subject or question | Useful structure | Guard against |
| --- | --- | --- |
| Concept or mechanism | Definition, parts, relationships, worked example, limits | An analogy replacing the actual mechanism |
| Event or history | Context, dated sequence, participants, outcomes, unresolved questions | Treating sequence as proof of causation |
| Comparison or decision | Shared criteria, side-by-side differences, tradeoffs, conditions | A universal winner when goals differ |
| Process or procedure | Inputs, steps, branches, outputs, failure points | Omitting prerequisites or consequential branches |
| Document or argument | Main claim, supporting reasons, evidence, assumptions, implications | Presenting the author's claim as established fact |
| System or repository | Boundary, components, flows, ownership, operations, constraints | Showing intended architecture as deployed |

For codebases or deployed infrastructure, read
[references/repository-analysis.md](references/repository-analysis.md). Load it
only for that mode; its runtime categories are not a template for every topic.

## Establish evidence before drawing

Keep a lightweight internal mapping from important claims to their supporting
passage, file and line, dataset, calculation, or observation. Separate two things:

- **Claim status:** supported fact, attributed interpretation, explicit assumption,
  or unresolved/uncertain claim. An illustrative scenario is not factual evidence.
- **Provenance and time:** who or what supports the claim, the relevant version or
  period, and when an event or observation occurred. Source type alone does not
  establish truth; a document may support the fact that someone made a claim.

Use supplied material directly when explaining its contents. When establishing
real-world truth, prefer primary sources and corroborate consequential disputed
claims. Verify changing or recent information when currentness matters, and keep
event dates separate from publication dates. If sources or live access are
unavailable, explain the bounded material available and name what is unverified.
Do not imply that a search, experiment, or runtime inspection occurred when it did
not. A repository file or saved screenshot cannot establish current runtime state.

Show citations near contested, numerical, time-sensitive, quoted, or otherwise
hard-to-check claims, and whenever requested. Prefer a few readable source notes
or linked references to an evidence index covering every label. Do not invent
citations, observations, dates, or precision. For undated historical artifacts,
label the observation time unknown; do not substitute a commit or file timestamp.

## Review visual alternatives

For substantive visual explanations, read
[references/ui-selection.md](references/ui-selection.md) and use the selection
harness after establishing the evidence. Respect requests for text, a supplied
final design, or another format; simple factual answers do not need a UI review.

- Let the user choose how to review the drafts: **inside the current host** or
  **in an HTML gallery**. Use an available native single-choice question tool;
  otherwise present the two choices in conversation and accept a numbered reply.
  Honor a method already specified in the task without asking again. Neither
  method is an automatic default or a fallback imposed on the user. If the chosen
  method is unavailable, explain the limitation and let the user choose another.
- Create rendered SVG UI drafts from the same central answer, evidence,
  relationships, and uncertainty. Use around six as an initial reference when no
  count is requested; adapt the count to the user's request, subject complexity,
  and meaningful design directions. Do not pad the comparison to hit a quota.
  Vary hierarchy, layout, typography, and visual treatment; changing colors alone
  is insufficient. Keep the structure appropriate to the subject.
- Show the alternatives with stable numbers, short names, differences, and
  readable previews using the selected presentation method. For in-host review,
  use its image output, file preview, or available visual surface. For HTML review,
  build the portable gallery. Do not switch methods without the user's direction.
- Use a native choice tool only when it is available in the active mode and can
  represent the options. Otherwise accept a numbered conversational reply. Never
  truncate the alternatives to fit a picker. Respect an explicit no-browser request.
- Wait for the user's design choice before polishing or presenting a final SVG.
  A recommendation, highlighted card, elapsed time, or tool-generated selection
  is not the user's choice. Do not click selection controls on their behalf.
- Keep SVG drafts, `manifest.json`, and `selection.json` as shared state across
  presentation methods. `scripts/ui_harness.py inspect` validates and lists drafts
  without building HTML. Record an explicit chat or native-tool choice with the
  harness, or read the choice saved by its local browser UI. Resume only from a
  valid selection for the current drafts and preserve the chosen layout.
- If the user explicitly supplies a preferred design or asks to skip comparison,
  honor that instruction. If they request new alternatives, update the comparison
  and obtain a new choice.

The previews are an intermediate deliverable. While awaiting a choice, show the
previews and wait; the final explanation is delivered after the design is chosen.

## Explain without distorting

- Use an analogy only when it helps. Preserve the important relationships and
  state where the analogy stops working. Avoid childish language unless requested.
- Distinguish what happened from why it may have happened. Label proposed causal
  links and attribute competing interpretations in proportion to their evidence.
- In comparisons, use the same criteria, units, period, and scope for each option.
  Mark missing data rather than inventing a score or ranking.
- In quantitative explanations, show assumptions, units, and the calculation
  that matters. Label made-up examples as illustrative.
- Make boundaries and uncertainty visible where they change the takeaway. Do not
  add stock warnings, strengths, risks, or action lists to fill a template.
- Add practical next steps when the user wants a decision or action. A definition
  or historical account does not need an improvement plan.

## Make the visual carry the explanation

Choose the smallest useful composition: relationship map, timeline, causal
diagram, aligned comparison, sequence, or chart. Give arrows explicit meaning;
do not use one unlabelled connector for time, causality, and information flow.

- Put the central answer, important relationships, example, and relevant limits
  inside the visual. Keep surrounding prose brief, with supporting detail or
  sources when they are needed. Respect a requested text-only answer.
- Use native SVG shapes, connectors, text, and groups. Reserve most of the space
  for the actual explanation rather than decorative panels or repeated prose.
- For time axes, distinguish proportional spacing from a schematic sequence.
  For charts, label units and avoid visual area or axis choices that distort data.
- Use labels, shapes, and line styles as well as color. Define any evidence
  categories or uncertainty marks that are necessary to read the visual.
- Use readable type (at least 11 screen pixels), explicit text wrapping, clear
  reading order, a concise SVG `title` and `desc`, and unique IDs.
- Design for desktop and mobile. Reflow or provide a mobile composition when a
  fixed viewBox would shrink labels below readable size. Use theme-aware colors;
  standalone SVGs must include their own light/dark palette.

## Adapt to the host

Use an available surface compatible with the user's selected presentation
method after reading its relevant instructions. Check actual capability
availability rather than only the host name: a model reading an image does not
guarantee the user can see it. Preserve a self-contained SVG for portability.
Add local interaction only when it helps investigate a relationship or scenario.

If there is no suitable native surface, write a standalone `.svg` in an authorized
workspace and return its link. If the chosen method is unavailable, explain the limitation and let the user
choose another method or inspect the files. Keep the explanation in SVG. Do not make completion depend on a particular vendor's
tool, external script, font service, or rendering service.

For a README, embed repository-relative static SVG assets and keep installation
commands, links, and a concise accessible text equivalent in Markdown. GitHub
readers should not need JavaScript or a separate hosted app to understand it.

## Verify and deliver

- Re-check the central answer, chronology, numerical examples, and important
  relationships against the evidence. Remove unsupported causal implications.
- Confirm facts, interpretations, assumptions, and uncertainty are distinguishable
  where relevant; do not label every sentence mechanically.
- Render and inspect desktop and mobile layouts and both themes where supported.
  Fix clipping, overlaps, misleading arrows, weak contrast, and unreadable text.
- Validate standalone SVG as XML and keep it free of external runtime dependencies.
  If rendering is unavailable, return the artifact and state which checks remain.
- Deliver the explanation in the same turn, with the visual or its link unless
  the user requested another format. Give a brief takeaway rather than duplicating
  the visual in a long prose summary.
