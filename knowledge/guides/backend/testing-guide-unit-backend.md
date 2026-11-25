# Testing Guide - Backend Unit

## Quick rules
- Run unit tests with `cargo nextest run --workspace --profile unit`; it must not need Docker or a database.
- Mock the ports (traits) with `mockall`; never mock domain types or third-party crates.
- Test domain rules with plain values and a fake clock; no mocks needed.
- Test use cases in `application` with mocked ports; assert on results and on port calls that matter.
- Test handlers in `adapters-http` with a fake use case through the router (`tower::ServiceExt::oneshot`): status, headers, problem+json body.
- To mock a port of another module or crate, import the mock re-exported by that module's `mod.rs` (`crate::modules::<module>::Mock<Port>`), never a path through its kind folders.
- Keep unit tests out of the source file: put them in `__tests__/<name>.<kind>.test.rs` next to the code, wired with `#[cfg(test)] #[path = "__tests__/..."] mod tests;` (see `structure-guide-backend.md`).
- Name tests `ac_<nn>_br_<nn>_<behavior>` so they trace to the story. [PROPOSED]
- Use builders/factories for test data; keep each test readable in one screen. [PROPOSED]
- Make the clock and id generation ports so tests are deterministic. [PROPOSED]
- Do not put tests that need Postgres in the `unit` profile; they belong to `crates/adapters-postgres/tests/`.
- Configure the two profiles in `.config/nextest.toml` and check them with `cargo nextest list --profile unit` / `--profile integration`.
- Use `#[tokio::test]` for async tests; avoid `sleep`. [PROPOSED]

## nextest profiles
```toml
# .config/nextest.toml
[profile.default]
fail-fast = false

[profile.unit]
default-filter = "not (package(adapters-postgres) | binary(auth_flow))"

[profile.integration]
default-filter = "package(adapters-postgres) | binary(auth_flow)"
```
`unit` excludes the `adapters-postgres` package and the `auth_flow` binary of `bootstrap` (both start a container); `integration` runs only them. Verified in `repos/medsafari/backend/.config/nextest.toml` with `cargo nextest list --profile unit` (175 tests before and after the module migration). The filters use package and binary names, so moving files into modules changes nothing.
Source: docs/decisions/phase-2-decisions.md (profiles `unit` and `integration`).

## mockall on a port
```rust
// crates/application/src/modules/appointments/usecases/__tests__/cancel_appointment.usecase.test.rs
#[tokio::test]
async fn ac_02_br_01_refuses_cancellation_inside_the_window() {
    // Arrange
    let mut repo = MockAppointmentRepository::new();
    repo.expect_find().returning(|_| Ok(Some(appointment_starting_in_hours(2))));
    repo.expect_save().never();
    let use_case = CancelAppointment::new(Arc::new(repo), Arc::new(FixedClock::now()));
    // Act
    let result = use_case.execute(AppointmentId::new()).await;
    // Assert
    assert!(matches!(result, Err(CancelError::Domain(DomainError::CancellationWindowClosed))));
}
```

## What to mock and what not
| Mock | Do not mock |
|---|---|
| Ports: repositories, clock, id generator, notifier | Domain entities and value objects |
| Fake use case in handler tests | The function under test |
| | `sqlx`/`axum` internals |

[PROPOSED]

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
