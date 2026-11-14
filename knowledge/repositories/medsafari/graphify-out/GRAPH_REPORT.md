# Graph Report - medsafari  (2026-11-14)

## Corpus Check
- 22 files · ~4,149 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 10 file(s) not represented in the graph (top: (none) 5, .css 2, .toml 1)

## Summary
- 161 nodes · 193 edges · 12 communities (8 shown, 4 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- package.json
- development
- main.rs
- biome.json
- app.ts
- frontend
- scripts
- Frontend
- CLAUDE.md
- .claude/CLAUDE.md
- README.md
- backend

## God Nodes (most connected - your core abstractions)
1. `scripts` - 9 edges
2. `frontend` - 7 edges
3. `Frontend` - 7 edges
4. `health()` - 6 edges
5. `development` - 6 edges
6. `@angular/core` - 6 edges
7. `VersionProvider` - 5 edges
8. `build_app()` - 5 edges
9. `build` - 5 edges
10. `options` - 5 edges

## Surprising Connections (you probably didn't know these)
- `@angular/core@^22.2.0` --declares--> `@angular/core`  [EXTRACTED]
  frontend/package.json → frontend/package.json  _Bridges community 0 → community 4_

## Import Cycles
- None detected.

## Communities (12 total, 4 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.08
Nodes (34): dependencies, @angular/compiler@^22.2.0, @angular/core@^22.2.0, @angular/forms@^22.2.0, @angular/platform-browser@^22.2.0, @angular/router@^22.2.0, rxjs@~7.8.0, tslib@^2.3.0 (+26 more)

### Community 1 - "development"
Cohesion: 0.09
Nodes (25): build, serve, test, builder, configurations, defaultConfiguration, options, development (+17 more)

### Community 2 - "main.rs"
Cohesion: 0.12
Nodes (8): AppState, build_app(), CargoVersion, Health, health(), health_retorna_200_com_status_ok_e_versao_do_mock(), main(), VersionProvider

### Community 3 - "biome.json"
Cohesion: 0.09
Nodes (22): source, assist, actions, enabled, files, ignoreUnknown, formatter, enabled (+14 more)

### Community 4 - "app.ts"
Cohesion: 0.20
Nodes (8): @angular/common@^22.2.0, Health, HealthService, App, appConfig, @angular/common, @angular/core, rxjs

### Community 5 - "frontend"
Cohesion: 0.14
Nodes (13): cli, analytics, packageManager, prefix, projectType, root, schematics, sourceRoot (+5 more)

### Community 6 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, check, format, lint, ng, start, test (+1 more)

### Community 7 - "Frontend"
Cohesion: 0.25
Nodes (7): Additional Resources, Building, Code scaffolding, Development server, Frontend, Running end-to-end tests, Running unit tests

## Knowledge Gaps
- **1 isolated node(s):** `backend`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 79 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `scripts` connect `scripts` to `package.json`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `backend` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.07899159663865546 - nodes in this community are weakly interconnected._
- **Why does `architect` connect `development` to `frontend`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Should `development` be split into smaller, more focused modules?**
  _Cohesion score 0.08666666666666667 - nodes in this community are weakly interconnected._
- **Why does `frontend` connect `frontend` to `development`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `main.rs` be split into smaller, more focused modules?**
  _Cohesion score 0.12318840579710146 - nodes in this community are weakly interconnected._