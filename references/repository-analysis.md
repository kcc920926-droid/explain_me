# Repository and infrastructure explanations

Apply this reference only when the subject is a codebase or deployed system.
Combine it with the common evidence and presentation rules in `SKILL.md`.

## Inspect the actual system

- Read applicable repository instructions and top-level documentation first.
- Inventory relevant deployable units, services, jobs, stores, queues, caches,
  observability resources, external dependencies, and exposure paths.
- Trace edges through configuration, environment variables, ports, mounts,
  selectors, imports, and entry commands. Check the entrypoint before treating a
  script as a running service.
- Calculate counts and capacity when they materially explain the system. For
  Kubernetes, include replicas when totaling pods and resource requests or limits.
- Inspect adjacent code to verify an architectural edge or missing role; stay
  within the requested explanation rather than starting an unrelated full audit.

## Separate runtime evidence

These categories describe evidence about a system, not degrees of confidence:

| State | What supports it |
| --- | --- |
| `declared` | Deployable configuration |
| `intended` | Comments, design documents, or stated goals |
| `recorded` | Historical logs, screenshots, exports, or prior command output |
| `observed` | Live runtime inspection performed during this analysis |

Keep unsupported claims unverified. Never present intended behavior as deployed.
Saved artifacts cannot by themselves prove current state. For recorded evidence,
show observation time and qualify freshness; if unknown, say so rather than using
the commit date. A newly fetched historical log is still historical evidence.
If live inspection is unavailable, state that limitation. Re-check every observed
claim against an actual live observation from this analysis before delivery.

## Map the architecture

Select the layers that matter to the question:

- **Context:** users, external systems, public entry paths, and system boundary.
- **Workloads:** APIs, workers, jobs, consumers, replicas, and role boundaries.
- **Flow:** request direction, work assignment, event transport, replay, fan-out.
- **Data responsibility:** source of truth, durable state, transport, cache, and
  rebuildable derived views.
- **Operations:** metrics, dashboards, alerts, scaling, and failure containment.

Use solid edges for declared relationships and clearly labeled dashed edges for
intended but undeclared behavior. Label recorded and observed overlays separately.
Show transitional coupling such as local paths, manual bootstrapping, or an old
production route when it changes how the system works.

When assessment is requested, explain strengths and risks as evidence and
consequence, then prioritize concrete next moves. Favor data-loss paths, missing
desired state, silent monitoring failures, exposure, and reproducibility over
cosmetic changes. Calibrate to the stated environment: a deliberate single-node
home lab is not a failed high-availability cluster. Do not invent maturity scores
or require a fixed number of findings.
