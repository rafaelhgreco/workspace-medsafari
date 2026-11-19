# Cadastro, login e sessão - backend Implementation Plan

> Plan produced by Termite; tasks are executed by step-03 of the termite skill.

**Goal:** Entregar no backend Rust/Axum o acesso por e-mail (link e código), criação de conta com termos, sessão em cookie, logout e sincronização idempotente do progresso.

**Architecture:** Hexagonal existente (`domain <- application <- adapters <- bootstrap`). Casos de uso na `application` com portas mockáveis; novo crate `adapters-postgres` (sqlx sem macros); `adapters-http` com rotas finas, cookie e middleware; `bootstrap` com configuração, adaptadores de infraestrutura e fiação.

**Tech Stack:** Rust 2024, Axum 0.8, sqlx 0.9 (Postgres), utoipa 6, mockall, nextest, testcontainers (Postgres) via Podman.

**Spec:** `artifacts/active/login-register/backend/delivery/02-tech-spec.md` (histórias em `01-functional-stories.md`). `<R>` abaixo = `repos/medsafari/backend`.

## Global Constraints

- Branch `feat/login-register-backend`; um commit Conventional por tarefa, com `LEFTHOOK=0` e a linha `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>` ao final.
- Dependência: `domain <- application <- (adapters-postgres, adapters-http) <- bootstrap`; adaptadores não dependem um do outro; `domain` sem `serde`, `sqlx`, `axum`, `tokio`, `utoipa`, `async-trait`.
- E-mail normalizado (trim, minúsculas, pontos e `+` mantidos), formato válido, no máximo 254 caracteres; inválido → `422`, título `Invalid Email Format`.
- Link e código: 15 minutos, uso único, só HMAC-SHA256 com `AUTH_SECRET` guardado; código de 6 dígitos; 5 erros invalidam o pedido; pedido novo invalida os abertos do mesmo e-mail.
- Limites: 3 envios por 15 minutos e 10 por dia por e-mail; 20 envios por hora por IP; 30 tentativas de código por hora por IP. Resposta ao pedido de acesso sempre idêntica, também sob limite.
- Sessão: cookie `session`, `HttpOnly`, `Secure`, `SameSite=Lax`, `Path=/`; expira em 30 dias renovados a cada uso (`min(agora + 30 dias, criação + 90 dias)`); o id não aparece em corpo nem em log; só o hash vai ao banco.
- `signup_token` e janela de aceite de termos: 15 minutos. Versão aceita deve ser igual à vigente (`TERMS_VERSION`, `PRIVACY_VERSION`).
- Nome de exibição opcional, aparado, no máximo 80 caracteres. `user_id` nunca aparece em resposta nem em e-mail.
- `attempts.question_id` sem FK; `attempt_id` único (idempotência).
- Erros em `application/problem+json`; handlers finos; sem `unwrap`/`expect` fora de testes e `bootstrap`; nunca logar token, código ou cookie (exceção única: adaptador de e-mail de desenvolvimento, só com `APP_ENV=dev`).
- Testes: `cargo nextest run --workspace --profile unit` (sem Docker); integração com `DOCKER_HOST=unix:///run/user/1000/podman/podman.sock cargo nextest run --workspace --profile integration`. Nomes `ac_<nn>_br_<nn>_<comportamento>`.
- Banco local e de teste: imagem oficial `docker.io/library/postgres:17` (mesma tag em `dev/db.sh` e em `support::test_db`), sem imagem customizada; as tabelas vêm só das migrações do sqlx, aplicadas pelo binário `migrate` ou na subida da API.
- Versões de crates novas (`uuid`, `time`, `sha2`, `hmac`, `getrandom`, `base64`, `tracing-subscriber`, `testcontainers`, `testcontainers-modules`) resolvidas com `cargo add` e fixadas em `[workspace.dependencies]`; features de `sqlx`: `runtime-tokio`, `postgres`, `migrate`, `uuid`, `time`.

## Review Focus

1. E-mail com maiúsculas, espaços nas pontas e `+`; exatamente 254 caracteres é válido e 255 não (T1, T5).
2. Cinco códigos errados em paralelo nunca passam de 5 tentativas contadas, e um token consumido em paralelo só vale uma vez (T10).
3. Fronteira de tempo: pedido com `expires_at == agora` já está expirado; sessão com 90 dias exatos já está expirada (T2, T10, T11).
4. Sincronização com lista vazia, com `attempt_id` repetido no mesmo lote e com mais de 1000 tentativas (limite proposto, recusado com `422`) (T8, T15).
5. Cookie ausente, vazio ou com lixo devolve `401` e nunca `500`; `signup_token` enviado duas vezes seguidas cria uma única conta (T11, T14, T7).

---

### Task 1: Value objects do domínio
- layer: domain
- repo: medsafari
- depends_on: []
- covers: AC-03, AC-04, AC-19, BR-05, BR-15, BR-24
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p domain --profile unit`
- commit: feat(domain): add email, access code, document version and display name

**Files:** Modify `<R>/crates/domain/src/lib.rs` (módulos `email.rs`, `access.rs`, `terms.rs` novos); `DomainError` ganha `InvalidEmail`, `InvalidAccessCode`, `InvalidDocumentVersion`, `InvalidDisplayName`.

**Interfaces — Produces:** `Email::parse(&str) -> Result<Email, DomainError>` + `as_str(&self) -> &str`; `AccessCode::parse(&str) -> Result<AccessCode, DomainError>` (exatamente 6 dígitos ASCII) + `as_str`; `DocumentVersion::new(impl Into<String>) -> Result<Self, DomainError>` (não vazio após trim) + `as_str`; `DisplayName::parse_optional(Option<&str>) -> Result<Option<DisplayName>, DomainError>` (vazio vira `None`, máximo 80 caracteres) + `as_str`.

- [x] Escrever testes: `ac_03_br_05_email_is_trimmed_and_lowercased`, `ac_03_br_05_email_keeps_dots_and_plus`, `ac_04_br_24_email_rejects_missing_at_and_blank`, `ac_04_br_24_email_accepts_254_and_rejects_255_chars`, `ac_19_br_15_display_name_is_optional_and_trimmed`, `ac_19_br_15_display_name_rejects_81_chars`, `ac_01_br_06_access_code_requires_six_digits`, `ac_17_br_13_document_version_rejects_blank`
- [x] Rodar e ver falhar (tipos inexistentes)
- [x] Implementar o mínimo (conta de caracteres com `chars().count()`)
- [x] Rodar `cargo nextest run -p domain --profile unit`, ver passar
- [x] Commit
- commit: 87dc530
### Task 2: Tentativa, identificadores e política de sessão
- layer: domain
- repo: medsafari
- depends_on: [1]
- covers: AC-21, AC-22, AC-33, BR-11, BR-19
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p domain --profile unit`
- commit: feat(domain): add attempt, ids and session policy

