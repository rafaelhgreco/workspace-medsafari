# Step 03 - Code with TDD

Goal: implement each plan task, one commit per task. Resume rule: start at the first task whose steps are not all checked.

## Per task (in plan order, respecting depends_on)
1. Quick check (file-operator): current branch equals the task repo's `branches[]` name; working tree has no unrelated changes.
2. Invoke the `test-driven-development` skill (vendored; do not edit it). Cycle RED -> GREEN -> REFACTOR:
   - YOU write the tests and the code with Read/Edit/Write; file-operator only runs commands.
   - Backend unit tests: `cargo nextest` + `mockall` mocks of ports (traits). Frontend: Vitest.
   - Respect the hexagonal dependency rule; adapters implement ports, domain has no I/O.
3. If `test_scope = unit+integration`: the cycle also covers an integration test of the adapter in `crates/adapters-postgres/tests/`, with testcontainers-rs and a real Postgres; apply migrations in the container with `sqlx::migrate!`. Confirm `docker info` still works.
4. Run the tests for the task (file-operator, raw output) until green.
5. Regression at the end of the task (file-operator, raw output):
   - always: `[tests.backend].unit` for backend; `[tests.frontend].unit` and `.component` for frontend;
   - only when `test_scope = unit+integration`: `[tests.backend].integration`.
6. Commit (file-operator): `git -C repos/<repo> add -A` then `LEFTHOOK=0 git -C repos/<repo> commit -m "<conventional message from the task>"`. One commit per task.
7. Tick the task's checkboxes in the plan and append `commit: <short sha>` to the task.

## Rules
- Red regression: fix before the next task; never commit a red state.
- Never skip a RED step; a test that passes before the code exists is wrong.
- Do not touch files outside the task's scope.
- If a task needs a decision the spec does not cover, stop and ask the human; do not invent.

## Done when
All tasks are checked and committed. Transition `termite_code -> termite_verify` (history, `by: "termite"`), run `[validation].command`, load `steps/step-04-verify.md`.
