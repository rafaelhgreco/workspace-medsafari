# Structure Guide - Backend (Rust workspace, hexagonal, modules)

Applies the premise in `commons/project-structure-general.md` to the Rust crates: first by module, then by kind, one item per file.

## Quick rules
- Path template: `crates/<crate>/src/modules/<module>/<kind>/<name>.<kind>.rs`, for example `crates/application/src/modules/login_request/usecases/get_login_request.usecase.rs`.
- A module is a business capability (`login_request`, `appointments`, `health`), named in `snake_case` and spelled the same in every crate that has code for it. To find everything about a capability, search for its module name.
- A module's `mod.rs` is its public API: kind folders are private (`mod usecases;`) and only the items other code may use are re-exported with `pub use`. The compiler rejects any outside import of a kind folder (`E0603`).
- Inside a kind folder, file modules are private too (`mod login_request_repository;`) and are re-exported by that folder's `mod.rs`.
- Declare every file with `#[path = "<name>.<kind>.rs"]`, because a dot in a file name cannot be a module name. A missing declaration is a compile error.
- `lib.rs` declares `modules` and `shared` (when the crate has them) and, besides that, only what is public from root files (for example `pub use settings::AuthSettings;`, the `bootstrap` entry points). No type is re-exported from a module at the crate root. `modules/mod.rs` contains only `pub mod <module>;` lines.
- Never create `ports.rs`, `usecases.rs`, `repositories.rs`, `utils.rs` or any file that collects several items; never put use cases of different modules in one folder.
- One item per file; a repository port and the error only it returns live in the same `.repository.rs` file. File name, type name and module name stay aligned: `login_request.repository.rs` holds `LoginRequestRepository`.
- Tests of crate-level files (`config.rs`, `router.rs`, `settings.rs`, ...) live in `<crate>/src/__tests__/<name>.test.rs` and are wired the same way.
- Unit tests go in `__tests__/<name>.<kind>.test.rs` inside the kind folder and are wired from the source file; no `mod tests { ... }` with a body inside a source file. Test files use `use super::*;` and see private items of the file under test.
- Mockable ports keep `#[cfg_attr(any(test, feature = "mocks"), mockall::automock)]` and the module's `mod.rs` re-exports the generated mock under `#[cfg(any(test, feature = "mocks"))]`, so other modules and crates can mock the port without touching internals.
- A module may use another module of the same crate only through that module's public API, never in a cycle. Code needed by two or more modules that has no natural owner goes to `<crate>/src/shared/`.
- Errors belong to the module that raises them (`errors/<name>.error.rs` or inside the use case or repository file); do not grow one crate-wide error enum that every module edits.
- Add a module in the same task that introduces its first item; create the folder in every crate the task touches, not in all crates.

## Where each kind lives
| Crate | Folder (under `modules/<module>/`) | File suffix | Holds |
|---|---|---|---|
| `domain` | `entities/` | `.entity.rs` | entities and aggregates |
| `domain` | `value_objects/` | `.value_object.rs` | value objects |
| `domain` | `errors/` | `.error.rs` | the module's domain errors |
| `application` | `repositories/` | `.repository.rs` | repository ports (traits) and their error |
| `application` | `ports/` | `.port.rs` | other ports owned by the module |
| `application` | `usecases/` | `.usecase.rs` | use cases and their error |
| `adapters-http` | `controllers/` | `.controller.rs` | thin Axum handlers with `#[utoipa::path]` |
| `adapters-http` | `dtos/` | `.dto.rs` | request/response DTOs with `ToSchema` |
| `adapters-postgres` | `repositories/` | `.repository.rs` | `sqlx` implementations of the module's ports |
| `bootstrap` | (module root) | `<module>.module.rs` | wiring of the module: builds its use cases and router |

Outside `modules/`:
- `<crate>/src/shared/` holds cross-cutting items with the same kind folders (`application/src/shared/ports/clock.port.rs`); modules may depend on `shared`, `shared` depends on no module.
- Crate-level files stay as plain files at `src/` (full list in "Initial module cut"). In `adapters-http`, `error.rs` keeps the `From<...Error> for ApiError` conversions; moving each one into the module's controller file is still open. [PROPOSED]
- Concrete port implementations that exist only in `bootstrap` live in the module as `providers/<name>.provider.rs`.

