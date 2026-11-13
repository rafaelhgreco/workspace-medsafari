# Step 05 - Graphify request and close

Goal: ask the human to run graphify manually, then close the demand. Graphify is never run by the agent.

## 1. Changed repositories
For each `branches[]` entry, count commits: `git -C repos/<repo> rev-list --count <default>..<branch>` (default branch via `git symbolic-ref --short refs/remotes/origin/HEAD`, fallback `main`/`master`). Keep repos with count > 0.

## 2. Request (status `awaiting_graphify`)
- Transition `termite_verify -> awaiting_graphify` (history, `by: "termite"`).
- Set `graphify.requestedAt = now` and `graphify.repos = [<repo names>]`; run `[validation].command`.
- Tell the human, in `output_language`, to run graphify on these repositories and write the output to:
  - `repos/<name>` -> `knowledge/repositories/<name>/graphify-out/` (one line per repo, from `targetRepositories[].graphifyPath`).
- Ask them to confirm when done. Stop and wait. Do not close without the confirmation.

## 3. After the human confirms (explicitly)
1. Set `graphify.confirmedBy` (the name the human gives) and `graphify.confirmedAt = now`.
2. Transition `awaiting_graphify -> done` (history, `by: "termite"`); run `[validation].command`.
3. file-operator: `mv artifacts/active/<slug> artifacts/archive/<slug>` (fail if the target exists).
4. In the moved `artifacts/archive/<slug>/demand-context.json`: transition `done -> archived` (history), run `[validation].command` on the new path.
5. Do not commit anything in this repository unless the human asks.

## 4. Final report
In `output_language`: demand id, repos and branches with commit counts, paths of the four deliverables (now under `artifacts/archive/<slug>/delivery/`), and the retries used.

## Done when
The folder is under `artifacts/archive/`, status is `archived`, and the report is delivered.
