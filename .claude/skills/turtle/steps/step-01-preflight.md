# Step 01 - Preflight

Goal: verify the gate, start the work, and make sure the inputs exist.

## 1. Gate
- `demand-context.json` status must be `tiger_review` AND `approvals[]` must contain `stage: "tiger_review"`. Otherwise refuse (see SKILL.md gate table) and stop.
- `delivery/01-functional-stories.md` must exist; read it in full.

## 2. Transition
Set `tiger_review -> turtle_in_progress` (history entry, `by: "turtle"`), then run `[validation].command`.

## 3. Knowledge
- Always: `knowledge/guides/commons/*.md`.
- By `demandType` (see `[knowledge]`): backend -> backend guides; frontend -> frontend guides; database -> database guides; fullstack -> all three.
- Read each guide's `## Quick rules` first; skip TODO stubs with a one-line note.
- If the impact touches `crates/adapters-postgres/` or `migrations/` and the demand is not already database/fullstack, also load the database guides in step-02 (lazy).

## 4. Graphify-out
For each `targetRepositories[]` entry check that `graphifyPath` exists and is not empty (`ls <graphifyPath>`).
- Missing or empty: STOP. List the missing paths and ask the human to run graphify manually on those repositories and place the output at `knowledge/repositories/<name>/graphify-out/`. Leave the status `turtle_in_progress`; the human re-runs `/turtle <slug>`.
- Present: note the report/index files found; do not load the full graph yet.

## 5. Repositories
Check each `repos/<name>` exists and is a git repository (`git -C repos/<name> rev-parse --is-inside-work-tree`). Missing: stop and ask the human to clone it.

## Done when
Status is `turtle_in_progress`, stories read, guides noted, graphify-out present. Load `steps/step-02-impact-analysis.md`.
