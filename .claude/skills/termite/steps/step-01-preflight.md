# Step 01 - Preflight

Goal: confirm the gate, put every repo on its work branch, and establish a green baseline.

## 1. Gate
- Status `termite_plan`, `approvals[]` contains `stage: "turtle_review"`, `branches[]` is non-empty. Otherwise refuse and stop.
- Read `delivery/02-tech-spec.md` in full and note the Work decomposition rows with `persistence = yes`.

## 2. Checkout (file-operator, raw output)
For each entry in `branches[]`:
1. `git -C repos/<repo> status --porcelain` must be empty, else STOP and report.
2. `git -C repos/<repo> checkout <name>`; confirm with `git -C repos/<repo> rev-parse --abbrev-ref HEAD`.

## 3. Tooling check
- Backend repos (`Cargo.toml` present): `cargo nextest --version`. Missing -> STOP and report.
- Frontend repos (`package.json` present): `node --version`; dependencies installed (`ls repos/<repo>/node_modules` or ask the human to `npm install`).
- Check that the nextest profiles `unit` and `integration` exist in `repos/<repo>/.config/nextest.toml`. Missing -> STOP, report, and ask the human whether the first plan task should add them.

## 4. Docker (only if any Work decomposition row has `persistence = yes`)
Run `docker info`. Failure -> STOP and report: integration tests need Docker.

## 5. Baseline (file-operator, raw output; run from each repo directory)
- Backend: `[tests.backend].unit`; if step 4 applies, also `[tests.backend].integration`.
- Frontend: `[tests.frontend].unit` then `[tests.frontend].component`.
- Any red baseline -> STOP and report the failing tests; do not start the plan on a red baseline.

## Done when
All repos are on their branches and the baseline is green. Load `steps/step-02-plan.md`.
