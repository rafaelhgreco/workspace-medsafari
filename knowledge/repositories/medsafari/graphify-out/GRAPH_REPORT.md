# Graph Report - medsafari  (2026-11-18)

## Corpus Check
- 35 files · ~4,968 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 12 file(s) not represented in the graph (top: (none) 6, .toml 2, .css 2)

## Summary
- 259 nodes · 391 edges · 15 communities (12 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7f1a5fea`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- frontend
- application/src/lib.rs
- error.rs
- biome.json
- adapters-http/src/lib.rs
- bootstrap/src/lib.rs
- clippy
- architecture.rs
- scripts
- Frontend
- application
- CLAUDE.md
- .claude/CLAUDE.md
- README.md

## God Nodes (most connected - your core abstractions)
1. `send()` - 12 edges
2. `app()` - 10 edges
3. `VersionError` - 10 edges
4. `GetHealth` - 9 edges
5. `scripts` - 9 edges
6. `ApiError` - 8 edges
7. `json_body()` - 8 edges
8. `AppVersion` - 8 edges
9. `GetHealthError` - 7 edges
10. `use_case_with()` - 7 edges

## Surprising Connections (you probably didn't know these)
- `health()` --references--> `GetHealth`  [EXTRACTED]
  backend/crates/adapters-http/src/health.rs → backend/crates/application/src/lib.rs
- `router()` --references--> `GetHealth`  [EXTRACTED]
  backend/crates/adapters-http/src/lib.rs → backend/crates/application/src/lib.rs
- `failing_provider()` --references--> `VersionError`  [EXTRACTED]
  backend/crates/adapters-http/src/lib.rs → backend/crates/application/src/lib.rs
- `main()` --calls--> `build_router()`  [INFERRED]
  backend/crates/bootstrap/src/main.rs → backend/crates/bootstrap/src/lib.rs
- `adapters-http` --depends_on--> `application`  [EXTRACTED]
  backend/crates/adapters-http/Cargo.toml → backend/crates/application/Cargo.toml

## Import Cycles
- None detected.

## Communities (15 total, 3 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.06
Nodes (42): dependencies, @angular/common@^22.2.0, @angular/compiler@^22.2.0, @angular/core@^22.2.0, @angular/forms@^22.2.0, @angular/platform-browser@^22.2.0, @angular/router@^22.2.0, rxjs@~7.8.0 (+34 more)

### Community 1 - "frontend"
Cohesion: 0.05
Nodes (38): build, serve, test, builder, configurations, defaultConfiguration, options, cli (+30 more)

### Community 2 - "application/src/lib.rs"
Cohesion: 0.12
Nodes (18): ac_01_br_01_reports_status_ok(), ac_03_br_05_propagates_version_failure(), ac_05_br_04_returns_version_from_replaced_port(), GetHealth, Health, HealthStatus, Ok, use_case_with() (+10 more)

### Community 3 - "error.rs"
Cohesion: 0.12
Nodes (8): ApiError, Problem, health(), HealthResponse, ApiDoc, openapi(), GetHealthError, Version

### Community 4 - "biome.json"
Cohesion: 0.09
Nodes (22): source, assist, actions, enabled, files, ignoreUnknown, formatter, enabled (+14 more)

### Community 5 - "adapters-http/src/lib.rs"
Cohesion: 0.26
Nodes (14): ac_01_br_01_health_returns_200_with_ok_and_version(), ac_01_br_01_post_health_keeps_405(), ac_01_br_01_unknown_route_keeps_404(), ac_03_br_05_empty_version_is_problem_json(), ac_03_br_05_health_failure_is_problem_json_without_cause(), ac_07_br_06_openapi_describes_health(), ac_08_br_05_error_body_has_problem_fields(), app() (+6 more)

### Community 6 - "bootstrap/src/lib.rs"
Cohesion: 0.13
Nodes (4): ac_01_br_01_router_serves_health_with_package_version(), build_router(), LISTEN_ADDR, main()

### Community 7 - "clippy"
Cohesion: 0.12
Nodes (15): glob, root, run, clippy, fmt, unit, glob, root (+7 more)

### Community 8 - "architecture.rs"
Cohesion: 0.31
Nodes (5): ac_04_br_02_layers_only_depend_inward(), ac_04_br_03_domain_has_no_framework_or_runtime_dependency(), ac_13_br_11_no_postgres_crate_and_no_sqlx_user(), ALLOWED, direct_dependencies()

### Community 9 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, check, format, lint, ng, start, test (+1 more)

### Community 10 - "Frontend"
Cohesion: 0.25
Nodes (7): Additional Resources, Building, Code scaffolding, Development server, Frontend, Running end-to-end tests, Running unit tests

### Community 11 - "application"
Cohesion: 0.83
Nodes (4): adapters-http, application, bootstrap, domain

## Knowledge Gaps
- **4 isolated node(s):** `Invalid`, `Ok`, `Version`, `EmptyVersion`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 102 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `VersionError` connect `application/src/lib.rs` to `error.rs`, `adapters-http/src/lib.rs`, `bootstrap/src/lib.rs`?**
  _High betweenness centrality (0.022) - this node is a cross-community bridge._
- **What connects `Invalid`, `Ok`, `Version` to the rest of the system?**
  _4 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.0611764705882353 - nodes in this community are weakly interconnected._
- **Why does `GetHealth` connect `application/src/lib.rs` to `error.rs`, `adapters-http/src/lib.rs`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Should `frontend` be split into smaller, more focused modules?**
  _Cohesion score 0.05398110661268556 - nodes in this community are weakly interconnected._
- **Why does `scripts` connect `scripts` to `package.json`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Should `application/src/lib.rs` be split into smaller, more focused modules?**
  _Cohesion score 0.12183908045977011 - nodes in this community are weakly interconnected._