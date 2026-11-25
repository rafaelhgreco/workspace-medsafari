# Guides - gaps and decisions

Status: the team documents expected in `knowledge/_sources/{commons,backend,database,frontend}/` did not exist when these guides were written (phase 2c). Every guide is built from `docs/decisions/phase-2-decisions.md` plus good practice; anything not literally decided is marked `[PROPOSED]`. This file is the review list.

## Open conflicts
| ID | Where | Conflict | Needs |
|---|---|---|---|
| OC-01 | `database/testing-testcontainers-guide-database.md`, `.claude/skills/termite/customize.toml` (`[tests.backend].integration`) | The request is one Postgres container per test binary reused via `OnceCell`; the decided runner is `cargo nextest`, which runs each test in its own process, so a static is not shared and every test would start its own container. | Human decision: (a) nextest setup script starting one Postgres per run, (b) run the integration profile with `cargo test`, or (c) accept one container per test. |

## Decisions needed (highest impact first)
| # | Topic | Where | Proposal in the guides |
|---|---|---|---|
| 1 | Test isolation strategy in the adapter | database/testing-testcontainers | Database per test from a migrated template; transaction rollback only for executor-based functions |
| 2 | Authentication mechanism (JWT, session, provider) | backend/middlewares | Not decided; guide gives only a skeleton |
| 3 | Tool to generate the Angular client from OpenAPI | frontend/development | `ng-openapi-gen` into `src/app/core/api/` |
| 4 | How the frontend gets `openapi.json` and the route exposing it | backend/code-patterns, frontend/development | `GET /api-docs/openapi.json`; committed copy or running backend |
| 5 | nextest filterset syntax for profiles `unit`/`integration` | backend/testing-guide-unit | Confirmed 2026-11-23 on `repos/medsafari`: `default-filter` with `package(...)` and `binary(...)` (`.config/nextest.toml`); `cargo nextest list --profile unit` unchanged by the module migration |
| 6 | Vitest split between `test:unit` and `test:component` | frontend/testing | Files `*.spec.ts` vs `*.component.spec.ts` |
| 7 | Supporting crates and versions (tracing, tower-http, async-trait, mockall, testcontainers-modules) | backend, database | Named without pinned versions |
| 8 | Test and migration naming | commons/testing, database/development | `ac_<nn>_br_<nn>_<behavior>`; `<verb>_<object>` migrations |
| 9 | Angular version and its built-in test builder vs a custom Vitest config | frontend/testing | Adapt to the project; scripts names are decided |
| 10 | Code samples were not compiled | all | Review in a real repo |
| 11 | Where `__tests__/` sits: one per kind folder (chosen) vs one tree mirrored at the crate/app root | commons/project-structure, backend/structure, frontend/structure | One `__tests__/` inside each folder that holds code |
| 12 | Dot-separated Rust file names need one `#[path]` line per module in `mod.rs`; the alternative is `<name>_<kind>.rs` with no attribute | backend/structure | Keep the decided `<name>.<kind>.rs` and the `#[path]` lines |
| 13 | Kinds beyond the four decided (`.port`, `.value_object`, `.error`, `.dto`, Angular kinds) and the crate-level exceptions (`lib.rs`, `main.rs`, `router.rs`, `openapi.rs`, `config.rs`, `error.rs`) | commons/project-structure, backend/structure, frontend/structure | As listed in the guides |
| 14 | Legacy migration policy: a task moves only the items it touches; a bulk move is its own `refactor` demand | commons/project-structure | As written |
| 15 | `cargo nextest list --profile unit` after the move | backend/structure, backend/testing-guide-unit | Confirmed 2026-11-23: same 175 names as the baseline (plus 5 guard tests), `unit` and `integration` green |
| 16 | The graphify snapshot (commit `7f1a5fea`, 2026-11-18) differs from the guides: frontend lint is Biome (not ESLint) and `package.json` has no `test:unit`/`test:component` scripts; the snapshot also has no `ports.rs` | frontend/development, frontend/testing-unit | Confirm against `~/Documentos/medsafari` and update the guides in a separate change |
| 17 | Module granularity: one module per business capability or aggregate; who approves a new module (Turtle names it in the tech spec) | commons/project-structure, backend/structure | As written (accepted 2026-11-23) |
| 18 | `modules/` also in `adapters-http` and `adapters-postgres` (the request named `domain`, `application` and `bootstrap`); without it controllers and repository implementations would pile up in one folder | backend/structure | Apply to the adapters too (accepted 2026-11-23) |
| 19 | Cross-cutting kernel as `<crate>/src/shared/` (sibling of `modules/`) vs a module named `shared` | backend/structure | `src/shared/`, modules may depend on it, never the reverse (accepted 2026-11-23) |
| 20 | Cross-module dependencies: only through the public API, declared in the tech spec, no cycles; enforced by Rust privacy (`E0603` proven on the real backend), the edge listing in VERIFY and `bootstrap/tests/architecture.rs` | commons/project-structure, backend/structure | As written; the architecture test checks root structure, edges, cycles and `shared` (accepted 2026-11-23, implemented in `refactor/backend-modules`) |
| 21 | Errors per module instead of one crate-wide `DomainError`; `ApiError` stays crate-level with `From<ModuleError>` per module | backend/structure | As written (accepted 2026-11-23) |
| 22 | Shape of per-module wiring in `bootstrap` (`<module>.module.rs`, `providers/`) | backend/structure, backend/code-patterns | Confirmed 2026-11-23: each module exposes `build(...)`, `wiring.rs` only composes; behavior unchanged |
| 23 | Tests of crate-level files live in `<crate>/src/__tests__/<name>.test.rs` (already the practice in `adapters-http`, `application`, `bootstrap`) | backend/structure, commons/project-structure | As written (accepted 2026-11-23) |
| 24 | Initial module cut: `health`, `auth`, `progress` (+ `shared`); `auth` is split only when a new flow justifies it | backend/structure | Done 2026-11-23 on `refactor/backend-modules`; result in "Initial module cut" of the structure guide |
| 25 | `From<...Error> for ApiError` stays in `adapters-http/src/error.rs`; the guide proposes one per module controller file | backend/structure | Decide whether to move each conversion into its module (separate change) |

