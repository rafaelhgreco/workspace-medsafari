# Testing Guide - Postgres integration (testcontainers-rs)

## Quick rules
- Use integration tests only for tasks that touch `crates/adapters-postgres/` or `migrations/`; they need Docker.
- Put them in `crates/adapters-postgres/tests/`; run them with `cargo nextest run --workspace --profile integration`.
- Start a real Postgres with `testcontainers-rs` (`testcontainers-modules` Postgres); never mock the database here.
- Share one container per test binary through a lazily initialized static (`tokio::sync::OnceCell`) or fixture. See Open conflicts about nextest.
- Apply the real migrations with `sqlx::migrate!` once per container.
- Isolate tests: create a database per test from a migrated template database; use transaction rollback only for functions that take an executor. [PROPOSED]
- Build test data with builders; give every builder sensible defaults. [PROPOSED]
- Test the adapter contract: row-to-domain mapping, constraints (unique, FK, check), queries (filters, ordering), transactions (commit and rollback).
- Do NOT test business rules here; they are unit tests in domain/application.
- Check Docker first (`docker info`); if it is unavailable, stop and report instead of skipping.
- Keep one file per adapter (for example `appointment_repository.rs`) so each is its own test binary. [PROPOSED]
- Name tests `ac_<nn>_br_<nn>_<behavior>` when they cover an AC/BR; otherwise by the contract they check. [PROPOSED]

## Shared container and migrations
```rust
use testcontainers_modules::{postgres::Postgres, testcontainers::{runners::AsyncRunner, ContainerAsync}};
use tokio::sync::OnceCell;

struct Db { _container: ContainerAsync<Postgres>, admin: PgPool, url_base: String }
static DB: OnceCell<Db> = OnceCell::const_new();

async fn db() -> &'static Db {
    DB.get_or_init(|| async {
        let container = Postgres::default().start().await.expect("start postgres");
        let port = container.get_host_port_ipv4(5432).await.expect("port");
        let url_base = format!("postgres://postgres:postgres@127.0.0.1:{port}");
        let admin = PgPool::connect(&format!("{url_base}/postgres")).await.expect("connect");
        sqlx::query("CREATE DATABASE template_app").execute(&admin).await.expect("template");
        let tpl = PgPool::connect(&format!("{url_base}/template_app")).await.expect("connect");
        sqlx::migrate!("../../migrations").run(&tpl).await.expect("migrate");
        tpl.close().await;
        Db { _container: container, admin, url_base }
    })
    .await
}

async fn fresh_pool() -> PgPool {
    let db = db().await;
    let name = format!("t_{}", uuid::Uuid::new_v4().simple());
    sqlx::query(&format!("CREATE DATABASE {name} TEMPLATE template_app")).execute(&db.admin).await.expect("create");
    PgPool::connect(&format!("{}/{name}", db.url_base)).await.expect("connect")
}
```
[PROPOSED] (the one-container-per-binary requirement is a decision; the code is a proposal). The migrations path is relative to the crate: `crates/adapters-postgres` to `../../migrations`.

## A contract test
```rust
#[tokio::test]
async fn ac_03_br_02_cancel_releases_the_slot() {
    // Arrange
    let pool = fresh_pool().await;
    let repo = PgAppointmentRepository::new(pool.clone());
    let appt = AppointmentBuilder::default().scheduled().insert(&pool).await;
    // Act
    repo.cancel_and_release(&appt.canceled()).await.unwrap();
    // Assert
    let slot = SlotRow::by_appointment(&pool, appt.id()).await;
    assert!(slot.available);
}
```

## What to test in the adapter
| Test | Do not test |
|---|---|
| Mapping row <-> domain, including NULLs and enums | Business rules (24h window, etc.) |
| Constraints (unique, FK, check) become typed errors | HTTP concerns |
| Query filters, ordering, pagination | Mocked ports |
| Atomicity: failure in a transaction rolls everything back | Framework internals |

## Open conflicts
- **OC-01 nextest vs one container per binary.** The decision asks for one container per test binary reused through `OnceCell`, and for `cargo nextest` profiles. nextest runs every test in its own process, so a process-wide static is NOT shared across tests: each test would start its own container (slow). Options: (a) a nextest setup script that starts one Postgres per run and exports its URL; (b) run the integration profile with `cargo test` instead of nextest; (c) accept one container per test. Not chosen here; needs a human decision. See `knowledge/guides/GAPS.md`.
