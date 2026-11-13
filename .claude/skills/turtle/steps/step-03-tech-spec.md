# Step 03 - Complete the tech spec

Goal: append the remaining sections to `delivery/02-tech-spec.md`.

## 1. Sequence diagrams
`## Sequence diagrams`: one Mermaid `sequenceDiagram` per main flow (use the main flows of the use cases). Participants follow the hexagon: client/Angular, adapters-http, application (use case/port), domain, adapters-postgres, database. Mark error paths that matter.

## 2. Work decomposition
`## Work decomposition`: table `| WD | layer | repo | description | refs (ST/AC/BR) | persistence | depends on |`.
- One item per layer and repository; order by dependency (domain -> application -> adapters -> bootstrap -> frontend).
- `persistence = yes` for items that touch `crates/adapters-postgres/` or `migrations/` (Termite uses this to set `test_scope`).
- Every AC appears in at least one item's refs; every BR as well.

## 3. Risks
`## Risks`: table `| ID | risk | impact | mitigation |`. Include migration risks (backward compatibility, locks, data backfill) when persistence items exist.

## 4. Inferences
- Inline: every inferred statement in the spec carries `[INF-xx]`.
- `## Inferences` table: `| ID | statement | origin | confidence (high/medium/low) | needs human confirmation? |`.
- `origin`: graphify node, repo file read, guide rule, or "assumption".
- Mark `needs human confirmation = yes` for low confidence or anything that changes behavior or the contract.

## 5. Self-check
- Every `[INF-xx]` in the text is in the table and vice versa.
- Every WD traces to refs; every AC and BR is covered.
- Run `grep -c "sequenceDiagram" <spec>` >= 1.

## Done when
All seven sections exist. Load `steps/step-04-review.md`.
