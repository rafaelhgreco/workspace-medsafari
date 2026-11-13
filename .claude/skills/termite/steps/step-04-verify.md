# Step 04 - Verify

Goal: prove the work with real output, write the report, and get human approval. Invoke the `verification-before-completion` skill (vendored; do not edit it).

## 1. Run (file-operator, raw output saved; run from each repo)
- Backend: `cargo fmt --check`, `cargo clippy --workspace -- -D warnings`, `[tests.backend].unit` (full). If any plan task has `test_scope = unit+integration`, also `[tests.backend].integration` (full, needs Docker); otherwise record integration as "not applicable".
- Frontend: `npm run lint`, `[tests.frontend].unit`, `[tests.frontend].component`.
- Hooks: `lefthook run pre-commit` in each repo.

## 2. Report: `delivery/04-verification-report.md`
Sections (headings in English, body in `output_language`):
1. `## Summary` - PASS or FAIL, attempt number (`verifyRetries + 1`).
2. `## Commands` - table `| command | repo | exit code | result |` with the real outcomes.
3. `## Traceability` - every AC and BR from `01-functional-stories.md` -> test name and path -> type (unit/integration) -> result. A BR/AC without a test is a FAIL.
4. `## Changed repositories` - repo, branch, number of commits.
5. `## Failures and retries` - each failure with its output excerpt and the task it belongs to.

## 3. On failure
- Read `verifyRetries` (demand file) and `[verify].max_verify_retries` (2).
- If `verifyRetries < max_verify_retries`: increment `verifyRetries`, transition `termite_verify -> termite_code` (history), identify the affected task, un-check its steps in the plan, and return to `steps/step-03-code-tdd.md` for that task only.
- Otherwise STOP: leave the status `termite_verify`, finish the report with the failures, and report to the human. Do not continue.

## 4. On success: human checkpoint
Set `artifacts.delivery.verificationReport = "delivery/04-verification-report.md"`. Show the Summary and Traceability. Ask: approve or request changes.
- Changes: handle them as a failure of the affected task (counts as a retry only if code changes).
- Explicit approval: append `{stage:"termite_verify", approver, date}` to `approvals[]`, run `[validation].command`, load `steps/step-05-graphify-close.md`.