**Files:** Modify `<R>/Cargo.toml` (adiciona `uuid`, `time`), `<R>/crates/domain/Cargo.toml`, `<R>/crates/domain/src/lib.rs` (módulos `ids.rs`, `attempt.rs`, `session.rs`).

**Interfaces — Produces:** `UserId(pub Uuid)`, `SessionId(pub Uuid)`, `AttemptId(pub Uuid)` (`Copy`, `Eq`, `Hash`); `Attempt { attempt_id: AttemptId, question_id: String, selected_option: String, is_correct: bool, answered_at: OffsetDateTime, device_id: Option<Uuid> }`; `SessionPolicy::default()` (30 dias deslizantes, 90 absolutos); `SessionPolicy::next_expiry(&self, created_at: OffsetDateTime, now: OffsetDateTime) -> OffsetDateTime` = `min(now + 30d, created_at + 90d)`; `SessionPolicy::is_expired(&self, created_at, expires_at, now) -> bool` (verdadeiro quando `now >= expires_at` ou `now >= created_at + 90d`).

- [x] Escrever testes: `ac_21_br_11_next_expiry_is_30_days_after_use`, `ac_22_br_11_next_expiry_is_capped_at_90_days_from_creation`, `ac_22_br_11_is_expired_at_exactly_90_days`, `ac_21_br_11_is_not_expired_one_second_before_expiry`, `ac_33_br_19_attempt_accepts_any_question_id`
- [x] Rodar e ver falhar
- [x] Implementar o mínimo
- [x] Rodar e ver passar (inclui `architecture` mantendo `domain` sem dependências proibidas)
- [x] Commit
- commit: db3def8
### Task 3: Portas, erros e configurações da aplicação
- layer: application
- repo: medsafari
- depends_on: [2]
- covers: BR-02, BR-06, BR-07, BR-09, BR-13, BR-22
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p application --profile unit`
- commit: feat(application): add auth ports and settings

**Files:** Modify `<R>/crates/application/Cargo.toml` (`async-trait`, `time`, `uuid`), `lib.rs`; Create `<R>/crates/application/src/ports.rs`, `settings.rs`.

**Interfaces — Produces:** erro `PortError::Infra(String)`; traits `automock` e `Send + Sync`: `Clock::now() -> OffsetDateTime`; `IdGenerator::uuid() -> Uuid`; `SecretGenerator::{token() -> String, code() -> AccessCode}`; `TokenHasher::{hash(&str) -> String, matches(&str, &str) -> bool}` (comparação em tempo constante); `async EmailSender::send_access(&Email, link: &str, &AccessCode, valid_minutes: u32) -> Result<(), PortError>`; `TermsPolicy::current() -> TermsVersions` com `TermsVersions { termos: DocumentVersion, privacidade: DocumentVersion }`; repositórios `LoginRequestRepository`, `PendingSignupRepository`, `UserRepository`, `SessionRepository`, `AttemptRepository` com as assinaturas abaixo (todas `async`, `-> Result<_, PortError>`):
  - `LoginRequestRepository`: `count_by_email_since(&Email, OffsetDateTime) -> u32`; `count_by_ip_since(&str, OffsetDateTime) -> u32`; `invalidate_open(&Email, OffsetDateTime)`; `insert(NewLoginRequest { id: Uuid, email, token_hash, code_hash, ip, created_at, expires_at })`; `consume_by_token(&str hash, now) -> ConsumeOutcome` (`Consumed(Email)` | `Gone`); `verify_code(&Email, code_hash: &str, now, max_attempts: u8) -> CodeOutcome` (`Consumed` | `Wrong { remaining: u8 }` | `Gone`); `count_code_attempts_by_ip_since(&str, OffsetDateTime) -> u32`; `log_code_attempt(&str, OffsetDateTime)`.
  - `PendingSignupRepository`: `insert(email, token_hash, expires_at)`; `consume(&str hash, now) -> Option<Email>`.
  - `UserRepository`: `find_by_email(&Email) -> Option<User>`; `find_by_id(UserId) -> Option<User>`; `create_with_acceptances(NewUser, Vec<Acceptance>) -> User` (transação; e-mail já existente devolve o usuário existente); `latest_accepted(UserId) -> Option<TermsVersions>`; `record_acceptances(UserId, Vec<Acceptance>)`. `User { id, email, display_name: Option<String> }`; `Acceptance { document: Document, version: DocumentVersion, accepted_at, ip }`.
  - `SessionRepository`: `insert(NewSession { id, user_id, token_hash, label, created_at, expires_at })`; `find_active(&str hash, now) -> Option<SessionRecord { id, user_id, created_at, expires_at }>`; `touch(SessionId, last_used_at, new_expires_at)`; `revoke(SessionId, now)`; `revoke_all(UserId, now)`.
  - `AttemptRepository`: `insert_many(UserId, &[Attempt], now) -> u32` (inseridas); `insert_one(UserId, &Attempt, now) -> bool`; `list(UserId) -> Vec<Attempt>` (ordem por `answered_at`).
- `AuthSettings::default()`: `code_valid_minutes = 15`, `max_code_attempts = 5`, `email_per_15min = 3`, `email_per_day = 10`, `ip_sends_per_hour = 20`, `ip_code_attempts_per_hour = 30`, `signup_valid_minutes = 15`, `max_attempts_per_batch = 1000`, `app_base_url: String`, `verify_path = "/entrar/confirmar"`.

- [x] Escrever testes: `ac_01_br_06_settings_defaults_match_the_spec` (valores acima), `ac_06_br_09_settings_limits_match_the_spec`, `ac_12_br_07_settings_max_code_attempts_is_five`, `ac_18_br_22_settings_signup_window_is_15_minutes`
- [x] Rodar e ver falhar
- [x] Implementar traits e `AuthSettings`
- [x] Rodar e ver passar
- [x] Commit
- commit: ba0324d
### Task 4: Serviço de sessão
- layer: application
- repo: medsafari
- depends_on: [3]
- covers: AC-20, AC-21, AC-22, AC-23, AC-24, AC-25, AC-26, BR-10, BR-11, BR-12, BR-14, BR-23
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p application --profile unit`
- commit: feat(application): add session service

