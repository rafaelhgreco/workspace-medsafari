# Testing Guide - Backend Unit

## Quick rules
- Run unit tests with `cargo nextest run --workspace --profile unit`; it must not need Docker or a database.
- Mock the ports (traits) with `mockall`; never mock domain types or third-party crates.
- Test domain rules with plain values and a fake clock; no mocks needed.
- Test use cases in `application` with mocked ports; assert on results and on port calls that matter.
- Test handlers in `adapters-http` with a fake use case through the router (`tower::ServiceExt::oneshot`): status, headers, problem+json body.
- Keep unit tests in `#[cfg(test)] mod tests` next to the code. [PROPOSED]
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
default-filter = "not (package(adapters-postgres) and kind(test))"

[profile.integration]
default-filter = "package(adapters-postgres) and kind(test)"
```
`unit` excludes the `adapters-postgres` integration test binaries (`crates/adapters-postgres/tests/`); `integration` runs only them. The exact `default-filter`/`kind(test)` filterset syntax depends on the nextest version: confirm with `cargo nextest list`. [PROPOSED]
Source: docs/decisions/phase-2-decisions.md (profiles `unit` and `integration`).

## mockall on a port
```rust
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