## Pending reconciliation
When the team documents are added under `knowledge/_sources/`, rerun the guides pass: reconcile each `[PROPOSED]` item below, cite `Source: _sources/...`, and record any conflict with a Phase 2 decision under "Open conflicts" without choosing alone.

## All `[PROPOSED]` items (generated)

### backend/code-patterns-backend.md

- L15: - Define ports as traits in `application`; annotate them with `mockall::automock` for tests. [PROPOSED]
- L17: - Inject dependencies as `Arc<dyn Port>` (use `async_trait` for async ports). [PROPOSED]
- L18: - Do not use `unwrap`/`expect` outside tests and `bootstrap`. [PROPOSED]
- L53: `cfg_attr(test, automock)` only mocks inside the same crate; to mock a port from another crate's tests expose it behind a `mocks` feature. [PROPOSED]
- L83: Do not return internal error text for 5xx; log it and return a generic `detail`. [PROPOSED]
- L98: Collect paths in a `#[derive(OpenApi)]` struct and expose the JSON (for example `GET /api-docs/openapi.json`); the Angular client is generated from it. [PROPOSED] for the exact route.
- L109: [PROPOSED]

### backend/development-guide-backend.md

- L13: - Do not add dependencies without a reason; prefer workspace-level `[workspace.dependencies]`. [PROPOSED]
- L14: - Keep `main.rs` free of logic beyond configuration and wiring. [PROPOSED]
- L15: - Do not bypass clippy with `#[allow]` without a comment stating why. [PROPOSED]
- L49: [PROPOSED] for the exact set of commands.

### backend/middlewares-guide-backend.md