## Layout example
```text
crates/domain/src/
  lib.rs
  modules/
    mod.rs
    login_request/
      mod.rs
      entities/
        mod.rs
        login_request.entity.rs
        __tests__/
          login_request.entity.test.rs
crates/application/src/
  lib.rs
  shared/
    mod.rs
    ports/
      mod.rs
      clock.port.rs
  modules/
    mod.rs
    login_request/
      mod.rs
      repositories/
        mod.rs
        login_request.repository.rs
      usecases/
        mod.rs
        get_login_request.usecase.rs
        __tests__/
          get_login_request.usecase.test.rs
    audit/
      mod.rs
      usecases/
        mod.rs
        record_login_lookup.usecase.rs
        __tests__/
          record_login_lookup.usecase.test.rs
```

## Mechanics
```rust
// crates/application/src/lib.rs
pub mod modules;
pub mod shared;

// crates/application/src/modules/mod.rs
pub mod audit;
pub mod login_request;
```
```rust
// crates/application/src/modules/login_request/mod.rs  (the module's public API)
mod repositories;
mod usecases;

pub use repositories::{LoginRequestRepository, RepositoryError};
#[cfg(any(test, feature = "mocks"))]
pub use repositories::MockLoginRequestRepository;
pub use usecases::GetLoginRequest;
```
```rust
// crates/application/src/modules/login_request/repositories/mod.rs
#[path = "login_request.repository.rs"]
mod login_request_repository;

pub use login_request_repository::{LoginRequestRepository, RepositoryError};
#[cfg(any(test, feature = "mocks"))]
pub use login_request_repository::MockLoginRequestRepository;
```
```rust
// crates/application/src/modules/login_request/repositories/login_request.repository.rs
use domain::modules::login_request::{LoginRequest, LoginRequestId};

#[derive(Debug, thiserror::Error)]
pub enum RepositoryError {
    #[error("storage failure")]
    Storage,
}

#[cfg_attr(any(test, feature = "mocks"), mockall::automock)]
#[async_trait::async_trait]
pub trait LoginRequestRepository: Send + Sync {
    async fn find(&self, id: LoginRequestId) -> Result<Option<LoginRequest>, RepositoryError>;
}
```
```rust
// crates/application/src/modules/login_request/usecases/get_login_request.usecase.rs (tail)
// files of the same module reach siblings by the full path, which stays legal inside the module
use crate::modules::login_request::repositories::{LoginRequestRepository, RepositoryError};

#[cfg(test)]
#[path = "__tests__/get_login_request.usecase.test.rs"]
mod tests;
```
```rust
// crates/application/src/modules/audit/usecases/record_login_lookup.usecase.rs (head)
// another module: public API of login_request and the shared kernel only
use crate::modules::login_request::GetLoginRequest;
use crate::shared::Clock;
```
The `#[path]` on `mod tests;` is resolved from the folder of the source file, so `__tests__/` sits next to it. Test paths in the runner output become `modules::login_request::usecases::get_login_request_usecase::tests::<test_name>`; the nextest `unit` filters (package and kind) need no change.

## Module boundaries
Verified on a proof workspace:
- `use crate::modules::login_request::repositories::...` written in module `audit` fails with `module repositories is private`.
- `use application::modules::login_request::usecases::...` written in another crate fails the same way.
- Cross-crate tests keep working: the consumer crate enables `application = { path = "...", features = ["mocks"] }` in `[dev-dependencies]` and imports `application::modules::login_request::MockLoginRequestRepository`.

When a module needs something from another module, first check that the item is re-exported by the other module's `mod.rs`; if it is not, the owner decides to export it (a task in the owner module), the consumer never reaches around it.

## Checks for VERIFY
Run from the workspace root (`backend/`). Both rely on shell only.
```bash
# 1. orphan test files: a .test.rs that no source file declares never compiles. Empty output = ok.
for f in $(find crates -path '*/__tests__/*.test.rs'); do
  dir=$(dirname "$(dirname "$f")"); base=$(basename "$f" .test.rs)
  grep -q "__tests__/$base.test.rs" "$dir/$base.rs" || echo "ORPHAN: $f"
done

# 2. module edges: one line per "<crate>: <module> -> <other module>". Every edge must be declared in the tech spec and the graph must have no cycle.
for crate in $(ls crates); do
  for m in crates/$crate/src/modules/*/; do a=$(basename "$m")
    grep -rhoE "(crate|domain|application)::modules::[a-z_]+" "$m" --include=*.rs 2>/dev/null \
      | sed -E 's/.*modules::([a-z_]+)/\1/' | sort -u | while read -r b; do [ "$b" != "$a" ] && echo "$crate: $a -> $b"; done
  done
done | sort -u
```
A non-empty result of check 1 is a verification failure. An undeclared edge or a cycle in check 2 is a verification failure.

