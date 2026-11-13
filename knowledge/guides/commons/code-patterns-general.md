# Code Patterns - General

## Quick rules
- Write commits as Conventional Commits: `<type>(<scope>): <subject>`; types `feat|fix|refactor|chore|docs|test|perf|build|ci`.
- Name branches `<type>/<slug>` with slug `[a-z0-9-]+`; Turtle creates them, never create branches by hand during a task.
- Make one commit per task; never commit a red test suite.
- Respect the dependency direction domain <- application <- adapters <- bootstrap; never import against it.
- Rust: `snake_case` functions/modules/files, `UpperCamelCase` types, `SCREAMING_SNAKE_CASE` constants. [PROPOSED]
- TypeScript: `camelCase` members, `PascalCase` types/classes, `kebab-case` file names with Angular suffix (`.component.ts`, `.service.ts`). [PROPOSED]
- SQL: `snake_case`, plural table names, foreign keys named `<singular>_id`. [PROPOSED]
- Comment the why, never the what; do not put BR/ST/AC/Epic ids or task references in source comments. [PROPOSED]
- Never swallow errors: propagate typed errors and map them at the edge. [PROPOSED]
- Keep functions small and single-purpose; extract when a name explains better than a comment. [PROPOSED]
- Do not hand-edit generated files (OpenAPI client, `.sqlx/` metadata). [PROPOSED]
- Leave no dead code and no unexplained placeholder comments. [PROPOSED]

## Commits and branches
| Item | Rule | Example |
|---|---|---|
| Commit subject | imperative, lowercase, no trailing period, <= 72 chars | `feat(appointments): cancel up to 24h before start` |
| Scope | the crate, feature or module touched | `adapters-postgres`, `appointments` |
| Branch | `<type>/<slug>` | `feat/cancel-appointment` |
| Breaking change | `!` after the scope and a `BREAKING CHANGE:` footer | `feat(api)!: rename status field` |

Source: docs/decisions/phase-2-decisions.md (Conventional Commits, `<type>/<slug>`, one commit per task).

## Naming
| Thing | Convention | Example |
|---|---|---|
| Rust crate (workspace) | kebab-case | `adapters-postgres` |
| Rust module/file | snake_case | `cancel_appointment.rs` |
| Rust type / trait | UpperCamelCase | `AppointmentRepository` |
| Port trait | named for the capability | `Clock`, `AppointmentRepository` |
| TS file | kebab-case + suffix | `appointments.service.ts` |
| SQL table / column | snake_case, plural table | `appointments.starts_at` |
| Test names | cite the rule, see testing guide | `ac_02_br_01_rejects_late_cancellation` |

[PROPOSED]

## Comments and errors
- A comment states a constraint, a trade-off or a non-obvious reason. Remove comments that restate the code.
- Errors are values: use typed errors per layer (see backend guide), add context at the boundary, log once where the error is handled, not where it is propagated.
- Do not use panics (`unwrap`, `expect`) outside tests and `main` setup; in TypeScript do not leave empty `catch` blocks.

[PROPOSED]

## Dependency direction
Inner layers know nothing about outer ones. Domain has no I/O and no framework types. Application defines ports (traits). Adapters implement ports. Bootstrap wires everything. Frontend: `core/` and `shared/` never import from `features/`; features do not import each other (use `shared/` or `core/`).

Source: docs/decisions/phase-2-decisions.md.

## Examples
```text
feat(adapters-postgres): persist appointment cancellation
test(appointments): add AC-02 refusal scenario
fix(adapters-http): return 409 problem+json on closed window
chore(build): add nextest profiles
```

## Open conflicts
None (no team documents available yet). Reconcile every `[PROPOSED]` item when team documents arrive; see `knowledge/guides/GAPS.md`.
