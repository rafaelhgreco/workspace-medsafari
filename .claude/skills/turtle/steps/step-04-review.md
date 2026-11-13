# Step 04 - Review (human gate)

Goal: put the spec in review and get an explicit decision.

## 1. Transition
If the status is `turtle_in_progress`: set `turtle_in_progress -> turtle_review` (history, `by: "turtle"`), set `artifacts.delivery.techSpec = "delivery/02-tech-spec.md"`, run `[validation].command`.

## 2. Present
Show a short summary (no full spec):
- file path; counts of work items, diagrams, risks;
- the inferences with `needs human confirmation = yes`, each with its id and statement;
- the proposed branch name `<type>/<slug>` and the repositories that will receive it;
- whether any item has `persistence = yes` (Termite will then need Docker).

## 3. Decision
Ask: approve, or request changes.
- Changes: edit the spec (go back to the affected step-02/03 content), re-run the self-check, keep status `turtle_review`, present again. A changed branch name or type is edited in the spec header.
- Explicit approval: append `{stage:"turtle_review", approver, date}` to `approvals[]`, run `[validation].command`, then load `steps/step-05-branch.md` in the same turn.
- Do not create branches or record approvals without that explicit approval.