## Migrating legacy code into modules
1. Run the unit profile and keep `cargo nextest list --profile unit` as the baseline.
2. Pick the module for each item (table below); create `modules/<module>/` with its `mod.rs` and the kind folders in each crate.
3. Move one item per file with the tests that cover it into `__tests__/`; keep the public path stable through re-exports in `lib.rs` until every caller is moved.
4. Delete the legacy file or folder once empty; the unit profile must list the same tests as the baseline, only under new module paths.
5. Commit as `refactor(<crate>): ...`; a move commit changes no behavior.

Result of the migration (branch `refactor/backend-modules` in `repos/medsafari`, 2026-11-23; four commits: `health`, `progress`, `auth` + `shared`, architecture guard). Behavior unchanged: the unit name list equals the baseline plus 5 guard tests, `unit` and `integration` profiles green, OpenAPI JSON identical.
| Module | Holds | Depends on |
|---|---|---|
| `health` | `AppVersion`, `HealthError`, `VersionProvider`, `GetHealth`, health controller and DTO, `CargoVersion` | nothing |
| `auth` | access request, verification, signup, terms, session, logout, user, `require_session`, `AuthError`; routes `/api/auth/*` | nothing |
| `progress` | attempts and progress sync; routes `/api/progress/*` | `auth` (`Principal`, `UserId`) |
| `shared` (`application`, `bootstrap`) | `Clock`, `PortError`, `SystemClock` | nothing |

Files that stay at the crate root:
- `application`: `settings.rs`.
- `adapters-http`: `client_ip.rs`, `cookie.rs`, `error.rs`, `json.rs`, `openapi.rs`, `router.rs`, `state.rs`, `test_support.rs`, `user_agent_label.rs`.
- `adapters-postgres`: `database.rs`, `error.rs`, `pg_store.rs`.
- `bootstrap`: `config.rs`, `dotenv.rs`, `wiring.rs`, `main.rs`, `bin/`.
- Their tests stay in `src/__tests__/`. `domain` has no root files besides `lib.rs`.

Shape that worked:
- Each `modules/<module>/mod.rs` re-exports every public item of its kind folders. `adapters-http` re-exports controllers and DTOs with `pub use <kind>::*`, because `utoipa` generates `__path_*` items. `adapters-postgres` exports nothing: the repositories are `impl <Port> for PgStore`.
- `bootstrap`: `<module>.module.rs` exposes `build(...)` and a struct with the module's use cases; `wiring.rs` composes `auth`, `progress` and `health`. Each module builds its own providers.
- `DomainError` became `HealthError` (domain/health) and `AuthError` (domain/auth).
- A test that needs two modules lives in the module that is allowed to depend on the other. Examples: `ac_15_br_01_ids_are_distinct_types_with_value_equality` (uses `UserId`, `SessionId`, `AttemptId`) is in `progress`, and `ac_21_br_11_system_clock_and_id_generator_produce_fresh_values` is in `auth`, because `shared` and `auth` must not depend on `progress`.
- `crates/bootstrap/tests/architecture.rs` runs the module checks: no kind folder or undeclared file at a crate root, only `progress -> auth` between modules, no cycle, `shared` depends on no module.

Split `auth` only when a new flow justifies it: with today's dependencies a finer cut (`account`, `session`, `access`) produces cycles (`session -> access -> session`).

Source: layout, `__tests__` and `modules/` decisions from the project owner (2026-11-19 and 2026-11-23). Mechanics verified on a proof workspace and then on the real backend: `cargo nextest` profiles `unit` (filters by package, no change needed) and `integration`, `cargo fmt --check`, `cargo clippy --workspace --all-targets -- -D warnings`, `E0603` on an import of another module's kind folder, both checks above, per-module wiring in `bootstrap`. Items #15 and #22 of `knowledge/guides/GAPS.md` are confirmed by this run. Items still marked [PROPOSED] extend the decision and need confirmation.

## Open conflicts
None. See `knowledge/guides/GAPS.md`.
