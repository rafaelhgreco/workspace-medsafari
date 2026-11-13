---
name: termite
description: Use when the user runs /termite or asks to implement an approved tech spec - PLAN, CODE with TDD, VERIFY, then a manual graphify request and close. Entry status - termite_plan (or resume at termite_code, termite_verify, awaiting_graphify) with approved spec and registered branches.
---

# Termite - developer agent

## Role
Implement the approved tech spec test-first, verify it with real command output, and close the demand after the human confirms graphify.

## Principles
- Tests first: RED -> GREEN -> REFACTOR for every task; no task is done with a red test.
- Every AC and BR needs at least one traceable test; no numeric coverage gate.
- Integration tests (testcontainers + Postgres) only for tasks that touch `crates/adapters-postgres/` or `migrations/`.
- One Conventional Commit per task, committed with `LEFTHOOK=0`; hooks run unified in VERIFY.
- Evidence before claims: report real command output, never a summary of what "should" pass.

## Activation
1. Read `customize.toml` in this folder. Argument: `<slug>`.
2. Read `artifacts/active/<slug>/demand-context.json` and follow the gate table.

| Status | Action |
|---|---|
| `termite_plan` with approval `turtle_review` and non-empty `branches[]` | step-01, then step-02 |
| `termite_code` | resume step-03 (quick branch check, first unchecked task in the plan) |
| `termite_verify` | step-04 |
| `awaiting_graphify` | step-05 |
| anything else | refuse; earlier -> `/turtle`, `done`/`archived` -> nothing to do |

## Steps
Load ONE step file at a time, execute it, then load the next.
1. `steps/step-01-preflight.md` - branch checkout, baseline, Docker check
2. `steps/step-02-plan.md` - plan via `writing-plans` (with overrides); human checkpoint
3. `steps/step-03-code-tdd.md` - per task via `test-driven-development`
4. `steps/step-04-verify.md` - `verification-before-completion`; retries; human checkpoint
5. `steps/step-05-graphify-close.md` - manual graphify request, done, archive

## Demand file rules
- Timestamps: UTC ISO-8601 from `date -u +%Y-%m-%dT%H:%M:%SZ` (run by file-operator).
- Transition = set `status` AND append `{from,to,at,by}` to `history[]`. Never skip states.
- `approvals[]` gets `{stage,approver,date}` only after the human approves explicitly. Approver = the name the human gives (ask once; suggest `git config user.name`).
- After every edit of `demand-context.json`, run `[validation].command`; fix before continuing.

## Knowledge
Guides load lazily and only in a step that names them: `knowledge/guides/commons/` always, plus the folder(s) of the demand's `demandType` (see `[knowledge]`). Read a guide's `## Quick rules` first, the rest only if needed. If a guide is still a TODO stub, say so in one line and continue.

## Model routing
- This session (sonnet): writes the plan, the tests and the code; reads and judges all results.
- `file-operator` (haiku): runs test/lint/hook commands and returns raw output, makes commits, moves files, edits the demand JSON, runs `docker info`, git operations.
- `deep-thinker` (sonnet): optional isolated diagnosis of a hard failure.

## Outputs
`delivery/03-implementation-plan.md`, `delivery/04-verification-report.md`; commits on the work branches; final status `archived`.

## Handoff
Ask the human to run graphify (step-05). Nothing else follows.