- L5: - Use `tower` / `tower-http` layers composed with `ServiceBuilder`; list them outermost first. [PROPOSED]
- L6: - Apply, in order: request id, tracing, timeout, CORS, auth. [PROPOSED]
- L7: - Generate a request id (`x-request-id`) at the edge and propagate it to logs and responses. [PROPOSED]
- L8: - Trace every request with `tower_http::trace::TraceLayer` and the `tracing` crate; log structured fields, not formatted strings. [PROPOSED]
- L9: - Set a global timeout with `TimeoutLayer`; return problem+json (408/504) on expiry. [PROPOSED]
- L10: - Configure CORS explicitly from configuration (allowed origins/methods/headers); never `Any` in production. [PROPOSED]
- L11: - Implement auth as `axum::middleware::from_fn_with_state` that puts an authenticated principal in request extensions. [PROPOSED]
- L12: - Keep authorization decisions in application use cases; the middleware only authenticates. [PROPOSED]
- L14: - Mark public routes (health, OpenAPI) explicitly; protected is the default. [PROPOSED]
- L15: - Never log secrets, tokens or personal data. [PROPOSED]
- L32: [PROPOSED] (versions and exact layer constructors follow the `tower-http` version in the workspace).
- L50: [PROPOSED]

### backend/structure-guide-backend.md

- L37: - Crate-level files stay as plain files at `src/` (full list in "Initial module cut"). In `adapters-http`, `error.rs` keeps the `From<...Error> for ApiError` conversions; moving each one into the module's controller file is still open. [PROPOSED]
- L201: Source: layout, `__tests__` and `modules/` decisions from the project owner (2026-11-19 and 2026-11-23). Mechanics verified on a proof workspace and then on the real backend: `cargo nextest` profiles `unit` (filters by package, no change needed) and `integration`, `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `E0603` on an import of another module's kind folder, both checks above, per-module wiring in `bootstrap`. Items #15 and #22 of `knowledge/guides/GAPS.md` are confirmed by this run. Items still marked [PROPOSED] extend the decision and need confirmation.

### backend/testing-guide-unit-backend.md

- L11: - Name tests `ac_<nn>_br_<nn>_<behavior>` so they trace to the story. [PROPOSED]
- L12: - Use builders/factories for test data; keep each test readable in one screen. [PROPOSED]
- L13: - Make the clock and id generation ports so tests are deterministic. [PROPOSED]
- L16: - Use `#[tokio::test]` for async tests; avoid `sleep`. [PROPOSED]
- L57: [PROPOSED]

### commons/code-patterns-general.md

- L9: - Rust: `snake_case` functions/modules/files, `UpperCamelCase` types, `SCREAMING_SNAKE_CASE` constants. [PROPOSED]
- L10: - TypeScript: `camelCase` members, `PascalCase` types/classes, `kebab-case` file names with Angular suffix (`.component.ts`, `.service.ts`). [PROPOSED]
- L11: - SQL: `snake_case`, plural table names, foreign keys named `<singular>_id`. [PROPOSED]
- L12: - Comment the why, never the what; do not put BR/ST/AC/Epic ids or task references in source comments. [PROPOSED]
- L13: - Never swallow errors: propagate typed errors and map them at the edge. [PROPOSED]
- L14: - Keep functions small and single-purpose; extract when a name explains better than a comment. [PROPOSED]
- L15: - Do not hand-edit generated files (OpenAPI client, `.sqlx/` metadata). [PROPOSED]
- L16: - Leave no dead code and no unexplained placeholder comments. [PROPOSED]
- L41: [PROPOSED]
- L48: [PROPOSED]
- L64: None (no team documents available yet). Reconcile every `[PROPOSED]` item when team documents arrive; see `knowledge/guides/GAPS.md`.

### commons/project-structure-general.md

