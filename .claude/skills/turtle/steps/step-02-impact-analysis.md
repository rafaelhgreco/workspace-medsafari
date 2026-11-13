# Step 02 - Impact analysis

Goal: find what the stories change, and write spec sections 1-3 in `delivery/02-tech-spec.md`.

## 1. Locate with graphify
- For each repository, read the graphify report/index first, then query only the nodes, modules, ports, adapters or features related to the stories' behavior.
- Record every graphify source consulted (path). Do not read the whole graph.

## 2. Targeted reads
- Read files in `repos/<name>/` ONLY where graphify pointed. Record each path read.
- If graphify does not cover something you need, say so and tag the conclusion `[INF-xx]`.
- Frontend or fullstack: read `design/` inputs listed in `artifacts.design`.

## 3. Impact by layer
For every affected element, one row: layer, repo, module/file, change, refs (ST/AC/BR), `persistence` (yes if it touches `crates/adapters-postgres/` or `migrations/`).
Layers: domain, application (ports), adapters-postgres, adapters-http (including utoipa OpenAPI contract), bootstrap, migrations (sqlx), Angular feature (`features/<feature>/{pages,components,services,models}`).
- Check the dependency rule domain <- application <- adapters <- bootstrap; reject any design that violates it.

## 4. Write the spec (file-operator or direct)
Create `artifacts/active/<slug>/delivery/02-tech-spec.md`:
1. `# <title> - Tech spec` and a status line (demand id, date, `Proposed branch: <type>/<slug>`; type chosen by the nature of the change).
2. `## Context` - summary of the stories and key BRs.
3. `## Sources` - graphify paths consulted and repo files read.
4. `## Impact by layer` - the table from section 3 above.
IDs and headings stay in English; prose uses `output_language`.

## Done when
The file exists with Context, Sources and Impact by layer. Load `steps/step-03-tech-spec.md`.
