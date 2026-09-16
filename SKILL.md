---
name: svg-eli5-archify
description: Analyze a codebase or infrastructure repository and produce an evidence-backed, SVG-first one-page architecture explainer using simple ELI5 analogies and layered system mapping. Use for requests to understand, review, or present a repository or deployed system visually; do not use for generic charts, implementation-only work, or text-only summaries.
---

# SVG ELI5 Archify

Turn a repository into one page that answers four questions at a glance:

1. What is the system?
2. How does work and data move through it?
3. Which decisions are strong, and where can it fail silently?
4. What should happen next?

The SVG is the explanation, not decoration. Put the architecture, evidence state,
findings, and next actions inside the visual. Keep prose outside the visual to at
most one short conclusion.

## Evidence first

Inspect the repository before drawing. Prefer local source and configuration over
assumptions.

- Read applicable repository instructions and the top-level documentation.
- Inventory deployable units, services, jobs, data stores, queues, caches,
  observability resources, external dependencies, and exposure paths.
- Trace dependencies from configuration, environment variables, ports, mounts,
  selectors, imports, and entry commands. Check the application entrypoint before
  treating a script as a running service.
- Calculate exact counts and capacity when they materially explain the system.
  For Kubernetes, include replicas when totaling pods and resource requests or
  limits.
- Compare evidence states explicitly: **declared** in deployable configuration,
  **intended** in comments or design docs, **recorded** in historical runtime
  artifacts, and **observed** through live inspection during the current analysis.
  Never show intended behavior as deployed. If live runtime inspection is
  unavailable, say so.
- Treat committed logs, screenshots, status exports, and prior command output as
  recorded evidence; show their observation time and qualify their freshness. A
  repository artifact cannot by itself establish current runtime state.
- Check adjacent code only to confirm an architectural edge or missing runtime
  role; do not expand into an unrelated full-repository review.

Keep an internal evidence map from every important visual claim to a file and
line or parsed resource. Record whether each claim is declared, intended,
recorded, observed, or unverified. Show citations only when the user requests
them or when the claim would otherwise be hard to verify.

## Archify the system

Organize the page in layers rather than listing files:

- **Context:** users, external systems, the current public path, and the system
  boundary.
- **Workloads:** APIs, workers, scheduled jobs, consumers, replicas, and role
  boundaries.
- **Flow:** request direction, work assignment, event transport, replay, and
  fan-out.
- **Data responsibility:** distinguish source of truth, durable operational
  state, transport, cache, and rebuildable derived views.
- **Operations:** metrics, dashboards, alerts, SLOs, scaling constraints, and
  failure containment.

Use solid connectors for declared relationships. Use clearly labeled dashed
connectors or nodes for intended-but-undeclared behavior. Show transitional
coupling such as local paths, manual bootstrapping, or an old production route
instead of hiding it.

## Explain like five without becoming inaccurate

Use one coherent analogy that preserves system semantics. Good mappings include:

- source of truth → warehouse or archive;
- task queue → ticket desk;
- event log → conveyor belt or shipping ledger;
- cache → short-lived sticky note;
- search index → catalog that can be rebuilt;
- observability → CCTV, gauges, and alarms.

Put the analogy near the title, then use precise technical labels in the diagram.
Do not force an analogy onto components where it would distort ownership,
durability, ordering, or failure behavior.

## Adapt to the host without weakening the result

Use the richest visual surface the current host provides, but keep the SVG as the
portable source of truth.

- If the host provides a visualization, artifact, canvas, or browser-preview
  capability, read its instructions before creating the visual and use it for the
  preview.
- Otherwise create a self-contained `.svg` file in an authorized workspace
  location. Add a minimal HTML preview only when it helps inspection; do not move
  substantive explanation into the wrapper.
- Never make completion depend on a Codex-, Claude-, or Gemini-specific tool. If a
  native preview is unavailable, return the SVG path and state which visual checks
  could not be performed.

## Make the SVG carry the page

- Put the title and analogy, architecture map, evidence legend, strengths, risks,
  and prioritized next moves inside SVG. Outside prose should be no more than a
  short handoff or conclusion.
- Use native SVG shapes, connectors, labels, badges, and grouped regions rather
  than embedding a screenshot or substituting a long Markdown explanation. The
  architecture flow should be the visually dominant region.
- When the host supports responsive inline output, compose a desktop view around
  736px and a separate mobile view around 360px. For standalone output, use a
  responsive `viewBox`; create a mobile companion SVG when one composition cannot
  remain readable at both widths.
- Keep visible text at least 11 screen pixels. Wrap text with explicit `tspan`
  lines and reserve room for the longest label.
- Use host theme tokens when available. For standalone output, define a
  self-contained light/dark palette inside the SVG. Pair color with labels, line
  styles, and shapes so meaning never depends on color alone.
- Give each SVG a concise `title` and `desc`. Keep IDs unique across multiple
  compositions.
- Prefer direct labels over legends. Use a small legend only for durable semantic
  categories such as source, transport, cache, derived view, and missing desired
  state.
- Do not invent maturity scores. Report concrete evidence, consequences, and
  next actions.

## Findings and prioritization

The one page should normally contain:

- three to five strengths that explain sound boundaries or operational choices;
- three to five risks stated as **evidence → consequence**;
- three ordered next moves that close the most important gaps.

Prioritize missing desired state, data-loss paths, silent monitoring failures,
external exposure, and reproducibility before cosmetic cleanup. Calibrate the
assessment to the stated environment: a deliberate single-node home lab is not a
failed high-availability cluster, but it must still be labeled as single-node.

## Verification

Before responding:

- render the available artifact and inspect it at desktop and mobile widths;
- inspect both light and dark themes when the renderer supports them; otherwise
  check both palettes for contrast;
- fix clipped labels, crossing arrows that change meaning, unreadably small text,
  low contrast, duplicate IDs, and unsupported external resources;
- validate standalone SVG as XML and keep it free of external runtime dependencies;
- apply any size or wrapper limits required by the current host's artifact surface;
- require live runtime evidence gathered during the current analysis for every
  `observed` claim; otherwise downgrade it to `recorded`, `declared`, `intended`,
  or `unverified` as appropriate;
- confirm that every `recorded` claim shows its observation time and does not
  imply current runtime state;
- re-check the top findings against source evidence;
- include the visualization or a link to the generated SVG in the same turn.
