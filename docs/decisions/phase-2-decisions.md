# Phase 2 decisions

Source of truth for phase 2. Every later file (agents, guides, templates) must follow this table set.

## Stack

| Area | Decision | Notes |
|---|---|---|
| Architecture | Hexagonal | Ports (traits) in `application`, adapters implement them |
| Backend | Rust + Axum, multi-crate workspace | `crates/domain`, `crates/application`, `crates/adapters-postgres`, `crates/adapters-http`, `crates/bootstrap` |
| Dependency rule | domain <- application <- adapters <- bootstrap | Never the reverse; `bootstrap` is the only composition root |
| Database | Postgres via sqlx | Migrations with `sqlx migrate` (sqlx-cli) in `migrations/` |
| Errors | `thiserror` per layer | HTTP adapter maps to `IntoResponse` as RFC 7807 `application/problem+json` |
| API contract | OpenAPI generated with utoipa | Angular generates client and types from the OpenAPI document |
| Frontend | Angular, standalone components | Signals + services, no state library |
| Frontend structure | Feature-based | `core/`, `shared/`, `features/<feature>/{pages,components,services,models}` |
| Lint / format (backend) | `cargo fmt --check`, `cargo clippy -- -D warnings` | |
| Lint / format (frontend) | Angular ESLint + Prettier | |
| Git hooks | lefthook in both repos | Termite commits with `LEFTHOOK=0`; hooks run unified in Verify via `lefthook run pre-commit` |

## Testing (Termite)

| Kind | When | Tooling | Location / profile |
|---|---|---|---|
| Unit (backend) | Always | `cargo nextest` + `mockall` (mocks of ports/traits) | nextest profile `unit` excludes `adapters-postgres/tests` |
| Unit (frontend) | Always | Vitest | npm scripts `test:unit` and `test:component` |
| Integration | ONLY if the task has backend AND SQL (touches `crates/adapters-postgres` or `migrations/`) | testcontainers-rs + real Postgres | `crates/adapters-postgres/tests/`; nextest profile `integration` runs only these; config in `.config/nextest.toml`; requires Docker |
| Coverage | No numeric gate | | Every AC and BR needs at least one traceable test |

Each task in the implementation plan declares `test_scope: unit | unit+integration`.

## Workflow

| Topic | Decision |
|---|---|
| Invocation | `/tiger`, `/turtle`, `/termite` |
| Persona | Lean: role + 3-5 operational principles, no roleplay |
| Human gates | After Tiger, after Turtle (between agents); Termite adds checkpoints after Plan and after Verify |
| Output language | `output_language` in `customize.toml` (default pt-BR); IDs, tags and fixed headings stay in English |
| `design/` folder | UI/UX inputs (screenshots, Figma links, references); read by Turtle and Termite on frontend demands |

### Tiger

| Topic | Decision |
|---|---|
| Intake | Hybrid: read the demand, ask only about gaps |
| Acceptance criteria | Gherkin; every scenario references a business rule `BR-xx` |
| Use cases | Simplified Cockburn |
| Tasks | Functional tasks only (`FT-xx`) |
| Output | Single file `delivery/01-functional-stories.md` |

### Turtle

| Topic | Decision |
|---|---|
| Sources | graphify-out first; targeted reads in `repos/` only where graphify points |
| Inferences | Inline tag `[INF-xx]` + final table (origin, confidence, needs human confirmation?) |
| Required diagram | Sequence diagram (Mermaid) |
| Branch | Creates `<type>/<slug>` ONLY after the spec is approved |
| Output | `delivery/02-tech-spec.md` |

### Termite

| Topic | Decision |
|---|---|
| Roles | Sonnet writes tests and code; `file-operator` runs commands, commits and file operations |
| Flow | PLAN -> CODE (TDD) -> VERIFY |
| Commits | One Conventional Commit per task |
| Verify failure | Back to TDD on the affected task; max 2 retries (`verifyRetries`), then stop and report |
| Outputs | `delivery/03-implementation-plan.md`, `delivery/04-verification-report.md` |
| Ending | Requests manual graphify; status `awaiting_graphify` |