**Files:** Create `<R>/crates/application/src/session.rs`.

**Interfaces — Produces:** `SessionService::new(sessions, users, secrets, hasher, clock, ids, terms, policy: SessionPolicy)`; `issue(&self, UserId, label: &str) -> Result<IssuedSession { token: String, expires_at: OffsetDateTime }, SessionError>` (grava só o hash e o rótulo); `authenticate(&self, token: &str) -> Result<Principal { user_id, session_id, terms_pending: bool }, SessionError>` (renova com `next_expiry`; `Unauthenticated` se inexistente, revogada ou expirada); `get(&self, &Principal) -> Result<SessionView { email, display_name, terms_pending, current_terms }, SessionError>`; `logout(&self, &Principal)`; `logout_all(&self, &Principal)`; `SessionError::{Unauthenticated, Infra(PortError)}`.

- [x] Escrever testes com portas mockadas: `ac_23_br_23_issue_stores_hash_and_label_not_the_token`, `ac_20_br_10_issued_token_is_not_the_stored_hash`, `ac_21_br_11_authenticate_extends_expiry_to_30_days`, `ac_22_br_11_authenticate_rejects_session_past_90_days`, `ac_22_br_11_authenticate_rejects_unknown_token`, `ac_26_br_14_principal_flags_terms_pending_when_versions_differ`, `ac_26_br_14_principal_not_pending_when_versions_match`, `ac_24_br_12_logout_revokes_only_current_session`, `ac_25_br_12_logout_all_revokes_every_session_of_user`
- [x] Rodar e ver falhar
- [x] Implementar o mínimo
- [x] Rodar e ver passar
- [x] Commit
- commit: 0852faf
### Task 5: Caso de uso RequestAccess
- layer: application
- repo: medsafari
- depends_on: [3]
- covers: AC-01, AC-02, AC-03, AC-04, AC-05, AC-06, AC-07, BR-02, BR-03, BR-04, BR-05, BR-08, BR-09, BR-24
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p application --profile unit`
- commit: feat(application): add request access use case

**Files:** Create `<R>/crates/application/src/request_access.rs`.

**Interfaces — Produces:** `RequestAccess::new(requests, secrets, hasher, ids, email, clock, settings: AuthSettings)` (o `IdGenerator` gera o id do pedido); `execute(&self, email: &str, ip: &str) -> Result<(), RequestAccessError>`; `RequestAccessError::{InvalidEmail, Infra(PortError)}`. Link enviado: `"{app_base_url}{verify_path}?token={token}"`.

- [x] Escrever testes: `ac_01_br_03_sends_email_with_link_code_and_15_minutes`, `ac_01_br_02_stores_only_hashes_of_token_and_code`, `ac_03_br_05_normalizes_email_before_counting_and_storing`, `ac_04_br_24_invalid_email_is_rejected_without_sending`, `ac_05_br_08_invalidates_open_requests_before_inserting`, `ac_06_br_09_fourth_request_in_15_minutes_is_silent_ok`, `ac_06_br_09_eleventh_request_in_a_day_is_silent_ok`, `ac_07_br_09_twenty_first_request_from_ip_is_silent_ok`, `ac_02_br_04_result_is_ok_for_sent_and_for_rate_limited`
- [x] Rodar e ver falhar
- [x] Implementar o mínimo (janelas de 15 min e de 24 h contadas por `count_by_email_since`)
- [x] Rodar e ver passar
- [x] Commit
- commit: a9b683f
### Task 6: Caso de uso VerifyAccess
- layer: application
- repo: medsafari
- depends_on: [4, 5]
- covers: AC-08, AC-09, AC-10, AC-11, AC-12, AC-13, AC-14, BR-03, BR-06, BR-07, BR-09, BR-20, BR-21
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p application --profile unit`
- commit: feat(application): add verify access use case

**Files:** Create `<R>/crates/application/src/verify_access.rs`.

**Interfaces — Produces:** `VerifyAccess::new(requests, pending, users, sessions: Arc<SessionService>, secrets, hasher, clock, terms, settings)`; `execute(&self, Credential, ip: &str, label: &str) -> Result<VerifyOutcome, VerifyError>`; `Credential::{Token(String), Code { email: String, code: String }}`; `VerifyOutcome::{Authenticated(IssuedSession), TermsRequired { signup_token: String, expires_at: OffsetDateTime, terms: TermsVersions }}`; `VerifyError::{Gone, WrongCode { remaining: u8 }, InvalidCode, InvalidEmail, TooManyAttempts, Infra(PortError)}`. Código mal formado devolve `InvalidCode` sem contar tentativa; o limite por IP só vale para o caminho do código e registra cada tentativa.

- [x] Escrever testes: `ac_08_br_03_token_for_existing_user_issues_session`, `ac_09_br_03_code_for_existing_user_issues_session`, `ac_10_br_06_gone_when_token_already_consumed`, `ac_11_br_06_gone_when_request_expired`, `ac_12_br_07_wrong_code_reports_remaining_attempts`, `ac_12_br_07_fifth_wrong_code_is_gone_even_with_right_code`, `ac_14_br_09_code_attempt_above_ip_limit_is_rejected_before_checking`, `ac_15_br_21_unknown_email_returns_terms_required_without_creating_user`, `ac_13_br_20_no_read_only_operation_consumes_the_token` (garante que só `execute` chama `consume_by_token`)
- [x] Rodar e ver falhar
- [x] Implementar o mínimo
- [x] Rodar e ver passar
- [x] Commit
- commit: 00a7622
### Task 7: CompleteSignup e AcceptTerms
- layer: application
- repo: medsafari
- depends_on: [4]
- covers: AC-15, AC-16, AC-17, AC-18, AC-19, AC-27, BR-01, BR-13, BR-14, BR-15, BR-21, BR-22
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p application --profile unit`
- commit: feat(application): add signup completion and terms acceptance

**Files:** Create `<R>/crates/application/src/signup.rs`.

**Interfaces — Produces:** `CompleteSignup::new(pending, users, sessions: Arc<SessionService>, ids, hasher, clock, terms)` (o `IdGenerator` gera o `UserId`); `execute(&self, signup_token: &str, accepted: AcceptedTerms { termos: String, privacidade: String }, display_name: Option<&str>, ip: &str, label: &str) -> Result<IssuedSession, SignupError>`; `SignupError::{Gone, VersionMismatch, InvalidDisplayName, Infra(PortError)}`; `AcceptTerms::new(users, clock, terms)`; `execute(&self, &Principal, AcceptedTerms, ip: &str) -> Result<(), TermsError>` com `TermsError::{VersionMismatch, Infra(PortError)}`. A versão é validada antes de consumir o `signup_token`.

- [x] Escrever testes: `ac_15_br_01_signup_creates_user_acceptances_and_session`, `ac_15_br_13_acceptance_records_version_time_and_ip_for_both_documents`, `ac_16_br_21_no_signup_token_means_no_user`, `ac_17_br_13_mismatched_version_creates_nothing_and_keeps_token`, `ac_18_br_22_expired_signup_token_is_gone`, `ac_19_br_15_signup_without_display_name_is_valid`, `ac_27_br_14_accept_terms_records_current_versions`, `ac_27_br_13_accept_terms_rejects_old_version`, `ac_15_br_01_second_use_of_signup_token_is_gone`
- [x] Rodar e ver falhar
- [x] Implementar o mínimo
- [x] Rodar e ver passar
- [x] Commit
- commit: c4e675c
### Task 8: Caso de uso de progresso
- layer: application
- repo: medsafari
- depends_on: [4]
- covers: AC-26, AC-28, AC-29, AC-30, AC-31, AC-32, AC-33, BR-14, BR-16, BR-17, BR-18, BR-19
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p application --profile unit`
- commit: feat(application): add progress sync and attempt recording

