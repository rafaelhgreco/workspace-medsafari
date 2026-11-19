# Structure Guide - Backend (Rust workspace, hexagonal)

Applies the premise in `commons/project-structure-general.md` to the Rust crates.

## Quick rules
- Each crate groups its code in kind folders under `src/`; each kind folder has a `mod.rs`.
- File name: `<name>.<kind>.rs` (for example `entities/login_request.entity.rs`). Module name: `<name>_<kind>` (`login_request_entity`).
- Declare every file in its folder's `mod.rs` with `#[path = "<name>.<kind>.rs"]`, because a dot in a file name cannot be a module name. A missing declaration is a compile error.
- Re-export the public items from `mod.rs` so callers write `crate::repositories::LoginRequestRepository`, not the long module path.
- `lib.rs` contains only `pub mod` lines (and re-exports). No traits, structs or tests in it.
- Never create `ports.rs`, `repositories.rs`, `utils.rs` or any file that collects several unrelated items.
- A repository port and the error type only it returns live in the same `.repository.rs` file.
- Keep the file name, the trait/struct name and the module name aligned: `login_request.repository.rs` holds `LoginRequestRepository`; `get_login_request.usecase.rs` holds `GetLoginRequest`.
- Unit tests go in `__tests__/<name>.<kind>.test.rs` and are wired from the source file; no `mod tests { ... }` with a body inside a source file.
- Test files use `use super::*;` and see private items of the file under test; they reach other files through `crate::...`.
- Mockable ports keep `#[cfg_attr(any(test, feature = "mocks"), mockall::automock)]` on the trait; the generated `Mock...` lives in the same module and is imported by tests of other files through `crate::<kind>::<module>::Mock...`.

## Where each kind lives
| Crate | Folder | File suffix | Holds |
|---|---|---|---|
| `domain` | `entities/` | `.entity.rs` | entities and aggregates |
| `domain` | `value_objects/` | `.value_object.rs` [PROPOSED] | value objects |
| `domain` | `errors/` | `.error.rs` [PROPOSED] | `DomainError` and variants |
| `application` | `repositories/` | `.repository.rs` | repository ports (traits) and their error |
| `application` | `ports/` | `.port.rs` [PROPOSED] | other ports: `Clock`, id generator, notifier |
| `application` | `usecases/` | `.usecase.rs` | use cases and their error |
| `adapters-http` | `controllers/` | `.controller.rs` | thin Axum handlers with `#[utoipa::path]` |
| `adapters-http` | `dtos/` | `.dto.rs` [PROPOSED] | request/response DTOs with `ToSchema` |
| `adapters-postgres` | `repositories/` | `.repository.rs` | `sqlx` implementations of the application ports |
| `bootstrap` | `src/` | plain `snake_case.rs` | configuration and wiring |

Crate-level singletons stay as plain files at `src/`: `lib.rs`, `main.rs`, `router.rs`, `openapi.rs`, `config.rs`, and the HTTP `ApiError` mapping (`error.rs`). [PROPOSED]

## Layout example
```text
crates/application/src/
  lib.rs
  repositories/
    mod.rs
    login_request.repository.rs
    __tests__/
      login_request.repository.test.rs
  ports/
    mod.rs
    clock.port.rs
    __tests__/
      clock.port.test.rs
  usecases/
    mod.rs
    get_login_request.usecase.rs
    __tests__/
      get_login_request.usecase.test.rs
```

## Mechanics
```rust
// crates/application/src/lib.rs
pub mod ports;
pub mod repositories;
pub mod usecases;
```
```rust
// crates/application/src/repositories/mod.rs
#[path = "login_request.repository.rs"]
pub mod login_request_repository;

pub use login_request_repository::{LoginRequestRepository, RepositoryError};
```
```rust
// crates/application/src/repositories/login_request.repository.rs
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

#[cfg(test)]
#[path = "__tests__/login_request.repository.test.rs"]
mod tests;
```
```rust
// crates/application/src/usecases/__tests__/get_login_request.usecase.test.rs
use super::*;
use crate::repositories::login_request_repository::MockLoginRequestRepository;

#[tokio::test]
async fn ac_03_br_01_returns_repository_value() {
    // Arrange
    let mut repo = MockLoginRequestRepository::new();
    repo.expect_find().returning(|_| Ok(Some(login_request())));
    let use_case = GetLoginRequest::new(Arc::new(repo));

    // Act
    let result = use_case.execute(login_request_id()).await;

    // Assert
    assert!(matches!(result, Ok(Some(_))));
}
```
The `#[path]` attribute on `mod tests;` is resolved from the folder of the source file, so `__tests__/` must sit next to it. Test paths in nextest output become `repositories::login_request_repository::tests::<test_name>`, so the `unit` profile filters in `.config/nextest.toml` (by package and kind) need no change.

## Orphan test files
A `.test.rs` file that no source file declares is never compiled, so its tests silently do not run. Check before every commit and in VERIFY:
```bash
# prints one line per test file not wired into its source file; empty output = ok
for f in $(find crates -path '*/src/*/__tests__/*.test.rs'); do
  dir=$(dirname "$(dirname "$f")"); base=$(basename "$f" .test.rs)
  grep -q "__tests__/$base.test.rs" "$dir/$base.rs" || echo "ORPHAN: $f"
done
```
Run it from the workspace root (`backend/`). A non-empty result is a verification failure.

## Migrating a legacy file (for example `ports.rs`)
1. Run the unit profile and keep the output as the baseline.
2. Create the kind folder and its `mod.rs`; move one item per file, with the tests that cover it into `__tests__/`.
3. Keep the public path stable through re-exports in `mod.rs` and `lib.rs`, so no caller changes in the same step.
4. Delete the legacy file once empty; the unit profile must list the same tests as the baseline, only under new module paths.
5. Commit as `refactor(<crate>): ...`; a move commit changes no behavior.

Source: layout and `__tests__` decision from the project owner (2026-11-19); the `#[path]` mechanics, `mockall` with the `mocks` feature, `cargo fmt --check` over test files and `cargo clippy --all-targets -- -D warnings` were verified on a proof workspace (cargo 1.97). `cargo nextest` was not run there; module-path filtering is [PROPOSED] until confirmed with `cargo nextest list --profile unit`. Items marked [PROPOSED] extend the decision.

## Open conflicts
None. See `knowledge/guides/GAPS.md`.
