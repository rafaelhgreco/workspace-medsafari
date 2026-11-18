# Refatorar backend Rust para arquitetura hexagonal Implementation Plan

> Plan produced by Termite; tasks are executed by step-03 of the termite skill.

**Goal:** Converter o backend monolítico (`main.rs`) em um workspace hexagonal com o contrato de `GET /api/health` preservado, OpenAPI publicado, erros em problem+json e ferramental (nextest `unit`, lefthook) ativo.

**Architecture:** Workspace `backend/crates/{domain, application, adapters-http, bootstrap}` com `domain <- application <- adapters-http <- bootstrap`. A porta `VersionProvider` vive em `application`; `CargoVersion` a implementa em `bootstrap`; o handler HTTP é fino e traduz erros para problem+json.

**Tech Stack:** Rust edition 2024, axum, tokio, serde, thiserror, utoipa, mockall, cargo-nextest, lefthook. `async-trait`, `sqlx`, `tracing` e `tower-http` apenas declarados em `[workspace.dependencies]`.

**Spec:** `artifacts/active/refatorar-backend-hexagonal/delivery/02-tech-spec.md` (histórias em `delivery/01-functional-stories.md`)

## Global Constraints

- Repo `repos/medsafari`, branch `refactor/backend-hexagonal`; todos os comandos rodam em `repos/medsafari/backend` (workspace root).
- Contrato preservado: `GET /api/health` -> 200 `{"status":"ok","version":"<CARGO_PKG_VERSION>"}`; escuta em `127.0.0.1:3000` (BR-01).
- Versão `0.1.0` vem de `[workspace.package]`; binário continua `backend` (INF-08).
- Regra de dependência: `domain` sem dependências internas; `application` -> `domain`; `adapters-http` -> `application`, `domain`; `bootstrap` -> todos (BR-02, BR-03).
- Sem `unwrap`/`expect` fora de testes e `bootstrap`; sem `#[allow]` sem comentário do motivo.
- Nomes de teste: `ac_<nn>_br_<nn>_<behavior>`; testes unitários ao lado do código em `#[cfg(test)] mod tests`, exceto o teste de arquitetura.
- Sem comentários com ids BR/ST/AC no código; comentar só o porquê.
- Fora de escopo: `adapters-postgres`, migrations, perfil `integration`, middlewares, autenticação, frontend (BR-11). Nenhum item usa Docker.
- Verificação padrão de cada tarefa: `cargo fmt --check`, `cargo clippy --workspace -- -D warnings`, `cargo nextest run --workspace --profile unit` (a partir da Task 1).
- Commits: Conventional, com `LEFTHOOK=0`.

## Review Focus

- `VersionProvider` devolve versão vazia: nunca vira 200 com versão vazia (`AppVersion` rejeita; a resposta é 500 problem+json). Teste na Task 2 e na Task 4.
- Falha da porta: o corpo do 500 não contém o texto da causa interna. Teste na Task 4.
- `POST /api/health` e rota inexistente: o comportamento atual do axum (405 e 404) se mantém. Testes na Task 4.
- O documento OpenAPI contém `openapi` 3.x, o path `/api/health` e os schemas `HealthResponse` e `Problem`. Teste na Task 4.
- O teste de arquitetura não passa vazio: deve falhar se uma dependência proibida existir. Verificação na Task 6 (RED com dependência proibida temporária).

## File Structure

```text
backend/Cargo.toml                       # [workspace] + [workspace.package] + [workspace.dependencies]
backend/.config/nextest.toml             # perfil unit
backend/crates/domain/                   # AppVersion, DomainError
backend/crates/application/              # VersionProvider, VersionError, GetHealth, Health, GetHealthError
backend/crates/adapters-http/            # router, health handler, HealthResponse, Problem, ApiError, ApiDoc
backend/crates/bootstrap/                # CargoVersion, LISTEN_ADDR, build_router, main (bin "backend"); tests/architecture.rs
lefthook.yml                             # raiz do repo medsafari (INF-11)
```

---

### Task 1: Workspace, dependências e perfil nextest `unit`
- commit: 1875a03
- layer: bootstrap
- repo: medsafari
- depends_on: []
- covers: AC-09, AC-12, AC-13, BR-02, BR-08, BR-10, BR-11
- test_scope: unit
- verify: `cd repos/medsafari/backend && cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo nextest list --profile unit && cargo nextest run --workspace --profile unit`
- commit: build(backend): convert to cargo workspace with nextest unit profile

**Files:**
- Modify: `backend/Cargo.toml` (vira workspace virtual)
- Create: `backend/.config/nextest.toml`, `backend/crates/{domain,application,adapters-http}/Cargo.toml` + `src/lib.rs` vazios, `backend/crates/bootstrap/Cargo.toml`
- Move: `backend/src/main.rs` -> `backend/crates/bootstrap/src/main.rs` (conteúdo e testes intactos; reescrito na Task 5)