**Files:** Create `<R>/crates/application/src/progress.rs`.

**Interfaces — Produces:** `SyncProgress::new(attempts, clock, settings)`; `execute(&self, &Principal, Vec<Attempt>) -> Result<Vec<Attempt>, ProgressError>` (grava as novas e devolve a lista completa); `RecordAttempt::new(attempts, clock)`; `execute(&self, &Principal, Attempt) -> Result<RecordOutcome, ProgressError>` (`Created` | `AlreadyExisted`); `ProgressError::{TermsPending, TooManyAttempts, Infra(PortError)}`. Ambos recusam com `TermsPending` quando `principal.terms_pending`; lote acima de `max_attempts_per_batch` recusa com `TooManyAttempts`; `attempt_id` repetido no mesmo lote conta uma vez.

- [x] Escrever testes: `ac_28_br_16_sync_inserts_new_attempts_and_returns_full_list`, `ac_29_br_16_sync_with_same_attempts_adds_nothing`, `ac_28_br_16_sync_with_empty_list_returns_account_progress`, `ac_30_br_17_sync_returns_attempts_of_account_not_only_sent`, `ac_28_br_16_duplicate_attempt_id_in_one_batch_counts_once`, `ac_26_br_14_sync_refused_when_terms_pending`, `ac_26_br_14_record_refused_when_terms_pending`, `ac_31_br_18_record_creates_attempt`, `ac_32_br_18_record_twice_reports_already_existed`, `ac_33_br_19_record_does_not_check_question_existence`, `ac_28_br_16_batch_over_1000_is_rejected`
- [x] Rodar e ver falhar
- [x] Implementar o mínimo
- [x] Rodar e ver passar
- [x] Commit
- commit: 2738229
### Task 9: Crate adapters-postgres, migrações e perfis do nextest
- layer: adapters-postgres
- repo: medsafari
- depends_on: [3]
- covers: BR-05, BR-06, BR-16, BR-19
- test_scope: unit+integration
- verify: `cd <R> && cargo nextest run --workspace --profile unit && DOCKER_HOST=unix:///run/user/1000/podman/podman.sock cargo nextest run --workspace --profile integration`
- commit: feat(adapters-postgres): add crate, migrations and integration profile

**Files:** Create `<R>/crates/adapters-postgres/{Cargo.toml,src/lib.rs,migrations/0001_auth.sql,migrations/0002_attempts.sql,tests/support/mod.rs,tests/schema.rs}`; Modify `<R>/Cargo.toml` (deps do workspace e `adapters-postgres`), `<R>/.config/nextest.toml` (perfil `unit` com `default-filter = "not package(adapters-postgres)"` e novo perfil `integration` com `default-filter = "package(adapters-postgres)"`; o nextest recusa `binary(auth_flow)` antes de o binário existir, então a Task 17 estende os dois filtros), `<R>/crates/bootstrap/tests/architecture.rs` (substitui `ac_13_br_11_no_postgres_crate_and_no_sqlx_user` por `ac_13_br_11_postgres_adapter_depends_only_inward`; `ALLOWED` ganha `("adapters-postgres", &["application", "domain"])`; `bootstrap` ganha `adapters-postgres`; só `adapters-postgres` pode usar `sqlx`).

**Interfaces — Produces:** `PgStore::new(PgPool) -> PgStore` (implementará as cinco portas nas tarefas 10 e 11); `adapters_postgres::migrate(&PgPool) -> Result<(), sqlx::migrate::MigrateError>`; helper de teste `support::test_db() -> TestDb { pool, .. }` (sobe um container `postgres:17`, aplica as migrações e mantém o container vivo enquanto o `TestDb` existir). Tabelas: `users(id uuid pk, email text unique, display_name text null, email_verified_at, created_at, deleted_at null)`, `login_requests(id, email, token_hash unique, code_hash, code_attempts int, expires_at, used_at null, invalidated_at null, requested_ip, created_at)`, `pending_signups(id, email, token_hash unique, expires_at, used_at null, created_at)`, `sessions(id, user_id fk, token_hash unique, user_agent_label, created_at, last_used_at, expires_at, revoked_at null)`, `terms_acceptances(id, user_id fk, document, version, accepted_at, ip)`, `code_attempt_log(id, ip, attempted_at)`, `attempts(attempt_id uuid pk, user_id fk, question_id text, selected_option text, is_correct bool, answered_at, device_id uuid null, synced_at)` sem FK em `question_id`; índices em `login_requests(email, created_at)`, `login_requests(requested_ip, created_at)`, `code_attempt_log(ip, attempted_at)`, `attempts(user_id, answered_at)`.

