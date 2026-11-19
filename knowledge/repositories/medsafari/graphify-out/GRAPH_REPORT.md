# Graph Report - medsafari  (2026-11-19)

## Corpus Check
- 181 files · ~27,153 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 13 file(s) not represented in the graph (top: (none) 6, .toml 2, .css 2)

## Summary
- 1383 nodes · 3507 edges · 75 communities (51 shown, 24 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 164 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `01ab7b12`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- frontend
- openapi.rs
- biome.json
- openapi.test.rs
- auth_flow.rs
- clippy
- architecture.rs
- scripts
- Frontend
- application
- CLAUDE.md
- .claude/CLAUDE.md
- README.md
- accounts.rs
- test_support.rs
- health.controller.test.rs
- config.test.rs
- PortError
- complete_signup.usecase.test.rs
- LoginRequestRepository
- UserId
- session_service.usecase.test.rs
- request_access.usecase.test.rs
- verify_access.usecase.test.rs
- SessionId
- Clock
- verify_access.controller.test.rs
- router.rs
- AttemptId
- verify_access.usecase.rs
- client_ip.rs
- SessionService
- sync_progress.usecase.test.rs
- cookie.rs
- ApiError
- signup.controller.test.rs
- TermsVersions
- session_service.usecase.rs
- app.ts
- accept_terms.usecase.test.rs
- AuthApi
- Principal
- record_attempt.usecase.test.rs
- verify_access.controller.rs
- TokenHasher
- dependencies
- hmac_hasher.rs
- statuscode
- dotenv.test.rs
- datetime
- arc
- require_session.middleware.rs
- error.test.rs
- OsIdGenerator
- access_request.controller.rs
- duration
- logout_all.controller.rs
- cookie.test.rs
- db.sh
- hmac_hasher.test.rs
- label
- init-env.sh

## God Nodes (most connected - your core abstractions)
1. `PortError` - 84 edges
2. `UserId` - 51 edges
3. `ApiError` - 47 edges
4. `Email` - 42 edges
5. `AuthApi` - 37 edges
6. `Ports` - 36 edges
7. `SessionId` - 31 edges
8. `authed()` - 28 edges
9. `TermsVersions` - 26 edges
10. `Clock` - 25 edges

## Surprising Connections (you probably didn't know these)
- `ac_13_br_20_get_on_verify_route_is_405()` --calls--> `auth_router()`  [INFERRED]
  backend/crates/adapters-http/src/__tests__/router.test.rs → backend/crates/adapters-http/src/router.rs
- `ac_33_br_19_attempt_accepts_any_question_id()` --references--> `AttemptId`  [INFERRED]
  backend/crates/domain/src/entities/__tests__/attempt.entity.test.rs → backend/crates/domain/src/value_objects/attempt_id.value_object.rs
- `ac_07_br_09_unknown_when_nothing_identifies_the_client()` --calls--> `resolve()`  [INFERRED]
  backend/crates/adapters-http/src/__tests__/client_ip.test.rs → backend/crates/adapters-http/src/client_ip.rs
- `ac_20_br_10_clear_cookie_expires_in_the_past()` --calls--> `clear()`  [INFERRED]
  backend/crates/adapters-http/src/__tests__/cookie.test.rs → backend/crates/adapters-http/src/cookie.rs
- `body_of()` --references--> `ApiError`  [INFERRED]
  backend/crates/adapters-http/src/__tests__/error.test.rs → backend/crates/adapters-http/src/error.rs

## Import Cycles
- 1-file cycle: `backend/crates/adapters-http/src/router.rs -> backend/crates/adapters-http/src/router.rs`
- 2-file cycle: `backend/crates/bootstrap/src/config.rs -> backend/crates/bootstrap/src/dotenv.rs -> backend/crates/bootstrap/src/config.rs`

## Communities (75 total, 24 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.13
Nodes (21): devDependencies, @angular/build@^22.2.7, @angular/cli@^22.2.7, @angular/compiler-cli@^22.2.0, @biomejs/biome@2.6.7, jsdom@^30.0.0, prettier@^3.8.1, typescript@~6.0.2 (+13 more)

### Community 1 - "frontend"
Cohesion: 0.05
Nodes (38): build, serve, test, builder, configurations, defaultConfiguration, options, cli (+30 more)

### Community 3 - "openapi.rs"
Cohesion: 0.07
Nodes (20): AcceptTermsBody, AcceptedResponse, AccessRequestBody, AttemptDto, invalid_request(), to_attempt(), to_dto(), SessionResponse (+12 more)

### Community 4 - "biome.json"
Cohesion: 0.09
Nodes (22): source, assist, actions, enabled, files, ignoreUnknown, formatter, enabled (+14 more)

### Community 5 - "openapi.test.rs"
Cohesion: 0.06
Nodes (38): ac_02_br_04_access_response_is_identical_for_sent_and_rate_limited(), ac_04_br_24_invalid_email_is_422_invalid_email_format(), app(), body_of(), content_type(), limited_ports(), post(), sending_ports() (+30 more)

### Community 6 - "auth_flow.rs"
Cohesion: 0.08
Nodes (26): Config, DEFAULT_APP_BASE_URL, DEFAULT_LISTEN_ADDR, EmailProvider, DevLog, MIN_SECRET_LEN, main(), OsSecretGenerator (+18 more)

### Community 7 - "clippy"
Cohesion: 0.12
Nodes (15): glob, root, run, clippy, fmt, unit, glob, root (+7 more)

### Community 8 - "architecture.rs"
Cohesion: 0.27
Nodes (5): ac_04_br_02_layers_only_depend_inward(), ac_04_br_03_domain_has_no_framework_or_runtime_dependency(), ac_13_br_11_postgres_adapter_depends_only_inward(), ALLOWED, direct_dependencies()

### Community 9 - "scripts"
Cohesion: 0.22
Nodes (9): scripts, build, check, format, lint, ng, start, test (+1 more)

### Community 10 - "Frontend"
Cohesion: 0.25
Nodes (7): Additional Resources, Building, Code scaffolding, Development server, Frontend, Running end-to-end tests, Running unit tests

### Community 11 - "application"
Cohesion: 0.90
Nodes (5): adapters-http, adapters-postgres, application, bootstrap, domain

### Community 15 - "accounts.rs"
Cohesion: 0.05
Nodes (72): ACQUIRE_TIMEOUT, applied_migrations(), connect(), connect_lazy(), MAX_CONNECTIONS, migrate(), PgStore, ac_15_br_01_concurrent_create_for_same_email_yields_one_user() (+64 more)

### Community 16 - "test_support.rs"
Cohesion: 0.06
Nodes (47): ac_27_br_13_accept_terms_with_old_version_is_422(), ac_27_br_14_accept_terms_returns_204_even_when_terms_are_pending(), ac_27_br_14_accept_terms_without_session_is_401(), app(), ac_25_br_12_logout_all_returns_204(), app(), ac_24_br_12_logout_clears_cookie_and_returns_204(), ac_24_br_12_second_logout_with_same_cookie_is_401() (+39 more)

### Community 17 - "health.controller.test.rs"
Cohesion: 0.06
Nodes (27): ac_01_br_01_health_returns_200_with_ok_and_version(), ac_03_br_05_empty_version_is_problem_json(), ac_03_br_05_health_failure_is_problem_json_without_cause(), ac_08_br_05_error_body_has_problem_fields(), app(), content_type(), failing_provider(), json_body() (+19 more)

### Community 18 - "config.test.rs"
Cohesion: 0.10
Nodes (23): ConfigError, DotEnv, InvalidEnv, InvalidListenAddr, Missing, NoEmailProvider, SecretTooShort, Env (+15 more)

### Community 19 - "PortError"
Cohesion: 0.12
Nodes (12): PgStore, PortError, Infra, EmailSender, code_hash_input(), RequestAccessError, Infra, InvalidEmail (+4 more)

### Community 20 - "complete_signup.usecase.test.rs"
Cohesion: 0.14
Nodes (15): ac_15_br_01_second_use_of_signup_token_is_gone(), ac_15_br_01_signup_creates_user_acceptances_and_session(), ac_15_br_13_acceptance_records_version_time_and_ip_for_both_documents(), ac_16_br_21_no_signup_token_means_no_user(), ac_17_br_13_mismatched_version_creates_nothing_and_keeps_token(), ac_18_br_22_expired_signup_token_is_gone(), ac_19_br_15_display_name_over_80_chars_is_rejected_before_consuming(), ac_19_br_15_signup_without_display_name_is_valid() (+7 more)

### Community 21 - "LoginRequestRepository"
Cohesion: 0.11
Nodes (12): to_u32(), PgStore, VERIFY_CODE, CodeOutcome, Consumed, Gone, Wrong, ConsumeOutcome (+4 more)

### Community 22 - "UserId"
Cohesion: 0.16
Nodes (11): document_name(), insert_acceptances(), PgStore, user_from_row(), Acceptance, Document, Privacy, Terms (+3 more)

### Community 23 - "session_service.usecase.test.rs"
Cohesion: 0.18
Nodes (18): ac_20_br_10_issued_token_is_not_the_stored_hash(), ac_21_br_11_authenticate_extends_expiry_to_30_days(), ac_22_br_11_authenticate_rejects_session_past_90_days(), ac_22_br_11_authenticate_rejects_unknown_token(), ac_23_br_23_issue_stores_hash_and_label_not_the_token(), ac_24_br_12_logout_revokes_only_current_session(), ac_25_br_12_logout_all_revokes_every_session_of_user(), ac_26_br_14_get_returns_email_name_and_pending_flag() (+10 more)

### Community 24 - "request_access.usecase.test.rs"
Cohesion: 0.14
Nodes (11): ac_01_br_02_stores_only_hashes_of_token_and_code(), ac_01_br_03_sends_email_with_link_code_and_15_minutes(), ac_02_br_04_result_is_ok_for_sent_and_for_rate_limited(), ac_03_br_05_normalizes_email_before_counting_and_storing(), ac_04_br_24_invalid_email_is_rejected_without_sending(), ac_05_br_08_invalidates_open_requests_before_inserting(), ac_06_br_09_eleventh_request_in_a_day_is_silent_ok(), ac_06_br_09_fourth_request_in_15_minutes_is_silent_ok() (+3 more)

### Community 25 - "verify_access.usecase.test.rs"
Cohesion: 0.20
Nodes (18): ac_08_br_03_token_for_existing_user_issues_session(), ac_09_br_03_code_for_existing_user_issues_session(), ac_10_br_06_gone_when_token_already_consumed(), ac_11_br_06_gone_when_request_expired(), ac_12_br_07_fifth_wrong_code_is_gone_even_with_right_code(), ac_12_br_07_malformed_code_is_invalid_without_counting(), ac_12_br_07_wrong_code_reports_remaining_attempts(), ac_12_br_24_invalid_email_on_code_path_is_rejected() (+10 more)

### Community 26 - "SessionId"
Cohesion: 0.17
Nodes (7): record(), infra(), PgStore, NewSession, SessionRecord, SessionRepository, SessionId

### Community 27 - "Clock"
Cohesion: 0.14
Nodes (12): Clock, AttemptRepository, RecordAttempt, RecordOutcome, AlreadyExisted, Created, ProgressError, Infra (+4 more)

### Community 28 - "verify_access.controller.test.rs"
Cohesion: 0.28
Nodes (17): ac_08_br_06_verify_token_sets_session_cookie_without_token_in_body(), ac_08_br_06_verify_without_credential_is_422(), ac_09_br_06_verify_code_returns_authenticated(), ac_10_br_06_used_token_is_410(), ac_11_br_06_expired_code_is_410(), ac_12_br_07_malformed_code_is_422_without_attempts_remaining(), ac_12_br_07_wrong_code_is_422_with_attempts_remaining(), ac_14_br_09_ip_limit_is_429() (+9 more)

### Community 29 - "router.rs"
Cohesion: 0.18
Nodes (7): health(), session_info(), HealthResponse, Problem, auth_router(), router(), GetHealth

### Community 30 - "AttemptId"
Cohesion: 0.16
Nodes (3): PgStore, Attempt, AttemptId

### Community 31 - "verify_access.usecase.rs"
Cohesion: 0.16
Nodes (14): Credential, Code, Token, VerifyAccess, VerifyError, Gone, Infra, InvalidCode (+6 more)

### Community 32 - "client_ip.rs"
Cohesion: 0.18
Nodes (7): resolve(), ac_07_br_09_falls_back_to_socket_when_header_is_missing_or_blank(), ac_07_br_09_header_is_ignored_when_not_configured(), ac_07_br_09_trusted_header_is_used_when_configured(), ac_07_br_09_unknown_when_nothing_identifies_the_client(), headers(), socket()

### Community 33 - "SessionService"
Cohesion: 0.26
Nodes (7): IdGenerator, TermsPolicy, PendingSignupRepository, UserRepository, AcceptTerms, CompleteSignup, SessionService

### Community 34 - "sync_progress.usecase.test.rs"
Cohesion: 0.30
Nodes (14): ac_26_br_14_sync_refused_when_terms_pending(), ac_28_br_16_batch_of_exactly_1000_is_accepted(), ac_28_br_16_batch_over_1000_is_rejected(), ac_28_br_16_duplicate_attempt_id_in_one_batch_counts_once(), ac_28_br_16_sync_inserts_new_attempts_and_returns_full_list(), ac_28_br_16_sync_with_empty_list_returns_account_progress(), ac_29_br_16_sync_with_same_attempts_adds_nothing(), ac_30_br_17_sync_returns_attempts_of_account_not_only_sent() (+6 more)

### Community 35 - "cookie.rs"
Cohesion: 0.18
Nodes (7): logout(), ATTRIBUTES, clear(), NAME, read(), set(), ac_20_br_10_clear_cookie_expires_in_the_past()

### Community 36 - "ApiError"
Cohesion: 0.26
Nodes (11): signup_error(), verify_error(), ApiError, Internal, Problem, invalid_code(), invalid_email(), progress_error() (+3 more)

### Community 38 - "signup.controller.test.rs"
Cohesion: 0.35
Nodes (11): ac_15_br_13_signup_returns_201_and_cookie(), ac_16_br_22_signup_with_expired_token_is_410(), ac_17_br_13_signup_with_old_version_is_422(), ac_19_br_13_signup_without_display_name_is_201(), ac_19_br_15_signup_with_81_char_display_name_is_422(), app(), body_of(), email() (+3 more)

### Community 39 - "TermsVersions"
Cohesion: 0.19
Nodes (7): TermsVersions, acceptances(), AcceptedTerms, TermsError, Infra, VersionMismatch, EnvTermsPolicy

### Community 40 - "session_service.usecase.rs"
Cohesion: 0.16
Nodes (10): SignupError, Gone, Infra, InvalidDisplayName, VersionMismatch, IssuedSession, SessionError, Infra (+2 more)

### Community 41 - "app.ts"
Cohesion: 0.20
Nodes (8): @angular/common@^22.2.0, Health, HealthService, App, appConfig, @angular/common, @angular/core, rxjs

### Community 42 - "accept_terms.usecase.test.rs"
Cohesion: 0.28
Nodes (8): ac_27_br_13_accept_terms_rejects_old_version(), ac_27_br_14_accept_terms_records_current_versions(), accept_service(), accepted(), NOW, principal(), shared(), versions()

### Community 43 - "AuthApi"
Cohesion: 0.29
Nodes (4): ClientIp, accept_terms(), signup(), AuthApi

### Community 44 - "Principal"
Cohesion: 0.26
Nodes (4): record_attempt(), sync_progress(), ApiJson, Principal

### Community 45 - "record_attempt.usecase.test.rs"
Cohesion: 0.34
Nodes (10): ac_26_br_14_record_refused_when_terms_pending(), ac_31_br_18_record_creates_attempt(), ac_32_br_18_record_twice_reports_already_existed(), ac_33_br_19_record_does_not_check_question_existence(), attempt(), clock(), NOW, principal() (+2 more)

### Community 46 - "verify_access.controller.rs"
Cohesion: 0.26
Nodes (4): rfc3339(), verify(), UNKNOWN, user_agent()

### Community 47 - "TokenHasher"
Cohesion: 0.23
Nodes (4): SecretGenerator, TokenHasher, AuthSettings, RequestAccess

### Community 48 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @angular/compiler@^22.2.0, @angular/core@^22.2.0, @angular/forms@^22.2.0, @angular/platform-browser@^22.2.0, @angular/router@^22.2.0, rxjs@~7.8.0, tslib@^2.3.0 (+5 more)

### Community 49 - "hmac_hasher.rs"
Cohesion: 0.24
Nodes (3): decode_hex(), HmacHasher, HmacSha256

### Community 51 - "dotenv.test.rs"
Cohesion: 0.27
Nodes (5): ac_01_br_02_dotenv_reads_values_comments_quotes_and_export(), ac_01_br_02_dotenv_unknown_key_is_none(), ac_01_br_02_process_env_wins_over_the_file(), env(), FILE

### Community 53 - "arc"
Cohesion: 0.28
Nodes (5): GetHealthError, Version, Health, HealthStatus, Ok

### Community 55 - "error.test.rs"
Cohesion: 0.39
Nodes (4): ac_02_br_04_internal_error_does_not_leak_cause(), ac_04_br_24_problem_json_has_type_title_status_detail(), ac_12_br_07_problem_can_carry_attempts_remaining(), body_of()

### Community 61 - "cookie.test.rs"
Cohesion: 0.53
Nodes (3): ac_20_br_10_read_cookie_ignores_empty_and_garbage(), ac_20_br_10_read_cookie_returns_the_session_value(), cookies()

### Community 62 - "db.sh"
Cohesion: 0.60
Nodes (5): exists(), print_env(), running(), db.sh script, wait_ready()

### Community 66 - "label"
Cohesion: 0.67
Nodes (3): ac_23_br_23_label_falls_back_when_unknown(), ac_23_br_23_label_names_browser_and_system(), label()

## Knowledge Gaps
- **46 isolated node(s):** `Authenticated`, `TermsRequired`, `Internal`, `Infra`, `Unavailable` (+41 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 290 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortError` connect `PortError` to `SessionService`, `auth_flow.rs`, `TermsVersions`, `session_service.usecase.rs`, `TokenHasher`, `test_support.rs`, `LoginRequestRepository`, `UserId`, `SessionId`, `Clock`, `AttemptId`, `verify_access.usecase.rs`?**
  _High betweenness centrality (0.060) - this node is a cross-community bridge._
- **Are the 11 inferred relationships involving `UserId` (e.g. with `ac_27_br_14_accept_terms_returns_204_even_when_terms_are_pending()` and `ac_25_br_12_logout_all_returns_204()`) actually correct?**
  _`UserId` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Authenticated`, `TermsRequired`, `Internal` to the rest of the system?**
  _46 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.12554112554112554 - nodes in this community are weakly interconnected._
- **Why does `AuthApi` connect `AuthApi` to `client_ip.rs`, `SessionService`, `cookie.rs`, `auth_flow.rs`, `Principal`, `verify_access.controller.rs`, `TokenHasher`, `test_support.rs`, `require_session.middleware.rs`, `access_request.controller.rs`, `Clock`, `logout_all.controller.rs`, `router.rs`, `verify_access.usecase.rs`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Should `frontend` be split into smaller, more focused modules?**
  _Cohesion score 0.05398110661268556 - nodes in this community are weakly interconnected._
- **Why does `UserId` connect `UserId` to `SessionService`, `sync_progress.usecase.test.rs`, `TermsVersions`, `session_service.usecase.rs`, `accept_terms.usecase.test.rs`, `Principal`, `record_attempt.usecase.test.rs`, `accounts.rs`, `test_support.rs`, `complete_signup.usecase.test.rs`, `verify_access.usecase.test.rs`, `SessionId`, `verify_access.controller.test.rs`, `AttemptId`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._