**Interfaces:**
- Produces: workspace `members = ["crates/*"]`, `resolver = "3"`, `[workspace.package] edition = "2024", version = "0.1.0"`; `[workspace.dependencies]` com `axum`, `tokio`, `serde`, `thiserror`, `async-trait`, `utoipa`, `sqlx` (`default-features = false`), `mockall`, `tracing`, `tower-http`, `tower`, `http-body-util`, `serde_json` e os quatro crates internos por `path`. Versões: as já existentes no `Cargo.toml` atual para `axum`, `tokio`, `serde`, `mockall`, `tower`, `http-body-util`, `serde_json`; as demais, a última estável resolvida na hora e fixada no `Cargo.lock`. Bootstrap tem `[[bin]] name = "backend"`.

- [x] **Step 1: Write the failing check** - `cargo nextest list --profile unit` (ainda sem `.config/nextest.toml`).
- [x] **Step 2: Run it** - Expected: erro de perfil `unit` inexistente.
- [x] **Step 3: Implement** o workspace e `nextest.toml` com `[profile.unit]` e `default-filter = "not (package(adapters-postgres) and kind(test))"`; usar `workspace = true` nas dependências de cada membro; `sqlx`, `tracing`, `tower-http`, `async-trait` ficam só no workspace (INF-09).
- [x] **Step 4: Run** `cargo nextest list --profile unit` lista os 2 testes antigos e `cargo nextest run --workspace --profile unit` passa; conferir `cargo build -p bootstrap` gerando o binário `backend`.
- [x] **Step 5: Commit**

---

### Task 2: Domínio (`AppVersion`)
- commit: 912c1a8
- layer: domain
- repo: medsafari
- depends_on: [1]
- covers: AC-04, BR-03
- test_scope: unit
- verify: `cd repos/medsafari/backend && cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo nextest run -p domain --profile unit`
- commit: feat(domain): add AppVersion value object

**Files:** `backend/crates/domain/src/lib.rs` (+ `Cargo.toml` com apenas `thiserror`).

**Interfaces:**
- Produces: `pub struct AppVersion` (`Debug, Clone, PartialEq, Eq`); `AppVersion::new(value: impl Into<String>) -> Result<AppVersion, DomainError>`; `fn as_str(&self) -> &str`; `pub enum DomainError { EmptyVersion }` (`thiserror`).

- [x] **Step 1: Write failing tests** `ac_04_br_03_app_version_accepts_non_empty_text` (`new("1.2.3")?.as_str() == "1.2.3"`) e `ac_04_br_03_app_version_rejects_empty_text` (`new("") == Err(DomainError::EmptyVersion)`; vale também para só espaços).
- [x] **Step 2: Run** `cargo nextest run -p domain --profile unit` -> FAIL (tipos não definidos).
- [x] **Step 3: Implement** as assinaturas acima; nenhuma dependência além de `thiserror`.
- [x] **Step 4: Run** -> PASS.
- [x] **Step 5: Commit**

---

### Task 3: Aplicação (porta e caso de uso)
- commit: ec3cd65
- layer: application
- repo: medsafari
- depends_on: [2]
- covers: AC-01, AC-03, AC-05, BR-04, BR-05, BR-08
- test_scope: unit
- verify: `cd repos/medsafari/backend && cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo nextest run -p application --profile unit`
- commit: feat(application): add GetHealth use case and VersionProvider port

**Files:** `backend/crates/application/src/lib.rs` (+ `Cargo.toml`: `domain`, `thiserror`, `mockall` opcional atrás da feature `mocks`, `mockall` em dev-dependencies).

**Interfaces:**
- Consumes: `domain::{AppVersion, DomainError}`.
- Produces:
  - `pub trait VersionProvider: Send + Sync { fn version(&self) -> Result<AppVersion, VersionError>; }` com `#[cfg_attr(any(test, feature = "mocks"), mockall::automock)]`.
  - `pub enum VersionError { Unavailable(String), Invalid(#[from] DomainError) }`.
  - `pub enum HealthStatus { Ok }`; `pub struct Health { pub status: HealthStatus, pub version: AppVersion }`.
  - `pub struct GetHealth`; `GetHealth::new(provider: Arc<dyn VersionProvider>) -> Self`; `fn execute(&self) -> Result<Health, GetHealthError>`.
  - `pub enum GetHealthError { Version(#[from] VersionError) }`.

