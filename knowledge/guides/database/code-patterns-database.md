# Code Patterns - Database (Postgres + sqlx)

## Quick rules
- Use Postgres through `sqlx`; all SQL lives in `crates/adapters-postgres`.
- Prefer compile-time checked queries (`sqlx::query!`, `query_as!`); fall back to `query`/`query_as` only with a stated reason. [PROPOSED]
- Commit the `.sqlx/` metadata and build CI/agents with `SQLX_OFFLINE=true`; regenerate with `cargo sqlx prepare --workspace` after any query or migration change. [PROPOSED]
- Open transactions in the adapter, never in `application`; an atomic operation is one repository method. [PROPOSED]
- Map rows to domain types in the adapter; do not expose row structs outside `adapters-postgres`.
- Map `sqlx::Error` to the adapter's own error enum (`thiserror`); translate unique/foreign-key violations into meaningful variants. [PROPOSED]
- Express invariants as constraints (NOT NULL, UNIQUE, CHECK, FOREIGN KEY) in addition to domain validation. [PROPOSED]
- Name SQL objects in `snake_case`, tables plural, foreign keys `<singular>_id`, indexes `idx_<table>_<columns>`. [PROPOSED]
- Use `timestamptz` for instants and `uuid` for ids. [PROPOSED]
- Index foreign keys and columns used in `WHERE`/`ORDER BY` of hot queries. [PROPOSED]
- Never build SQL by string concatenation; always bind parameters.
- Keep queries small and named after the use case need (`find_by_id`, `list_open_for_patient`). [PROPOSED]

## Repository adapter
```rust
// crates/adapters-postgres/src/appointment_repository.rs
pub struct PgAppointmentRepository { pool: PgPool }

#[async_trait::async_trait]
impl AppointmentRepository for PgAppointmentRepository {
    async fn find(&self, id: AppointmentId) -> Result<Option<Appointment>, RepositoryError> {
        let row = sqlx::query_as!(
            AppointmentRow,
            "SELECT id, starts_at, status FROM appointments WHERE id = $1",
            id.0
        )
        .fetch_optional(&self.pool)
        .await
        .map_err(RepositoryError::from)?;
        Ok(row.map(Appointment::from))
    }
}
```
Source: docs/decisions/phase-2-decisions.md (Postgres via sqlx, ports in application, adapters in `adapters-postgres`).

## Transactions
```rust
async fn cancel_and_release(&self, appt: &Appointment) -> Result<(), RepositoryError> {
    let mut tx = self.pool.begin().await?;
    sqlx::query!("UPDATE appointments SET status = 'canceled' WHERE id = $1", appt.id().0)
        .execute(&mut *tx).await?;
    sqlx::query!("UPDATE slots SET available = true WHERE appointment_id = $1", appt.id().0)
        .execute(&mut *tx).await?;
    tx.commit().await?;
    Ok(())
}
```
[PROPOSED]

## sqlx offline
| Situation | Command |
|---|---|
| Regenerate metadata | `cargo sqlx prepare --workspace` (needs `DATABASE_URL` and an up-to-date schema) |
| Verify metadata is current | `cargo sqlx prepare --workspace --check` |
| Build without a database | `SQLX_OFFLINE=true cargo build` |

[PROPOSED]

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
