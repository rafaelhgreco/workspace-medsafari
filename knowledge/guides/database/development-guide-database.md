# Development Guide - Database (migrations)

## Quick rules
- Manage the schema only through `sqlx migrate` migrations in `migrations/`; never edit a database by hand.
- Create reversible migrations: `sqlx migrate add -r <name>` produces an `.up.sql` and a `.down.sql`. [PROPOSED]
- Name migrations `<verb>_<object>` in snake_case (`create_appointments`, `add_canceled_at_to_appointments`); sqlx adds the timestamp prefix. [PROPOSED]
- Never edit a migration that was applied or merged; add a new one.
- Keep one concern per migration; keep the `.down.sql` truly inverse or document why it cannot be.
- Make schema changes backward compatible with the running code: expand, deploy, contract (see below). [PROPOSED]
- Add NOT NULL columns in steps: nullable add, backfill, then constraint. [PROPOSED]
- Create indexes on large tables with `CREATE INDEX CONCURRENTLY` in a migration that opts out of the transaction. [PROPOSED]
- Regenerate `.sqlx/` metadata (`cargo sqlx prepare --workspace`) in the same task as the migration.
- A task that touches `migrations/` or `crates/adapters-postgres/` is `unit+integration` and needs Docker for its integration test.
- Apply migrations in tests with `sqlx::migrate!` (see testcontainers guide); never replay SQL by hand.
- Test the down migration locally at least once before merging. [PROPOSED]

## Commands
| Purpose | Command |
|---|---|
| Add reversible migration | `sqlx migrate add -r <name>` |
| Apply | `sqlx migrate run` |
| Revert last | `sqlx migrate revert` |
| Refresh offline metadata | `cargo sqlx prepare --workspace` |

Source: docs/decisions/phase-2-decisions.md (`sqlx migrate`, sqlx-cli); reversibility and naming are [PROPOSED].

## Expand / contract
1. Expand: add the new column/table (nullable or with default). Old code keeps working.
2. Migrate data and switch the code to the new shape.
3. Contract: in a later migration, drop the old column/constraint.

[PROPOSED]

## Migration example
```sql
-- 20261113120000_add_canceled_at_to_appointments.up.sql
ALTER TABLE appointments ADD COLUMN canceled_at timestamptz NULL;

-- 20261113120000_add_canceled_at_to_appointments.down.sql
ALTER TABLE appointments DROP COLUMN canceled_at;
```

## Task checklist
- [ ] Up and down migrations written; down reverts the up.
- [ ] `.sqlx/` metadata regenerated; `SQLX_OFFLINE=true cargo build` works.
- [ ] Integration test applies migrations via `sqlx::migrate!` and covers the new schema behavior.
- [ ] `unit+integration` profiles green; Docker available.

## Open conflicts
None (no team documents available yet). See `knowledge/guides/GAPS.md`.