- [x] Escrever testes de integração em `tests/schema.rs`: `br_05_users_email_is_unique`, `br_16_attempt_id_is_unique`, `br_19_attempts_accept_unknown_question_id`; e o teste de arquitetura novo
- [x] Rodar o perfil `integration` e ver falhar (crate/tabelas ausentes); rodar `unit` e ver o teste de arquitetura falhar
- [x] Criar o crate, as migrações, o helper e os perfis
- [x] Rodar `unit` e `integration`, ver passar
- [x] Commit
- commit: 824015d
### Task 10: Repositórios de pedido de acesso e cadastro pendente
- layer: adapters-postgres
- repo: medsafari
- depends_on: [9]
- covers: AC-05, AC-06, AC-07, AC-10, AC-11, AC-12, AC-14, AC-18, BR-06, BR-07, BR-08, BR-09, BR-22
- test_scope: unit+integration
- verify: `cd <R> && DOCKER_HOST=unix:///run/user/1000/podman/podman.sock cargo nextest run -p adapters-postgres --profile integration`
- commit: feat(adapters-postgres): add login request and pending signup repositories

**Files:** Create `<R>/crates/adapters-postgres/src/login_requests.rs`, `pending_signups.rs`, `tests/login_requests.rs`; Modify `lib.rs`.

**Interfaces — Consumes:** portas `LoginRequestRepository` e `PendingSignupRepository` (Task 3). **Produces:** `impl` de ambas em `PgStore`. `consume_by_token` e `verify_code` são atômicos (`UPDATE ... WHERE used_at IS NULL AND invalidated_at IS NULL AND expires_at > $now RETURNING`); `verify_code` incrementa `code_attempts` na mesma instrução, invalida na 5ª e devolve `remaining`; consumir por um meio marca o pedido inteiro como usado.

- [x] Escrever testes de integração: `ac_10_br_06_token_consumed_once_even_in_parallel`, `ac_11_br_06_request_expires_at_the_boundary`, `ac_10_br_06_using_the_link_invalidates_the_code`, `ac_12_br_07_parallel_wrong_codes_never_exceed_five_attempts`, `ac_12_br_07_correct_code_after_five_wrong_is_gone`, `ac_05_br_08_new_request_invalidates_open_ones_of_same_email`, `ac_06_br_09_counts_by_email_window_ignore_older_rows`, `ac_07_br_09_counts_by_ip_in_last_hour`, `ac_14_br_09_code_attempts_by_ip_are_counted`, `ac_18_br_22_pending_signup_is_single_use_and_expires`
- [x] Rodar e ver falhar
- [x] Implementar as consultas com `sqlx::query` e `bind`
- [x] Rodar e ver passar
- [x] Commit
- commit: 968cd8d
### Task 11: Repositórios de usuário, sessão e tentativas
- layer: adapters-postgres
- repo: medsafari
- depends_on: [9]
- covers: AC-15, AC-21, AC-22, AC-24, AC-25, AC-28, AC-29, AC-30, AC-31, AC-32, AC-33, BR-01, BR-11, BR-12, BR-13, BR-16, BR-18, BR-19
- test_scope: unit+integration
- verify: `cd <R> && DOCKER_HOST=unix:///run/user/1000/podman/podman.sock cargo nextest run -p adapters-postgres --profile integration`
- commit: feat(adapters-postgres): add user, session and attempt repositories

**Files:** Create `<R>/crates/adapters-postgres/src/users.rs`, `sessions.rs`, `attempts.rs`, `tests/accounts.rs`, `tests/progress.rs`; Modify `lib.rs`.

**Interfaces — Consumes:** `UserRepository`, `SessionRepository`, `AttemptRepository` (Task 3). **Produces:** `impl` em `PgStore`. `create_with_acceptances` roda numa transação e, em conflito de e-mail, devolve o usuário existente sem gravar aceites; `find_active` ignora sessão revogada, com `expires_at <= now` ou com `created_at + 90 dias <= now`; `insert_many` e `insert_one` usam `ON CONFLICT (attempt_id) DO NOTHING`; `list` ordena por `answered_at` e `attempt_id`.

