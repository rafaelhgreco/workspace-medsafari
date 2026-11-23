# Project Structure - General (file layout and test location)

Standing premise for every demand that creates or moves source files, in any repo. Loaded with the commons guides on every run.

## Quick rules
- Group code by module first, then by kind. A module is a business capability (`login_request`, `appointments`, `health`); inside it there is one folder per kind (`repositories/`, `usecases/`, `entities/`, ...). Never one folder that holds the use cases of several modules, and never a catch-all file such as `ports.rs`.
- Spell the module name the same in every crate that has code for it (`modules/login_request/` in `domain`, `application`, the adapters and `bootstrap`); searching for the name finds the whole capability.
- A module exposes only what its `mod.rs` re-exports. Modules use each other only through that public API and never in a cycle; code with no single owner goes to `<crate>/src/shared/`.
- Frontend: `features/<feature>/` is the module; there is no extra `modules/` folder.
- One item per file. A file holds one repository, one use case, one controller or one entity, plus the types that exist only for it (its error, its input/output).
- Name every file `<name>.<kind>.<ext>`: `login_request.repository.rs`, `login-request.service.ts`. `<name>` is the business concept, `<kind>` is the role.
- Use the same `<name>` across layers for the same concept (`login_request` in `entities/`, `repositories/`, `usecases/`, `controllers/`).
- Unit tests never live inside the source file. They live in a `__tests__/` subfolder of the folder that holds the code, with the same base name as the file under test.
- `__tests__/` contains only tests and test helpers. It never contains production code, and production code never imports from it.
- Integration tests and the architecture test keep their current homes (`crates/adapters-postgres/tests/`, `crates/bootstrap/tests/`); `__tests__/` is for unit tests only.
- A crate or app root file (`lib.rs`, `main.rs`, `app.ts`) only declares modules, re-exports or wires; it defines no business items.
- New code always follows this layout. Details per stack: `backend/structure-guide-backend.md`, `frontend/structure-guide-frontend.md`.

## Kinds and suffixes
| Kind | Suffix | Where (backend crate / frontend) |
|---|---|---|
| Repository (port) | `.repository` | `application` / - |
| Repository (implementation) | `.repository` | `adapters-postgres` / - |
| Use case | `.usecase` | `application` / - |
| Controller (HTTP handler) | `.controller` | `adapters-http` / - |
| Entity | `.entity` | `domain` / - |
| Other port (clock, id generator, notifier) | `.port` [PROPOSED] | `application` / - |
| Module wiring | `.module` | `bootstrap` / - |
| Value object | `.value_object` [PROPOSED] | `domain` / - |
| HTTP DTO | `.dto` [PROPOSED] | `adapters-http` / - |
| Component, service, model, guard, interceptor, pipe | `.component`, `.service`, `.model`, `.guard`, `.interceptor`, `.pipe` | - / `features/<feature>/...`, `core/`, `shared/` |

Rust file names use `snake_case` (`login_request.repository.rs`); TypeScript file names use `kebab-case` (`login-request.service.ts`). The dot-separated suffix is part of the file name, not of the Rust module name; see the backend guide for the `#[path]` mechanics.

## Tests next to the code, in `__tests__/`
```text
modules/login_request/
  repositories/
    mod.rs
    login_request.repository.rs
    __tests__/
      login_request.repository.test.rs    # Rust
  usecases/
    get_login_request.usecase.rs
    __tests__/
      get_login_request.usecase.test.rs
```
Frontend: `services/login-request.service.ts` is tested by `services/__tests__/login-request.service.spec.ts`.

- A test file name is the source file name plus `.test` (Rust) or `.spec` (TypeScript) before the extension.
- Tests of crate-level files (those that stay outside `modules/` and `shared/`) live in `<crate>/src/__tests__/<name>.test.rs`.
- Naming of the tests themselves does not change (`ac_<nn>_br_<nn>_<behavior>`, `it('AC-02 [BR-01] ...')`); see `testing-guide-unit-general.md`.
- Create the `__tests__/` file first (RED), then the source file; the test must fail for the right reason before any code exists.

## Modules
- Create a module when a task introduces a new business capability or aggregate; do not create one per use case, and do not park a new capability inside an existing module to save a folder.
- The tech spec (Turtle) names the module of every new file and lists every dependency between modules; the verification (Termite) checks that the code has no other edge and no cycle.
- The compiler enforces the boundary in Rust (kind folders are private to their module); in TypeScript the rule is checked in review and by lint.
- Paths per crate, `shared/`, crate-level files and the checks are in `backend/structure-guide-backend.md`.

## Existing code
- A task that changes an item still living in a legacy file (`ports.rs`, an inline `mod tests`) moves that item, and its tests, to the new layout (module, kind folder, `__tests__/`) in the same task. [PROPOSED]
- Migrating the rest of a legacy file is its own `refactor` demand; do not mix a bulk move with feature work. [PROPOSED]
- A move changes paths only: behavior, public names and test names stay the same, and the suite stays green before and after.

## Examples
```text
feat(application): add login request repository port
refactor(application): split ports.rs into repositories/ and ports/
refactor(application): move health use cases into modules/health
feat(domain): add login_request module
test(application): move unit tests to __tests__
```

Source: layout and `__tests__` decision from the project owner (2026-11-19); the `modules/` decision is from 2026-11-23; the Rust mechanics were checked by compiling proof workspaces (cargo 1.97: `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`). Items marked [PROPOSED] extend that decision and need confirmation; see `knowledge/guides/GAPS.md`.

## Open conflicts
None.
