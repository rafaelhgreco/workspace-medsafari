# Development Guide - Backend

## Quick rules
- Work per layer in this order: domain, application, adapters, bootstrap; each step test-first.
- Run `cargo fmt --check` and `cargo clippy --workspace -- -D warnings` before every commit attempt and in VERIFY.
- Run unit tests with `cargo nextest run --workspace --profile unit` after every task.
- Run `cargo nextest run --workspace --profile integration` only for tasks that touch `crates/adapters-postgres/` or `migrations/` (needs Docker).
- Commit with `LEFTHOOK=0`; the hooks run unified in VERIFY with `lefthook run pre-commit`.
- Add a new use case as: domain change (if any), port (if any), use case with mocked ports, adapter, handler, route, OpenAPI annotation.
- Add the port first when a use case needs a new capability; never reach into an adapter from a use case.
- Keep DTO changes and `utoipa` annotations in the same task as the handler so the OpenAPI stays correct.
- Treat a change to the OpenAPI document as an API change: note it in the task so the frontend regenerates its client.
- Do not add dependencies without a reason; prefer workspace-level `[workspace.dependencies]`. [PROPOSED]
- Keep `main.rs` free of logic beyond configuration and wiring. [PROPOSED]
- Do not bypass clippy with `#[allow]` without a comment stating why. [PROPOSED]

## Task flow
1. Read the task: layer, repo, covers (AC/BR), `test_scope`.
2. RED: write the failing test at the correct layer (see testing guides).
3. GREEN: minimal code; keep the dependency rule.
4. REFACTOR; run `fmt`, `clippy`, `unit` profile.
5. `unit+integration` tasks: also write and run the adapter integration test (see database testing guide).
6. Commit (Conventional, `LEFTHOOK=0`).

Source: docs/decisions/phase-2-decisions.md.

## Commands
| Purpose | Command |
|---|---|
| Format check | `cargo fmt --check` |
| Lint | `cargo clippy --workspace -- -D warnings` |
| Unit tests | `cargo nextest run --workspace --profile unit` |
| Integration tests | `cargo nextest run --workspace --profile integration` |
| Hooks (unified) | `lefthook run pre-commit` |
| SQLx metadata | `cargo sqlx prepare --workspace` (see database guide) |

Source: docs/decisions/phase-2-decisions.md; `termite/customize.toml`.

## lefthook
```yaml
# lefthook.yml (backend repo)
pre-commit:
  parallel: true
  commands:
    fmt:    { run: cargo fmt --check }
    clippy: { run: cargo clippy --workspace -- -D warnings }
    unit:   { run: cargo nextest run --workspace --profile unit }
```
[PROPOSED] for the exact set of commands.

## Task checklist
- [ ] Failing test seen RED, then GREEN.
- [ ] Dependency rule respected (no inward imports from outer crates).
- [ ] Errors typed per layer and mapped to problem+json at the edge.
- [ ] `utoipa` annotations updated when the HTTP surface changed.
- [ ] `fmt`, `clippy`, `unit` profile green; `integration` green if in scope.
- [ ] One Conventional Commit.

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
