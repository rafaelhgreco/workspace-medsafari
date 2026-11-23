# Structure Guide - Backend (Rust workspace, hexagonal, modules)

Applies the premise in `commons/project-structure-general.md` to the Rust crates: first by module, then by kind, one item per file.

## Quick rules
- Path template: `crates/<crate>/src/modules/<module>/<kind>/<name>.<kind>.rs`, for example `crates/application/src/modules/login_request/usecases/get_login_request.usecase.rs`.
- A module is a business capability (`login_request`, `appointments`, `health`), named in `snake_case` and spelled the same in every crate that has code for it. To find everything about a capability, search for its module name.
- A module's `mod.rs` is its public API: kind folders are private (`mod usecases;`) and only the items other code may use are re-exported with `pub use`. The compiler rejects any outside import of a kind folder (`E0603`).
- Inside a kind folder, file modules are private too (`mod login_request_repository;`) and are re-exported by that folder's `mod.rs`.
- Declare every file with `#[path = "<name>.<kind>.rs"]`, because a dot in a file name cannot be a module name. A missing declaration is a compile error.
- `lib.rs` contains only `pub mod modules;` and `pub mod shared;` (when the crate has them). `modules/mod.rs` contains only `pub mod <module>;` lines.
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
| `domain` | `value_objects/` | `.value_object.rs` [PROPOSED] | value objects |
| `domain` | `errors/` | `.error.rs` [PROPOSED] | the module's domain errors |
| `application` | `repositories/` | `.repository.rs` | repository ports (traits) and their error |
| `application` | `ports/` | `.port.rs` [PROPOSED] | other ports owned by the module |
| `application` | `usecases/` | `.usecase.rs` | use cases and their error |
| `adapters-http` | `controllers/` | `.controller.rs` | thin Axum handlers with `#[utoipa::path]` |
| `adapters-http` | `dtos/` | `.dto.rs` | request/response DTOs with `ToSchema` [PROPOSED] |
| `adapters-postgres` | `repositories/` | `.repository.rs` | `sqlx` implementations of the module's ports |
| `bootstrap` | (module root) | `<module>.module.rs` | wiring of the module: builds its use cases and router |

Outside `modules/`:
- `<crate>/src/shared/` holds cross-cutting items with the same kind folders (`application/src/shared/ports/clock.port.rs`); modules may depend on `shared`, `shared` depends on no module.
- Crate-level singletons stay as plain files at `src/`: `lib.rs`, `main.rs`, `router.rs`, `openapi.rs`, `config.rs` and the HTTP `ApiError` mapping (`error.rs`); a module's `From<ModuleError> for ApiError` lives in its controller file. [PROPOSED]
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

Initial module cut for the current backend (after the login/register merge; graphify snapshot of 2026-11-19; accepted 2026-11-23). The file-by-file mapping lives in the demand `refactor-backend-modules`.
| Module | Holds | Depends on |
|---|---|---|
| `health` | `AppVersion`, `VersionProvider`, `GetHealth`, health controller and DTO, `CargoVersion` | nothing |
| `auth` | access request, verification, signup, terms, session, logout, user; routes `/api/auth/*` | nothing |
| `progress` | attempts and progress sync; routes `/api/progress/*` | `auth` (through `SessionService`) |
| `shared` (per crate) | `Clock`, `PortError`, `SystemClock` | nothing |

Files that stay at the crate root: `settings.rs`, `config.rs`, `dotenv.rs`, `wiring.rs`, `router.rs`, `state.rs`, `openapi.rs`, `error.rs`, `json.rs`, `database.rs`, `pg_store.rs`, `client_ip.rs`, `cookie.rs`, `user_agent_label.rs`. Split `auth` only when a new flow justifies it: with today's dependencies a finer cut (`account`, `session`, `access`) produces cycles (`session -> access -> session`).

Source: layout, `__tests__` and `modules/` decisions from the project owner (2026-11-19 and 2026-11-23). The module mechanics (private kind folders and compiler-enforced boundaries, `#[path]` with dotted file names, `mockall` with the `mocks` feature across crates, `cargo fmt --check` over test files, `cargo clippy --all-targets -- -D warnings`, `cargo test`, both checks above) were verified on a proof workspace with `domain`, `application` and a stand-in adapter crate (cargo 1.97). `cargo nextest` and the `bootstrap` wiring were not exercised there. Items #17 to #22 of `knowledge/guides/GAPS.md` (modules in the adapters, `shared/`, cross-module rules, errors per module, per-module wiring) were accepted by the project owner on 2026-11-23. Items still marked [PROPOSED] extend the decision and need confirmation; see `GAPS.md`.

## Open conflicts
None. See `knowledge/guides/GAPS.md`.
