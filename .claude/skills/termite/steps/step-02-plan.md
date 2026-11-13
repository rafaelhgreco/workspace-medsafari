# Step 02 - Plan

Goal: produce `delivery/03-implementation-plan.md` and get human approval.

## 1. Use the vendored skill with overrides
Invoke the `writing-plans` skill (it is vendored; never edit it). Apply these overrides, which win over the skill text:
- Save to `artifacts/active/<slug>/delivery/03-implementation-plan.md` (NOT `docs/superpowers/plans/`).
- Replace the header line "REQUIRED SUB-SKILL ..." with: `Plan produced by Termite; tasks are executed by step-03 of the termite skill.`
- Skip the final execution handoff (executing-plans / subagent-driven-development are not used).
- Input is `delivery/02-tech-spec.md` (Work decomposition) and `01-functional-stories.md`; the plan's `Spec:` line points to the spec.

## 2. Task format (each task)
```
### Task N: <title>
- layer: domain | application | adapters-postgres | adapters-http | bootstrap | frontend
- repo: <name>
- depends_on: [<task numbers>]
- covers: AC-xx, BR-xx
- test_scope: unit | unit+integration
- verify: <exact commands>
- commit: <type>(<scope>): <subject>
- [ ] write failing test ...
- [ ] run it, see it fail
- [ ] implement the minimum
- [ ] run tests, see them pass
- [ ] commit
```
- `test_scope = unit+integration` if and only if the task touches `crates/adapters-postgres/` or `migrations/`; otherwise `unit`.
- Tasks follow the Work decomposition order; each Work item maps to one or more tasks; every AC and BR is covered by some task.
- A `unit+integration` task lists the integration test file under `crates/adapters-postgres/tests/`.

## 3. Checkpoint (human gate)
Show a table: task, layer, repo, covers, test_scope. Ask: approve or request changes.
- Changes: edit the plan and show again.
- Explicit approval: append `{stage:"termite_plan", approver, date}` to `approvals[]`; set `artifacts.delivery.implementationPlan = "delivery/03-implementation-plan.md"`; transition `termite_plan -> termite_code` (history, `by: "termite"`); run `[validation].command`.

## Done when
Plan approved and status `termite_code`. Load `steps/step-03-code-tdd.md`.