- [x] **Step 1: Write failing tests** com `MockVersionProvider`: `ac_05_br_04_returns_version_from_replaced_port` (mock devolve `AppVersion::new("1.2.3")`; `execute()` -> `Health{Ok, "1.2.3"}`; `times(1)`), `ac_01_br_01_reports_status_ok` e `ac_03_br_05_propagates_version_failure` (mock devolve `VersionError::Unavailable("x")`; `execute()` é `Err(GetHealthError::Version(_))`).
- [x] **Step 2: Run** `cargo nextest run -p application --profile unit` -> FAIL.
- [x] **Step 3: Implement** as assinaturas acima.
- [x] **Step 4: Run** -> PASS.
- [x] **Step 5: Commit**

---

### Task 4: Adaptador HTTP (handler, problem+json, OpenAPI)
- commit: 87add74
- layer: adapters-http
- repo: medsafari
- depends_on: [3]
- covers: AC-01, AC-03, AC-07, AC-08, BR-01, BR-05, BR-06
- test_scope: unit
- verify: `cd repos/medsafari/backend && cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo nextest run -p adapters-http --profile unit`
- commit: feat(adapters-http): expose health, problem+json errors and OpenAPI document

**Files:** `backend/crates/adapters-http/src/{lib.rs,health.rs,error.rs,openapi.rs}` (+ `Cargo.toml`: `application`, `domain`, `axum`, `serde`, `utoipa`; dev: `application` com feature `mocks`, `tower`, `http-body-util`, `serde_json`, `tokio`).

**Interfaces:**
- Consumes: `application::{GetHealth, GetHealthError, MockVersionProvider}`.
- Produces:
  - `pub fn router(use_case: Arc<GetHealth>) -> Router` com `GET /api/health` e `GET /api-docs/openapi.json`.
  - `pub struct HealthResponse { pub status: String, pub version: String }` (`Serialize`, `ToSchema`).
  - `pub struct Problem { r#type: String, title: String, status: u16, detail: String }` (`Serialize`, `ToSchema`); `ApiError(GetHealthError)` com `IntoResponse` -> 500, `Content-Type: application/problem+json`, `title: "Internal error"`, `detail` genérico fixo (INF-04).
  - `pub struct ApiDoc` (`utoipa::OpenApi`) com o path do handler (`#[utoipa::path(get, path = "/api/health", responses(200 body HealthResponse, 500 body Problem content_type "application/problem+json")))`) e os schemas `HealthResponse`, `Problem`.

- [x] **Step 1: Write failing tests** via `tower::ServiceExt::oneshot` com a porta mockada: `ac_01_br_01_health_returns_200_with_ok_and_version` (corpo `{"status":"ok","version":"1.2.3"}`); `ac_03_br_05_health_failure_is_problem_json_without_cause` (500, content-type `application/problem+json`, `detail` não contém a mensagem da causa); `ac_03_br_05_empty_version_is_problem_json`; `ac_01_br_01_post_health_keeps_405` e `ac_01_br_01_unknown_route_keeps_404`; `ac_07_br_06_openapi_describes_health` (200; `openapi` começa com `3.`; `paths` contém `/api/health`; `components.schemas` contém `HealthResponse` e `Problem`); `ac_08_br_05_error_body_has_problem_fields` (`type`, `title`, `status`, `detail`).
- [x] **Step 2: Run** `cargo nextest run -p adapters-http --profile unit` -> FAIL.
- [x] **Step 3: Implement** as assinaturas; o handler só chama `use_case.execute()` e mapeia; sem lógica de negócio.
- [x] **Step 4: Run** -> PASS.
- [x] **Step 5: Commit**

---

### Task 5: Composição (`bootstrap`) e remoção do monólito
- commit: fbfcfe0
- layer: bootstrap
- repo: medsafari
- depends_on: [4]
- covers: AC-01, AC-02, AC-06, BR-01, BR-04, BR-07
- test_scope: unit
- verify: `cd repos/medsafari/backend && cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo nextest run --workspace --profile unit && cargo build -p bootstrap`
- commit: refactor(bootstrap): wire hexagonal crates and remove monolithic main

**Files:** `backend/crates/bootstrap/src/{lib.rs,main.rs}` (+ `Cargo.toml`: `application`, `adapters-http`, `domain`, `axum`, `tokio`; dev: `tower`, `http-body-util`, `serde_json`).

**Interfaces:**
- Consumes: `adapters_http::router`, `application::{GetHealth, VersionProvider, VersionError}`.
- Produces: `pub struct CargoVersion` (implementa `VersionProvider` com `env!("CARGO_PKG_VERSION")`); `pub const LISTEN_ADDR: &str = "127.0.0.1:3000"`; `pub fn build_router() -> Router` (DI manual); `main` apenas faz bind em `LISTEN_ADDR`, imprime a mensagem e `axum::serve` (`expect` permitido em bootstrap).

