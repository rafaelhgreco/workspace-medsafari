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
| 5 | nextest filterset syntax for profiles `unit`/`integration` | backend/testing-guide-unit | `default-filter` with `package(...)` and `kind(test)`; confirm with `cargo nextest list` on the pinned version |
| 6 | Vitest split between `test:unit` and `test:component` | frontend/testing | Files `*.spec.ts` vs `*.component.spec.ts` |
| 7 | Supporting crates and versions (tracing, tower-http, async-trait, mockall, testcontainers-modules) | backend, database | Named without pinned versions |
| 8 | Test and migration naming | commons/testing, database/development | `ac_<nn>_br_<nn>_<behavior>`; `<verb>_<object>` migrations |
| 9 | Angular version and its built-in test builder vs a custom Vitest config | frontend/testing | Adapt to the project; scripts names are decided |
| 10 | Code samples were not compiled | all | Review in a real repo |

## Pending reconciliation
When the team documents are added under `knowledge/_sources/`, rerun the guides pass: reconcile each `[PROPOSED]` item below, cite `Source: _sources/...`, and record any conflict with a Phase 2 decision under "Open conflicts" without choosing alone.

## All `[PROPOSED]` items (generated)

### backend/code-patterns-backend.md

- L15: - Define ports as traits in `application`; annotate them with `mockall::automock` for tests. [PROPOSED]
- L16: - Inject dependencies as `Arc<dyn Port>` (use `async_trait` for async ports). [PROPOSED]
- L17: - Do not use `unwrap`/`expect` outside tests and `bootstrap`. [PROPOSED]
- L52: `cfg_attr(test, automock)` only mocks inside the same crate; to mock a port from another crate's tests expose it behind a `mocks` feature. [PROPOSED]
- L82: Do not return internal error text for 5xx; log it and return a generic `detail`. [PROPOSED]
- L96: Collect paths in a `#[derive(OpenApi)]` struct and expose the JSON (for example `GET /api-docs/openapi.json`); the Angular client is generated from it. [PROPOSED] for the exact route.
- L107: [PROPOSED]

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

### backend/testing-guide-unit-backend.md

- L9: - Keep unit tests in `#[cfg(test)] mod tests` next to the code. [PROPOSED]
- L10: - Name tests `ac_<nn>_br_<nn>_<behavior>` so they trace to the story. [PROPOSED]
- L11: - Use builders/factories for test data; keep each test readable in one screen. [PROPOSED]
- L12: - Make the clock and id generation ports so tests are deterministic. [PROPOSED]
- L15: - Use `#[tokio::test]` for async tests; avoid `sleep`. [PROPOSED]
- L29: `unit` excludes the `adapters-postgres` integration test binaries (`crates/adapters-postgres/tests/`); `integration` runs only them. The exact `default-filter`/`kind(test)` filterset syntax depends on the nextest version: confirm with `cargo nextest list`. [PROPOSED]
- L55: [PROPOSED]

### commons/code-patterns-general.md

- L8: - Rust: `snake_case` functions/modules/files, `UpperCamelCase` types, `SCREAMING_SNAKE_CASE` constants. [PROPOSED]
- L9: - TypeScript: `camelCase` members, `PascalCase` types/classes, `kebab-case` file names with Angular suffix (`.component.ts`, `.service.ts`). [PROPOSED]
- L10: - SQL: `snake_case`, plural table names, foreign keys named `<singular>_id`. [PROPOSED]
- L11: - Comment the why, never the what; do not put BR/ST/AC/Epic ids or task references in source comments. [PROPOSED]
- L12: - Never swallow errors: propagate typed errors and map them at the edge. [PROPOSED]
- L13: - Keep functions small and single-purpose; extract when a name explains better than a comment. [PROPOSED]
- L14: - Do not hand-edit generated files (OpenAPI client, `.sqlx/` metadata). [PROPOSED]
- L15: - Leave no dead code and no unexplained placeholder comments. [PROPOSED]
- L38: [PROPOSED]
- L45: [PROPOSED]
- L61: None (no team documents available yet). Reconcile every `[PROPOSED]` item when team documents arrive; see `knowledge/guides/GAPS.md`.

### commons/testing-guide-unit-general.md

- L7: - Rust test names: `ac_<nn>_br_<nn>_<behavior>` (for example `ac_02_br_01_rejects_late_cancellation`). [PROPOSED]
- L8: - TypeScript test names: `it('AC-02 [BR-01] rejects late cancellation')`. [PROPOSED]
- L15: - Keep tests deterministic: fixed clock, fixed ids, no sleeps, no order dependence. [PROPOSED]
- L16: - Do not assert on implementation details (private calls, log text) unless that is the behavior. [PROPOSED]
- L32: - A test may cover several ids; list them all in the name or in a single trailing id list. [PROPOSED]

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
- L51: [PROPOSED]
- L64: [PROPOSED]

### frontend/development-guide-frontend.md

- L10: - Keep every feature self-contained; promote shared code to `shared/` only when a second feature needs it. [PROPOSED]
- L12: - Generate the client with `ng-openapi-gen` from `openapi.json` into `src/app/core/api/` via `npm run api:generate`. [PROPOSED]
- L13: - Fetch `openapi.json` from the running backend or a committed copy; document which in the repo README. [PROPOSED]
- L14: - Do not use `any`; enable `strict` in `tsconfig`. [PROPOSED]
- L15: - Keep accessibility basics: labels, focus order, keyboard use, semantic elements. [PROPOSED]
- L25: Source: docs/decisions/phase-2-decisions.md (`test:unit`, `test:component`, ESLint + Prettier, lefthook); `api:generate` is [PROPOSED].
- L36: [PROPOSED] for the exact set of commands.

### frontend/testing-guide-unit-frontend.md

- L7: - Split by file name: `*.spec.ts` for unit, `*.component.spec.ts` for component tests. [PROPOSED]
- L9: - Cite the rule in the test name: `it('AC-02 [BR-01] ...')`. [PROPOSED]
- L12: - Drive signals through the public API; use `TestBed.flushEffects()` / `fixture.detectChanges()` to settle. [PROPOSED]
- L13: - Use a fixed clock and fixed data; no real timers. [PROPOSED]
- L32: [PROPOSED]: the Angular version and its test builder may already provide Vitest; adapt the config to the project instead of duplicating it. The script names are decided.
- L46: If the service uses `inject()`, create it inside `TestBed.runInInjectionContext` with a provided fake. [PROPOSED]
- L60: [PROPOSED]

## Totals

| Guide | [PROPOSED] lines |
|---|---|
| backend/code-patterns-backend.md | 7 |
| backend/development-guide-backend.md | 4 |
| backend/middlewares-guide-backend.md | 12 |
| backend/testing-guide-unit-backend.md | 7 |
| commons/code-patterns-general.md | 11 |
| commons/testing-guide-unit-general.md | 5 |
| database/code-patterns-database.md | 11 |
| database/development-guide-database.md | 8 |
| database/testing-testcontainers-guide-database.md | 5 |
| frontend/code-patterns-frontend.md | 8 |
| frontend/development-guide-frontend.md | 7 |
| frontend/testing-guide-unit-frontend.md | 7 |
| **Total** | 92 |