- [x] Escrever testes de integração: `ac_15_br_01_create_user_and_acceptances_commit_together`, `ac_15_br_13_failed_acceptance_rolls_back_the_user`, `ac_15_br_01_concurrent_create_for_same_email_yields_one_user`, `ac_21_br_11_touch_updates_last_used_and_expiry`, `ac_22_br_11_find_active_rejects_session_at_90_days`, `ac_24_br_12_revoke_keeps_other_sessions`, `ac_25_br_12_revoke_all_covers_every_session_of_user`, `ac_28_br_16_insert_many_skips_existing_attempt_ids`, `ac_29_br_16_repeating_the_batch_inserts_zero`, `ac_30_br_17_list_returns_all_attempts_of_user_only`, `ac_32_br_18_insert_one_reports_duplicate`, `ac_33_br_19_attempt_with_unknown_question_is_stored`
- [x] Rodar e ver falhar
- [x] Implementar
- [x] Rodar e ver passar
- [x] Commit
- commit: c5911d2
### Task 12: Erro genérico de API e estado do router
- layer: adapters-http
- repo: medsafari
- depends_on: [4]
- covers: AC-20, BR-04, BR-10, BR-24
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p adapters-http --profile unit`
- commit: refactor(adapters-http): generalize api error and add auth state

**Files:** Modify `<R>/crates/adapters-http/Cargo.toml`, `src/error.rs`, `src/lib.rs`; Create `src/state.rs`, `src/cookie.rs`, `src/client_ip.rs`.

**Interfaces — Produces:** `ApiError::{Problem(StatusCode, title: &'static str, detail: String), Internal}` com `IntoResponse` problem+json (detalhe interno nunca vaza) e `From<GetHealthError>` preservando o 500 atual; `AuthApi { request_access, verify, signup, sessions, accept_terms, sync, record: Arc<...>, client_ip_header: Option<String> }`; `router(health: Arc<GetHealth>) -> Router` mantém a assinatura (o `bootstrap` não quebra); a Task 13 adiciona `auth_router(api: Arc<AuthApi>) -> Router` e o `bootstrap` faz `merge` dos dois na Task 16; `cookie::set(token: &str, expires_at: OffsetDateTime) -> HeaderValue` (`session=<token>; HttpOnly; Secure; SameSite=Lax; Path=/; Expires=...`); `cookie::clear() -> HeaderValue`; `cookie::read(&HeaderMap) -> Option<String>` (ignora vazio e lixo); extrator `ClientIp(String)` (cabeçalho confiável configurado, senão `ConnectInfo`, senão `"unknown"`).

- [x] Escrever testes: `ac_20_br_10_set_cookie_has_httponly_secure_samesite_lax`, `ac_20_br_10_clear_cookie_expires_in_the_past`, `ac_20_br_10_read_cookie_ignores_empty_and_garbage`, `ac_01_br_01_existing_health_tests_still_pass`, `ac_04_br_24_problem_json_has_type_title_status_detail`, `ac_02_br_04_internal_error_does_not_leak_cause`
- [x] Rodar e ver falhar
- [x] Implementar o mínimo (cookie montado à mão, sem `axum-extra`)
- [x] Rodar e ver passar (testes de `health` incluídos)
- [x] Commit
- commit: fbed10c
### Task 13: Rotas de acesso e cadastro
- layer: adapters-http
- repo: medsafari
- depends_on: [5, 6, 7, 12]
- covers: AC-01, AC-02, AC-04, AC-08, AC-09, AC-10, AC-11, AC-12, AC-13, AC-14, AC-15, AC-16, AC-17, AC-18, AC-19, BR-04, BR-06, BR-07, BR-09, BR-13, BR-20, BR-22, BR-24
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p adapters-http --profile unit`
- commit: feat(adapters-http): add access request, verify and signup routes

**Files:** Create `<R>/crates/adapters-http/src/auth/{mod.rs,access.rs}`; Modify `lib.rs`, `openapi.rs`.

**Interfaces — Produces:** `POST /api/auth/access-requests` (`{email}` → `202 {message}` idêntico sempre; `InvalidEmail` → `422` título `Invalid Email Format`); `POST /api/auth/verify` (`{token}` ou `{email, code}`; `Authenticated` → `200 {status:"authenticated"}` + `Set-Cookie`; `TermsRequired` → `200 {status:"terms_required", signup_token, expires_at, terms}`; `Gone` → `410`; `WrongCode` → `422` com `attempts_remaining`; `TooManyAttempts` → `429`; `InvalidCode` → `422`); `POST /api/auth/signup` (`{signup_token, accepted, display_name?}` → `201` + `Set-Cookie`; `Gone` → `410`; `VersionMismatch` → `422`). Nenhum `GET` consome token. DTOs com `ToSchema` e rotas com `#[utoipa::path]`, registradas em `ApiDoc`. O rótulo da sessão sai do `User-Agent`.

- [x] Escrever testes via `tower::ServiceExt::oneshot` com casos de uso sobre portas mockadas: `ac_02_br_04_access_response_is_identical_for_known_unknown_and_limited`, `ac_04_br_24_invalid_email_is_422_invalid_email_format`, `ac_08_br_06_verify_token_sets_session_cookie_without_token_in_body`, `ac_09_br_06_verify_code_returns_authenticated`, `ac_10_br_06_used_token_is_410`, `ac_11_br_06_expired_token_is_410`, `ac_12_br_07_wrong_code_is_422_with_attempts_remaining`, `ac_14_br_09_ip_limit_is_429`, `ac_13_br_20_get_on_verify_route_is_405`, `ac_15_br_13_signup_returns_201_and_cookie`, `ac_16_br_22_signup_with_expired_token_is_410`, `ac_17_br_13_signup_with_old_version_is_422`, `ac_19_br_13_signup_without_display_name_is_201`, `ac_01_br_04_openapi_lists_auth_access_routes`
- [x] Rodar e ver falhar
- [x] Implementar handlers finos e o mapeamento de erros
- [x] Rodar e ver passar
- [x] Commit
- commit: c624e85
### Task 14: Middleware de autenticação e rotas de sessão
- layer: adapters-http
- repo: medsafari
- depends_on: [4, 7, 12]
- covers: AC-20, AC-21, AC-22, AC-24, AC-25, AC-26, AC-27, BR-10, BR-11, BR-12, BR-14
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p adapters-http --profile unit`
- commit: feat(adapters-http): add auth middleware and session routes

**Files:** Create `<R>/crates/adapters-http/src/auth/{middleware.rs,session.rs}`; Modify `lib.rs`, `openapi.rs`.

**Interfaces — Produces:** middleware `from_fn_with_state` que lê o cookie, chama `SessionService::authenticate` e põe `Principal` nas extensions (sem sessão → `401`); rotas protegidas: `GET /api/auth/session` (`200 {email, display_name, terms_pending, current_terms}`, sem `user_id`), `POST /api/auth/terms` (`{accepted}` → `204`; `VersionMismatch` → `422`), `POST /api/auth/logout` e `POST /api/auth/logout-all` (`204` + cookie removido). Rotas públicas continuam as das tarefas 13 e `health`/OpenAPI.

- [x] Escrever testes: `ac_20_br_10_session_without_cookie_is_401`, `ac_22_br_11_expired_session_is_401`, `ac_20_br_10_garbage_cookie_is_401_not_500`, `ac_21_br_11_session_response_has_no_user_id`, `ac_26_br_14_session_reports_terms_pending`, `ac_27_br_14_accept_terms_returns_204`, `ac_24_br_12_logout_clears_cookie_and_returns_204`, `ac_25_br_12_logout_all_returns_204`, `ac_24_br_12_second_logout_with_same_cookie_is_401`
- [x] Rodar e ver falhar
- [x] Implementar
- [x] Rodar e ver passar
- [x] Commit
- commit: 7572181
### Task 15: Rotas de progresso e contrato OpenAPI
- layer: adapters-http
- repo: medsafari
- depends_on: [8, 14]
- covers: AC-26, AC-28, AC-29, AC-30, AC-31, AC-32, AC-33, BR-14, BR-16, BR-17, BR-18, BR-19
- test_scope: unit
- verify: `cd <R> && cargo nextest run -p adapters-http --profile unit`
- commit: feat(adapters-http): add progress routes and openapi contract

**Files:** Create `<R>/crates/adapters-http/src/progress.rs`; Modify `lib.rs`, `openapi.rs`.

**Interfaces — Produces:** `POST /api/progress/sync` (`{schema_version:1, device_id, attempts[]}` → `200 {schema_version:1, attempts[]}`; `TermsPending` → `403`; `TooManyAttempts` → `422`) e `POST /api/progress/attempts` (uma tentativa → `201` nova, `200` já existente; `403` termos pendentes; `422` corpo inválido). Ambas atrás do middleware. `schema_version` diferente de 1 → `422`. `ApiDoc` descreve todas as rotas da spec.

- [x] Escrever testes: `ac_28_br_16_sync_returns_full_progress`, `ac_29_br_16_sync_repeated_returns_same_total`, `ac_30_br_17_sync_with_empty_list_returns_account_attempts`, `ac_28_br_16_sync_over_1000_attempts_is_422`, `ac_26_br_14_sync_with_terms_pending_is_403`, `ac_31_br_18_record_new_attempt_is_201`, `ac_32_br_18_record_existing_attempt_is_200`, `ac_33_br_19_record_accepts_unknown_question_id`, `ac_28_br_16_unknown_schema_version_is_422`, `ac_01_br_01_openapi_describes_every_auth_and_progress_route`
- [x] Rodar e ver falhar
- [x] Implementar
- [x] Rodar e ver passar
- [x] Commit
- commit: f878fb4
### Task 16: Configuração, adaptadores de infraestrutura e fiação
- layer: bootstrap
- repo: medsafari
- depends_on: [9, 10, 11, 13, 14, 15]
- covers: AC-01, AC-02, AC-06, AC-20, BR-02, BR-06, BR-09, BR-10, BR-13
- test_scope: unit
- verify: `cd <R> && cargo nextest run --workspace --profile unit && cargo fmt --check && cargo clippy --workspace -- -D warnings`
- commit: feat(bootstrap): wire auth use cases, config and infra adapters

**Files:** Create `<R>/crates/bootstrap/src/{config.rs,infra.rs}`, `<R>/crates/bootstrap/src/bin/migrate.rs`, `<R>/dev/db.sh`; Modify `<R>/crates/bootstrap/Cargo.toml`, `src/lib.rs`, `src/main.rs`, `<R>/docs/requests.http` (requisições de exemplo das rotas novas).

**Interfaces — Produces:** `Config::from_lookup(impl Fn(&str) -> Option<String>) -> Result<Config, ConfigError>` lendo `DATABASE_URL`, `APP_BASE_URL`, `AUTH_SECRET` (mínimo 32 caracteres), `TERMS_VERSION`, `PRIVACY_VERSION`, `APP_ENV` (`dev` ou `prod`), `TRUSTED_IP_HEADER` (opcional); adaptadores `SystemClock`, `OsIdGenerator`, `OsSecretGenerator` (token de 32 bytes em base64 url-safe; código de 6 dígitos sem viés), `HmacHasher::new(secret)`, `EnvTermsPolicy`, `LogEmailSender` (só criado com `APP_ENV=dev`), `BackgroundEmailSender<S: EmailSender>` (devolve na hora e envia com `tokio::spawn`, falha só gera `tracing::warn!`); `build_router(&Config, PgPool) -> Router`; `main` aplica as migrações, inicia `tracing` e serve com `into_make_service_with_connect_info`. `APP_ENV=prod` sem provedor real de e-mail recusa subir (`ConfigError::NoEmailProvider`). Binário `migrate` (`cargo run -p bootstrap --bin migrate`): lê `DATABASE_URL`, chama `adapters_postgres::migrate` e imprime as migrações aplicadas. `dev/db.sh up|down|status` usa `podman` para criar ou remover o container `medsafari-pg` (`docker.io/library/postgres:17`, porta 5432, volume nomeado, espera o `pg_isready`) e imprime a `DATABASE_URL`.

- [x] Escrever testes: `ac_01_br_02_config_requires_secret_of_32_chars`, `ac_01_br_06_hmac_is_deterministic_and_secret_dependent`, `ac_01_br_06_hmac_matches_is_false_for_other_value`, `ac_02_br_04_background_sender_returns_even_when_inner_fails`, `ac_06_br_09_secret_generator_code_is_always_six_digits`, `ac_20_br_10_secret_generator_tokens_are_unique_and_url_safe`, `ac_01_br_13_config_rejects_missing_terms_versions`, `ac_01_br_02_prod_without_email_provider_is_refused`
- [x] Rodar e ver falhar
- [x] Implementar
- [x] Rodar `unit`, `fmt` e `clippy`, ver passar
- [x] Verificação manual (vai para o relatório do VERIFY): `dev/db.sh up`, `DATABASE_URL=<url impressa> cargo run -p bootstrap --bin migrate` e `podman exec medsafari-pg psql -U postgres -c '\dt'` listando as sete tabelas mais `_sqlx_migrations`; rodar `migrate` de novo não falha
- [x] Commit
- commit: cd16e88
### Task 17: Fluxo completo sobre Postgres
- layer: bootstrap
- repo: medsafari
- depends_on: [16]
- covers: AC-01, AC-08, AC-15, AC-28, AC-29, AC-25, BR-01, BR-16, BR-12
- test_scope: unit+integration
- verify: `cd <R> && DOCKER_HOST=unix:///run/user/1000/podman/podman.sock cargo nextest run --workspace --profile integration`
- commit: test(bootstrap): add end-to-end auth flow on postgres

**Files:** Create `<R>/crates/bootstrap/tests/auth_flow.rs`; Modify `<R>/crates/bootstrap/Cargo.toml` (dev-deps de testcontainers).

**Nota:** esta tarefa foge da regra "`unit+integration` só se toca `adapters-postgres`/`migrations`": o arquivo mora em `bootstrap`, mas exige Postgres. Esta tarefa estende os `default-filter` dos perfis `unit` e `integration` com `binary(auth_flow)`.

- [x] Escrever o teste `ac_15_br_01_visitor_signs_up_and_keeps_progress` com e-mail de teste que captura link e código: pede acesso, confirma, aceita os termos, envia 12 tentativas e vê 12; depois `ac_08_br_16_login_in_second_browser_sums_attempts_without_duplicates` (30 + 5, reenvio das 5 mantém 35) e `ac_25_br_12_logout_all_invalidates_both_sessions`
- [x] Rodar e ver falhar
- [x] Ajustar apenas a fiação, se necessário, para o fluxo passar
- [x] Rodar `integration` e `unit`, ver passar
- [x] Commit
- commit: c0b9faa
---

## Refactor: estrutura de arquivos (mudança pedida no VERIFY, retry 1)

Premissa: `knowledge/guides/commons/project-structure-general.md` e `backend/structure-guide-backend.md`. Só caminhos mudam: nomes de teste, comportamento e caminhos públicos (`application::X`, `domain::X`) ficam iguais por reexport. Baseline: `nextest list` de unit e integration antes de começar; depois de cada crate o conjunto de testes (nome do teste, sem o caminho do módulo) tem de ser idêntico.

Layout de destino (um item por arquivo, `<nome>.<tipo>.rs`, teste em `__tests__/<nome>.<tipo>.test.rs`):
- `domain`: `entities/` (`attempt`), `value_objects/` (`access_code`, `app_version`, `attempt_id`, `display_name`, `document_version`, `email`, `session_id`, `session_policy`, `user_id`), `errors/` (`domain.error`).
- `application`: `repositories/` (`login_request`, `pending_signup`, `user`, `session`, `attempt`), `ports/` (`clock`, `id_generator`, `secret_generator`, `token_hasher`, `terms_policy`, `email_sender`, `version_provider`), `usecases/` (`get_health`, `request_access`, `verify_access`, `complete_signup`, `accept_terms`, `session_service`, `sync_progress`, `record_attempt`), `errors/` (`port.error`); `settings.rs` fica na raiz como singleton de configuração.
- `adapters-postgres`: `repositories/` (`login_request`, `pending_signup`, `user`, `session`, `attempt`); raiz: `lib.rs`, `error.rs`, `database.rs`, `pg_store.rs`.
- `adapters-http`: `controllers/` (um por rota), `dtos/`, `middlewares/` (`require_session`); raiz: `lib.rs`, `router.rs`, `error.rs`, `openapi.rs`, `state.rs`, `cookie.rs`, `client_ip.rs`, `json.rs`, `user_agent_label.rs`.
- `bootstrap`: arquivos planos em `src/` (`config`, `wiring`, `cargo_version`, `system_clock`, `os_id_generator`, `os_secret_generator`, `hmac_hasher`, `env_terms_policy`, `log_email_sender`, `background_email_sender`); `bin/migrate.rs` e `main.rs` ficam.

### Task R1: domain
- layer: domain
- repo: medsafari
- depends_on: [17]
- covers: AC-03, AC-04, AC-17, AC-19, AC-21, AC-22, AC-33, BR-05, BR-11, BR-13, BR-15, BR-24 (inalterado)
- test_scope: unit
- files: `crates/domain/src/{entities,value_objects,errors}/*`; testes em `*/__tests__/*.test.rs`
- verify: `cargo nextest run --workspace --profile unit` e `nextest list` igual ao baseline
- commit: refactor(domain): split into kind folders and move unit tests to __tests__
- [x] split
- [x] unit igual ao baseline
- [x] commit
- commit: 6295a6a
### Task R2: application
- layer: application
- repo: medsafari
- depends_on: [R1]
- test_scope: unit
- files: `crates/application/src/{repositories,ports,usecases,errors}/*`; testes em `*/__tests__/*.test.rs`
- commit: refactor(application): split ports.rs and use cases into kind folders and move unit tests to __tests__
- [x] split
- [x] unit igual ao baseline
- [x] commit
- commit: 099f24a
### Task R3: adapters-postgres
- layer: adapters-postgres
- repo: medsafari
- depends_on: [R2]
- test_scope: unit+integration
- files: `crates/adapters-postgres/src/repositories/*`, `database.rs`, `pg_store.rs`; sem teste unitário (integração fica em `tests/`)
- commit: refactor(adapters-postgres): split repositories into one file per port
- [x] split
- [x] unit e integration iguais ao baseline
- [x] commit
- commit: 528ff08
### Task R4: adapters-http
- layer: adapters-http
- repo: medsafari
- depends_on: [R3]
- test_scope: unit
- files: `crates/adapters-http/src/{controllers,dtos,middlewares}/*`, `router.rs`, `user_agent_label.rs`; testes em `*/__tests__/*.test.rs`
- commit: refactor(adapters-http): split handlers and dtos into kind folders and move unit tests to __tests__
- [x] split
- [x] unit igual ao baseline
- [x] commit
- commit: d6a04bb
### Task R5: bootstrap
- layer: bootstrap
- repo: medsafari
- depends_on: [R4]
- test_scope: unit+integration
- files: `crates/bootstrap/src/*.rs` (um item por arquivo); testes em `src/__tests__/*.test.rs`
- commit: refactor(bootstrap): split infra adapters and wiring into one file per item
- [x] split
- [x] unit e integration iguais ao baseline
- [x] commit
- commit: bb27330
---

## Configuração por dotenv (mudança pedida no VERIFY, retry 2)

Pedido: tirar valores fixos do código e guardar a configuração e os segredos num `.env` (fora do git). A API passa a ler `LISTEN_ADDR` (padrão `127.0.0.1:3000`) e carrega o `.env` sem alterar o ambiente do processo; variável de ambiente de verdade tem precedência sobre o arquivo. Os limites de negócio (`AuthSettings`), o pool e o contrato com o frontend continuam como padrões no código.

### Task 18: dotenv e LISTEN_ADDR
- layer: bootstrap
- repo: medsafari
- depends_on: [R5]
- covers: sem AC/BR novos; mantém `ac_02_br_01_listens_on_127_0_0_1_3000`
- test_scope: unit
- files: `crates/bootstrap/src/dotenv.rs` + `src/__tests__/dotenv.test.rs`; `config.rs` + `src/__tests__/config.test.rs`; `lib.rs`, `main.rs`, `bin/migrate.rs`; `backend/.env.example`, `backend/dev/init-env.sh`, `backend/dev/db.sh`
- verify: `cargo nextest run --workspace --profile unit`, `cargo clippy --workspace --all-targets -- -D warnings`, e subir a API de verdade com um `.env`
- commit: feat(bootstrap): read configuration from .env and make LISTEN_ADDR configurable
- [x] testes novos falham (RED)
- [x] implementar
- [x] unit verde
- [x] subir a API com `.env` e conferir `/api/health`
- [x] commit
- commit: 01ab7b1
---

## Self-review

- **Cobertura:** AC-01 a AC-33 e BR-01 a BR-24 aparecem em tarefas (BR-02 em T3/T5/T16; BR-20 em T6/T13; BR-21 em T6/T7; BR-23 em T4; BR-24 em T1/T5/T13). WD-01 a WD-10 do spec mapeiam para T1-T2 (WD-01), T3 (WD-02), T5-T7 (WD-03), T4 e T7 (WD-04), T8 (WD-05), T9 (WD-06), T9-T11 (WD-07), T12-T14 (WD-08), T15 (WD-09), T16-T17 (WD-10).
- **Consistência de tipos:** `Principal`, `IssuedSession`, `TermsVersions`, `AcceptedTerms`, `AuthSettings` e as portas nascem nas T3/T4 e são só consumidas depois.
- **Decisões novas deste plano (sem INF no spec):** limite de 1000 tentativas por lote; cookie montado à mão (sem `axum-extra`); filtro `binary(auth_flow)` no perfil `integration`.