- [x] **Step 1: Write failing tests** em `lib.rs`: `ac_01_br_04_cargo_version_reads_package_version` (`CargoVersion.version()? == env!("CARGO_PKG_VERSION")`), `ac_01_br_01_router_serves_health_with_package_version` (GET `/api/health` real -> 200 com a versão do pacote), `ac_02_br_01_listens_on_127_0_0_1_3000` (`LISTEN_ADDR` parseia como `SocketAddr` com IP `127.0.0.1` e porta `3000`).
- [x] **Step 2: Run** -> FAIL (itens não definidos).
- [x] **Step 3: Implement** as assinaturas; remover do `main.rs` tudo o que migrou (trait, estado, handler, DTO e testes antigos); `main.rs` só com configuração e fiação.
- [x] **Step 4: Run** a verificação completa -> PASS; conferir `grep -n "fn health\|struct Health\|trait VersionProvider" crates/bootstrap/src` sem resultados (AC-06).
- [x] **Step 5: Commit**

---

### Task 6: Teste da regra de dependência
- commit: ad0af72
- layer: bootstrap
- repo: medsafari
- depends_on: [5]
- covers: AC-04, AC-13, BR-02, BR-03, BR-11
- test_scope: unit
- verify: `cd repos/medsafari/backend && cargo fmt --check && cargo clippy --workspace -- -D warnings && cargo nextest run -p bootstrap --profile unit`
- commit: test(bootstrap): enforce layer dependency rule via cargo metadata

**Files:** `backend/crates/bootstrap/tests/architecture.rs` (dev-dependency `serde_json`).

**Interfaces:**
- Produces: dois testes que executam `cargo metadata --format-version 1 --no-deps` e leem `packages[].dependencies[].name` dos membros: `ac_04_br_02_layers_only_depend_inward` (permitido: `domain` -> nenhum interno; `application` -> `domain`; `adapters-http` -> `application`, `domain`; `bootstrap` -> todos) e `ac_13_br_11_no_postgres_crate_and_no_sqlx_user` (nenhum membro `adapters-postgres`; nenhum membro depende de `sqlx`).

- [x] **Step 1: Write failing tests** e provar o RED: adicionar temporariamente `application` como dependência de `domain` (e `sqlx` em um membro) e ver os dois testes falharem; reverter.
- [x] **Step 2: Run** -> FAIL com a dependência proibida presente.
- [x] **Step 3: Implement** o helper que carrega o metadata e as asserções.
- [x] **Step 4: Run** sem a dependência proibida -> PASS. Se `cargo metadata` se mostrar frágil, parar e reportar (INF-12).
- [x] **Step 5: Commit**

---

### Task 7: Hooks `lefthook`
- commit: 7f1a5fe
- layer: bootstrap
- repo: medsafari
- depends_on: [5]
- covers: AC-10, AC-11, BR-09
- test_scope: unit
- verify: `cd repos/medsafari && lefthook run pre-commit` (verde no código conforme; vermelho com formatação quebrada)
- commit: chore: add lefthook pre-commit hooks for the backend

**Files:** `repos/medsafari/lefthook.yml`.

**Interfaces:**
- Produces: `pre-commit` com `parallel: true` e comandos `fmt` (`cargo fmt --check`), `clippy` (`cargo clippy --workspace -- -D warnings`), `unit` (`cargo nextest run --workspace --profile unit`), cada um com `root: backend/` e `glob: "backend/**/*.{rs,toml}"` (INF-11, R-06).

- [x] **Step 1: Write the failing check** - criar `lefthook.yml`, `lefthook install`, e introduzir uma linha mal formatada em um `.rs` do `domain`.
- [x] **Step 2: Run** `lefthook run pre-commit` -> FAIL em `fmt` (prova AC-10).
- [x] **Step 3: Revert** a linha mal formatada.
- [x] **Step 4: Run** `lefthook run pre-commit` -> PASS nos três comandos (prova AC-11); registrar a saída no relatório de VERIFY.
- [x] **Step 5: Commit**

---

## Self-review

- **Spec coverage:** WD-01..WD-07 mapeiam para as Tasks 1..7; AC-01..AC-13 e BR-01..BR-11 cobertos (AC-06 por teste de estrutura da Task 5 e revisão no VERIFY; AC-09 pelo perfil `unit` e pela execução de todas as tarefas).
- **Consistência de tipos:** `AppVersion`, `VersionError`, `GetHealth`, `Health`, `GetHealthError`, `router`, `build_router`, `LISTEN_ADDR` definidos uma vez e usados com as mesmas assinaturas.
- **Persistência:** nenhuma tarefa toca `adapters-postgres` ou `migrations`; todas são `unit`.
