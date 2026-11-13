# Testing Guide - General

## Quick rules
- Write the failing test first (RED), then the minimum code (GREEN), then refactor.
- Test one behavior per test; name the test after the behavior and cite the rule.
- Every AC and every BR needs at least one traceable test; there is no numeric coverage gate.
- Rust test names: `ac_<nn>_br_<nn>_<behavior>` (for example `ac_02_br_01_rejects_late_cancellation`). [PROPOSED]
- TypeScript test names: `it('AC-02 [BR-01] rejects late cancellation')`. [PROPOSED]
- Structure each test as Arrange, Act, Assert, separated by blank lines.
- Unit tests never touch network, filesystem, clock or database; inject them as ports/services and fake them.
- Mock only your own ports (traits/services), never third-party types or the thing under test.
- A task is `unit` unless it touches `crates/adapters-postgres/` or `migrations/`; then it is `unit+integration`.
- Integration tests need Docker and live in `crates/adapters-postgres/tests/`; do not run them in the `unit` profile.
- Put business rules in unit tests at domain/application; use integration tests only for the adapter contract.
- Keep tests deterministic: fixed clock, fixed ids, no sleeps, no order dependence. [PROPOSED]
- Do not assert on implementation details (private calls, log text) unless that is the behavior. [PROPOSED]
- A test that passes before the code exists is wrong; always see RED first.

## Unit or integration
| Question | Answer |
|---|---|
| Does it check a business rule? | unit (domain/application) |
| Does it check SQL, mapping, constraints, transactions? | integration (`adapters-postgres`) |
| Does it check HTTP status/serialization of a handler? | unit with a fake use case (adapters-http) |
| Does it check an Angular service or pure logic? | `test:unit` |
| Does it render a component? | `test:component` |

Source: docs/decisions/phase-2-decisions.md (Testing table, `test_scope`).

## Traceability
- The verification report maps every AC/BR to a test name, its path and type (unit/integration).
- A test may cover several ids; list them all in the name or in a single trailing id list. [PROPOSED]
- A BR without a test is a verification failure.

Source: docs/decisions/phase-2-decisions.md.

## Examples
```rust
#[test]
fn ac_02_br_01_rejects_late_cancellation() {
    // Arrange
    let clock = FixedClock::at("2026-11-13T12:00:00Z");
    let appointment = Appointment::scheduled("2026-11-13T14:00:00Z");
    // Act
    let result = appointment.cancel(&clock);
    // Assert
    assert!(matches!(result, Err(DomainError::CancellationWindowClosed)));
}
```
```ts
it('AC-02 [BR-01] rejects late cancellation', () => {
  const service = new CancellationPolicy(fixedClock('2026-11-13T12:00:00Z'));
  expect(service.canCancel(startsAt('2026-11-13T14:00:00Z'))).toBe(false);
});
```

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