- L62: - A task that changes an item still living in a legacy file (`ports.rs`, an inline `mod tests`) moves that item, and its tests, to the new layout (module, kind folder, `__tests__/`) in the same task. [PROPOSED]
- L63: - Migrating the rest of a legacy file is its own `refactor` demand; do not mix a bulk move with feature work. [PROPOSED]
- L75: Source: layout and `__tests__` decision from the project owner (2026-11-19); the `modules/` decision is from 2026-11-23; the Rust mechanics were checked by compiling proof workspaces (cargo 1.97: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`). Items marked [PROPOSED] extend that decision and need confirmation; see `knowledge/guides/GAPS.md`.

### commons/testing-guide-unit-general.md

- L7: - Rust test names: `ac_<nn>_br_<nn>_<behavior>` (for example `ac_02_br_01_rejects_late_cancellation`). [PROPOSED]
- L8: - TypeScript test names: `it('AC-02 [BR-01] rejects late cancellation')`. [PROPOSED]
- L16: - Keep tests deterministic: fixed clock, fixed ids, no sleeps, no order dependence. [PROPOSED]
- L17: - Do not assert on implementation details (private calls, log text) unless that is the behavior. [PROPOSED]
- L33: - A test may cover several ids; list them all in the name or in a single trailing id list. [PROPOSED]

### database/code-patterns-database.md

- L5: - Prefer compile-time checked queries (`sqlx::query!`, `query_as!`); fall back to `query`/`query_as` only with a stated reason. [PROPOSED]
- L6: - Commit the `.sqlx/` metadata and build CI/agents with `SQLX_OFFLINE=true`; regenerate with `cargo sqlx prepare --workspace` after any query or migration change. [PROPOSED]
- L7: - Open transactions in the adapter, never in `application`; an atomic operation is one repository method. [PROPOSED]
- L9: - Map `sqlx::Error` to the adapter's own error enum (`thiserror`); translate unique/foreign-key violations into meaningful variants. [PROPOSED]
- L10: - Express invariants as constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY) in addition to domain validation. [PROPOSED]
- L11: - Name SQL objects in `snake_case`, tables plural, foreign keys `<singular>_id`, indexes `idx_<table>_<columns>`. [PROPOSED]
- L12: - Use `timestamptz` for instants and `uuid` for ids. [PROPOSED]
- L13: - Index foreign keys and columns used in `WHERE`/`ORDER BY` of hot queries. [PROPOSED]
- L15: - Keep queries small and named after the use case need (`find_by_id`, `list_open_for_patient`). [PROPOSED]
- L51: [PROPOSED]
- L60: [PROPOSED]

### database/development-guide-database.md

- L5: - Create reversible migrations: `sqlx migrate add -r <name>` produces an `.up.sql` and a `.down.sql`. [PROPOSED]
- L6: - Name migrations `<verb>_<object>` in snake_case (`create_appointments`, `add_canceled_at_to_appointments`); sqlx adds the timestamp prefix. [PROPOSED]
- L9: - Make schema changes backward compatible with the running code: expand, deploy, contract (see below). [PROPOSED]
- L10: - Add NOT NULL columns in steps: nullable add, backfill, then constraint. [PROPOSED]
- L11: - Create indexes on large tables with `CREATE INDEX CONCURRENTLY` in a migration that opts out of the transaction. [PROPOSED]
- L15: - Test the down migration locally at least once before merging. [PROPOSED]
- L25: Source: docs/decisions/phase-2-decisions.md (`sqlx migrate`, sqlx-cli); reversibility and naming are [PROPOSED].
- L32: [PROPOSED]

### database/testing-testcontainers-guide-database.md

- L9: - Isolate tests: create a database per test from a migrated template database; use transaction rollback only for functions that take an executor. [PROPOSED]
- L10: - Build test data with builders; give every builder sensible defaults. [PROPOSED]
- L14: - Keep one file per adapter (for example `appointment_repository.rs`) so each is its own test binary. [PROPOSED]
- L15: - Name tests `ac_<nn>_br_<nn>_<behavior>` when they cover an AC/BR; otherwise by the contract they check. [PROPOSED]
- L47: [PROPOSED] (the one-container-per-binary requirement is a decision; the code is a proposal). The migrations path is relative to the crate: `crates/adapters-postgres` to `../../migrations`.

### frontend/code-patterns-frontend.md

- L11: - Expose service state as read-only signals; keep writable signals private to the service. [PROPOSED]
- L12: - Use `inject()` for dependency injection and `ChangeDetectionStrategy.OnPush` on components. [PROPOSED]
- L13: - Keep pages thin: they compose components and call services; business logic lives in services or pure functions. [PROPOSED]
- L14: - Handle API errors as RFC 7807 problem+json mapped to a typed `ProblemDetails` in `core/`. [PROPOSED]
- L15: - Use typed reactive forms and keep validation messages in `output_language`. [PROPOSED]
- L16: - Use the new control flow (`@if`, `@for`) and `track` in loops. [PROPOSED]
- L53: [PROPOSED]
- L66: [PROPOSED]

### frontend/development-guide-frontend.md

- L10: - Keep every feature self-contained; promote shared code to `shared/` only when a second feature needs it. [PROPOSED]
- L12: - Generate the client with `ng-openapi-gen` from `openapi.json` into `src/app/core/api/` via `npm run api:generate`. [PROPOSED]
- L13: - Fetch `openapi.json` from the running backend or a committed copy; document which in the repo README. [PROPOSED]
- L14: - Do not use `any`; enable `strict` in `tsconfig`. [PROPOSED]
- L15: - Keep accessibility basics: labels, focus order, keyboard use, semantic elements. [PROPOSED]
- L25: Source: docs/decisions/phase-2-decisions.md (`test:unit`, `test:component`, ESLint + Prettier, lefthook); `api:generate` is [PROPOSED].
- L36: [PROPOSED] for the exact set of commands.

### frontend/structure-guide-frontend.md

- L8: - Kinds and suffixes: `.component`, `.service`, `.model`, `.guard`, `.interceptor`, `.pipe`, `.directive`, `.routes`. [PROPOSED] for the ones beyond `.component`, `.service`, `.model`.
- L13: - Test helpers (fakes, builders) used by one folder live in that folder's `__tests__/`; helpers shared across features go to `shared/testing/`. [PROPOSED]
- L14: - `app.ts`, `app.config.ts` and `main.ts` generated by the CLI keep their names; `app.spec.ts` moves to `src/app/__tests__/app.spec.ts`. [PROPOSED]
- L68: - The test run must pick up nested `__tests__/**/*.spec.ts`; the builder default (`**/*.spec.ts`) already matches them and `tsconfig.app.json` must keep excluding `src/**/*.spec.ts` so specs stay out of the app build. [PROPOSED] Confirm with one failing spec in a `__tests__/` folder (RED) before moving the others.
- L78: Source: layout and `__tests__` decision from the project owner (2026-11-19); Angular suffixes follow `commons/code-patterns-general.md`. The tooling check was not executed (no frontend checkout in the session); items marked [PROPOSED] extend the decision.

### frontend/testing-guide-unit-frontend.md

- L7: - Split by file name: `*.spec.ts` for unit, `*.component.spec.ts` for component tests. [PROPOSED]
- L10: - Cite the rule in the test name: `it('AC-02 [BR-01] ...')`. [PROPOSED]
- L13: - Drive signals through the public API; use `TestBed.flushEffects()` / `fixture.detectChanges()` to settle. [PROPOSED]
- L14: - Use a fixed clock and fixed data; no real timers. [PROPOSED]
- L33: [PROPOSED]: the Angular version and its test builder may already provide Vitest; adapt the config to the project instead of duplicating it. The script names are decided.
- L50: If the service uses `inject()`, create it inside `TestBed.runInInjectionContext` with a provided fake. [PROPOSED]
- L67: [PROPOSED]

## Totals

| Guide | [PROPOSED] lines |
|---|---|
| backend/code-patterns-backend.md | 7 |
| backend/development-guide-backend.md | 4 |
| backend/middlewares-guide-backend.md | 12 |
| backend/structure-guide-backend.md | 2 |
| backend/testing-guide-unit-backend.md | 5 |
| commons/code-patterns-general.md | 11 |
| commons/project-structure-general.md | 3 |
| commons/testing-guide-unit-general.md | 5 |
| database/code-patterns-database.md | 11 |
| database/development-guide-database.md | 8 |
| database/testing-testcontainers-guide-database.md | 5 |
| frontend/code-patterns-frontend.md | 8 |
| frontend/development-guide-frontend.md | 7 |
| frontend/structure-guide-frontend.md | 5 |
| frontend/testing-guide-unit-frontend.md | 7 |
| **Total** | 100 |
