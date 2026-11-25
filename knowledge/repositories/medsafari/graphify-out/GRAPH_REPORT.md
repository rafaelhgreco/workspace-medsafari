# Graph Report - medsafari  (2026-11-25)

## Corpus Check
- 585 files · ~88,733 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 20 file(s) not represented in the graph (top: (none) 7, .http 7, .toml 2)

## Summary
- 4012 nodes · 12022 edges · 349 communities (159 shown, 190 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 420 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ccf24a41`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- package.json
- frontend
- openapi.rs
- biome.json
- openapi.test.rs
- config.test.rs
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
- DocumentVersion
- Email
- .pool
- User
- request_access.usecase.test.rs
- PortError
- Problem
- DispatchNotification
- ApiError
- super
- app.ts
- privacy.controller.rs
- ApiJson
- header
- Clock
- dependencies
- HmacHasher
- statuscode
- dotenv.test.rs
- AttemptId
- health.controller.test.rs
- error.test.rs
- session_service.usecase.test.rs
- Principal
- db.sh
- verify_access.usecase.test.rs
- complete_signup.usecase.test.rs
- login_requests.rs
- init-env.sh
- verify_access.controller.test.rs
- sync_progress.controller.test.rs
- SessionId
- PortError
- SignupError
- AttemptRepository
- datetime
- Subir o backend e testar os endpoints
- TermsVersions
- sync_progress.usecase.test.rs
- signup.controller.test.rs
- accept_terms.usecase.test.rs
- VerifyError
- attempt.dto.rs
- ProfileError
- access_request.controller.test.rs
- uuid
- dtos
- confirm_institutional_code.usecase.test.rs
- session_policy.value_object.test.rs
- AccountApi
- decide_verification.usecase.test.rs
- account_test_support.rs
- wiring.rs
- auth_flow.rs
- PrivacyAppError
- AccessError
- submit_verification.usecase.test.rs
- bootstrap/tests/support/mod.rs
- badges.rs
- AccountPorts
- AccountStatus
- PgStore
- error
- jobs.test.rs
- test_db
- DecisionError
- VerificationAppError
- VerificationError
- CrmRegistration
- revoke_verification.usecase.test.rs
- verification.controller.test.rs
- Verification
- request_institutional_code.usecase.test.rs
- DataExportRepository
- account.rs
- LocalFileStorage
- router.rs
- verification_decision.controller.test.rs
- VerificationMethod
- request_data_export.usecase.test.rs
- uuid
- profile.controller.test.rs
- profile.dto.rs
- profiles.rs
- toschema
- institutional_email.controller.test.rs
- DisplayMode
- confirm_fraud.usecase.test.rs
- database.rs
- set_display_mode.usecase.test.rs
- BadgeType
- DomainRequest
- schedule_account_deletion.usecase.test.rs
- health.controller.test.rs
- Specialty
- AuthApi
- deactivate_account.usecase.test.rs
- preview_display.usecase.test.rs
- update_profile.usecase.test.rs
- StoredNotification
- reference.controller.rs
- data_export.controller.test.rs
- FlowProbe
- mark_notification_read.usecase.test.rs
- AuthorRecord
- get_public_author.usecase.test.rs
- resolve_author_display.usecase.test.rs
- verification.entity.test.rs
- versions
- AuthorDisplay
- verification_review.dto.rs
- json.test.rs
- Attempt
- progress.rs
- download_data_export.usecase.test.rs
- VerificationItemType
- get_verification_for_review.usecase.test.rs
- list_verification_queue.usecase.test.rs
- account.controller.test.rs
- privacy.controller.test.rs
- verification.controller.rs
- router.test.rs
- dispatch_notification.usecase.test.rs
- notification.controller.rs
- crm_registration.controller.test.rs
- verification.dto.rs
- adapters-postgres/src/modules/privacy/repositories/public_author.repository.rs
- Badge
- data_export.controller.rs
- account.dto.rs
- verification_review.controller.test.rs
- list_badges.usecase.test.rs
- list_my_verifications.usecase.test.rs
- wiring.test.rs
- author_display.entity.test.rs
- account.controller.rs
- add_residency.usecase.test.rs
- get_profile.usecase.test.rs
- evidence_file.value_object.test.rs
- notification.dto.rs
- public_author.controller.test.rs
- crm_registration.controller.rs
- postgraduate.controller.rs
- fraud.controller.test.rs
- institutional_email.controller.rs
- notifications.rs
- grant_badges_for_verification.usecase.test.rs
- postgraduate.controller.test.rs
- reference.controller.test.rs
- residency.controller.test.rs
- residency.dto.rs
- adapters-postgres/src/modules/verification/repositories/email_domain.repository.rs
- add_postgraduate.usecase.test.rs
- .check
- profile.entity.test.rs
- verification_decision.dto.rs
- reactivate_account.usecase.test.rs
- get_health.usecase.test.rs
- SessionPolicy
- PublicAuthorPage
- create-staff.sh

## God Nodes (most connected - your core abstractions)
1. `PortError` - 296 edges
2. `UserId` - 246 edges
3. `Principal` - 162 edges
4. `AccountStatus` - 133 edges
5. `ApiError` - 117 edges
6. `SessionId` - 104 edges
7. `Clock` - 97 edges
8. `DispatchNotification` - 91 edges
9. `Email` - 87 edges
10. `AccountPorts` - 86 edges

## Surprising Connections (you probably didn't know these)
- `list_notifications()` --references--> `NotificationQuery`  [INFERRED]
  backend/crates/adapters-http/src/modules/notifications/controllers/notification.controller.rs → backend/crates/adapters-http/src/modules/notifications/dtos/notification.dto.rs
- `list_universities()` --references--> `UniversityQuery`  [INFERRED]
  backend/crates/adapters-http/src/modules/profile/controllers/reference.controller.rs → backend/crates/adapters-http/src/modules/profile/dtos/reference.dto.rs
- `session_record()` --references--> `SessionId`  [INFERRED]
  backend/crates/adapters-http/src/account_test_support.rs → backend/crates/domain/src/modules/auth/value_objects/session_id.value_object.rs
- `ac_07_br_09_unknown_when_nothing_identifies_the_client()` --calls--> `resolve()`  [INFERRED]
  backend/crates/adapters-http/src/__tests__/client_ip.test.rs → backend/crates/adapters-http/src/client_ip.rs
- `body_of()` --references--> `ApiError`  [INFERRED]
  backend/crates/adapters-http/src/__tests__/error.test.rs → backend/crates/adapters-http/src/error.rs

## Import Cycles
- 1-file cycle: `backend/crates/adapters-http/src/router.rs -> backend/crates/adapters-http/src/router.rs`
- 2-file cycle: `backend/crates/domain/src/modules/verification/errors/verification.error.rs -> backend/crates/domain/src/modules/verification/value_objects/verification_status.value_object.rs -> backend/crates/domain/src/modules/verification/errors/verification.error.rs`
- 2-file cycle: `backend/crates/domain/src/modules/auth/errors/account.error.rs -> backend/crates/domain/src/modules/auth/value_objects/account_status.value_object.rs -> backend/crates/domain/src/modules/auth/errors/account.error.rs`
- 2-file cycle: `backend/crates/bootstrap/src/config.rs -> backend/crates/bootstrap/src/dotenv.rs -> backend/crates/bootstrap/src/config.rs`

## Communities (349 total, 190 thin omitted)

### Community 0 - "package.json"
Cohesion: 0.13
Nodes (21): devDependencies, @angular/build@^22.2.7, @angular/cli@^22.2.7, @angular/compiler-cli@^22.2.0, @biomejs/biome@2.6.7, jsdom@^30.0.0, prettier@^3.8.1, typescript@~6.0.2 (+13 more)

### Community 1 - "frontend"
Cohesion: 0.05
Nodes (38): build, serve, test, builder, configurations, defaultConfiguration, options, cli (+30 more)

### Community 4 - "biome.json"
Cohesion: 0.09
Nodes (22): source, assist, actions, enabled, files, ignoreUnknown, formatter, enabled (+14 more)

### Community 5 - "openapi.test.rs"
Cohesion: 0.31
Nodes (8): ac_01_br_01_openapi_describes_every_auth_and_progress_route(), ac_01_br_04_openapi_lists_auth_access_routes(), ac_07_br_06_openapi_describes_health(), app(), json_body(), openapi_doc(), provider_returning(), send()

### Community 6 - "config.test.rs"
Cohesion: 0.10
Nodes (25): ConfigError, DotEnv, InvalidEnv, InvalidListenAddr, Missing, NoEmailProvider, SecretTooShort, Env (+17 more)

### Community 7 - "clippy"
Cohesion: 0.12
Nodes (15): glob, root, run, clippy, fmt, unit, glob, root (+7 more)

### Community 8 - "architecture.rs"
Cohesion: 0.14
Nodes (17): ac_04_br_02_layers_only_depend_inward(), ac_04_br_03_domain_has_no_framework_or_runtime_dependency(), ac_13_br_11_postgres_adapter_depends_only_inward(), ALLOWED, ALLOWED_MODULE_EDGES, br_02_no_kind_folder_outside_modules_and_shared(), br_02_only_declared_root_files_stay_loose(), br_04_module_graph_has_no_cycle() (+9 more)

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
Cohesion: 0.21
Nodes (29): ac_15_br_01_concurrent_create_for_same_email_yields_one_user(), ac_15_br_01_create_user_and_acceptances_commit_together(), ac_15_br_01_find_by_email_and_by_id_return_the_user(), ac_15_br_13_failed_acceptance_rolls_back_the_user(), ac_21_br_11_touch_updates_last_used_and_expiry(), ac_22_br_11_find_active_ignores_unknown_and_revoked_sessions(), ac_22_br_11_find_active_rejects_session_at_90_days(), ac_23_br_23_session_keeps_creation_label_and_last_use() (+21 more)

### Community 16 - "test_support.rs"
Cohesion: 0.12
Nodes (7): ac_24_br_12_logout_clears_cookie_and_returns_204(), ac_24_br_12_second_logout_with_same_cookie_is_401(), app(), body_of(), NOW, Ports, send()

### Community 18 - "DocumentVersion"
Cohesion: 0.08
Nodes (11): EnvPublicDisplayTerms, AuthError, InvalidAccessCode, InvalidDisplayName, InvalidDocumentVersion, InvalidEmail, LEN, DisplayName (+3 more)

### Community 20 - "Email"
Cohesion: 0.14
Nodes (5): EmailSender, BackgroundEmailSender, LogEmailSender, OsSecretGenerator, AccessCode

### Community 21 - ".pool"
Cohesion: 0.08
Nodes (9): to_u32(), PgStore, PgStore, PgStore, stored(), PgStore, PgStore, PgStore (+1 more)

### Community 22 - "User"
Cohesion: 0.15
Nodes (9): document_name(), insert_acceptances(), PgStore, user_from_row(), Acceptance, Document, Privacy, Terms (+1 more)

### Community 24 - "request_access.usecase.test.rs"
Cohesion: 0.11
Nodes (21): ac_59_br_38_execute_deletes_files_then_erases_and_sends_final_email(), ac_59_br_38_execute_is_idempotent_when_the_file_is_already_gone(), br_38_execute_with_nothing_due_does_nothing(), clock(), dispatch(), due(), email_only(), NOW (+13 more)

### Community 26 - "PortError"
Cohesion: 0.09
Nodes (13): VERIFY_CODE, PgStore, CodeOutcome, Consumed, Gone, Wrong, ConsumeOutcome, Consumed (+5 more)

### Community 29 - "Problem"
Cohesion: 0.15
Nodes (5): Problem, accept_terms(), logout(), session_info(), health()

### Community 32 - "DispatchNotification"
Cohesion: 0.05
Nodes (42): AccountAppError, Access, EmailMismatch, Infra, Invalid, NotFound, Notify, TooSoon (+34 more)

### Community 36 - "ApiError"
Cohesion: 0.17
Nodes (27): access_error(), account_error(), ApiError, Internal, Problem, badges_error(), conflict(), decision_error() (+19 more)

### Community 41 - "app.ts"
Cohesion: 0.20
Nodes (8): @angular/common@^22.2.0, Health, HealthService, App, appConfig, @angular/common, @angular/core, rxjs

### Community 43 - "privacy.controller.rs"
Cohesion: 0.09
Nodes (16): AuthApi, ClientIp, resolve(), ACCESS_MESSAGE, access_request(), AcceptedResponse, AccessRequestBody, preview_display() (+8 more)

### Community 44 - "ApiJson"
Cohesion: 0.20
Nodes (7): ApiJson, record_attempt(), sync_progress(), approve_verification(), principal_is_staff(), reject_verification(), revoke_verification()

### Community 46 - "header"
Cohesion: 0.08
Nodes (19): ATTRIBUTES, clear(), NAME, read(), set(), logout_all(), signup(), rfc3339() (+11 more)

### Community 47 - "Clock"
Cohesion: 0.08
Nodes (21): PurgeExpiredExports, BadgesAppError, Access, Infra, BadgeRepository, ExpireStudentBadges, BadgeGrant, BadgeSpec (+13 more)

### Community 48 - "dependencies"
Cohesion: 0.15
Nodes (13): dependencies, @angular/compiler@^22.2.0, @angular/core@^22.2.0, @angular/forms@^22.2.0, @angular/platform-browser@^22.2.0, @angular/router@^22.2.0, rxjs@~7.8.0, tslib@^2.3.0 (+5 more)

### Community 49 - "HmacHasher"
Cohesion: 0.24
Nodes (3): decode_hex(), HmacHasher, HmacSha256

### Community 50 - "statuscode"
Cohesion: 0.11
Nodes (10): ApiJson<T>, Job, .ALL, ExecuteDeletions, ExpireBadges, PurgeEvidence, PurgeExports, WarnBadges (+2 more)

### Community 51 - "dotenv.test.rs"
Cohesion: 0.27
Nodes (5): ac_01_br_02_dotenv_reads_values_comments_quotes_and_export(), ac_01_br_02_dotenv_unknown_key_is_none(), ac_01_br_02_process_env_wins_over_the_file(), env(), FILE

### Community 52 - "AttemptId"
Cohesion: 0.42
Nodes (7): ac_26_br_14_record_with_terms_pending_is_403(), ac_31_br_18_record_new_attempt_is_201(), ac_32_br_18_record_existing_attempt_is_200(), ac_33_br_19_record_accepts_unknown_question_id(), accepted(), app(), attempt_json()

### Community 53 - "health.controller.test.rs"
Cohesion: 0.10
Nodes (15): VersionError, Invalid, Unavailable, VersionProvider, GetHealth, GetHealthError, Version, Health (+7 more)

### Community 55 - "error.test.rs"
Cohesion: 0.39
Nodes (4): ac_02_br_04_internal_error_does_not_leak_cause(), ac_04_br_24_problem_json_has_type_title_status_detail(), ac_12_br_07_problem_can_carry_attempts_remaining(), body_of()

### Community 59 - "session_service.usecase.test.rs"
Cohesion: 0.19
Nodes (19): ac_20_br_10_issued_token_is_not_the_stored_hash(), ac_21_br_11_authenticate_extends_expiry_to_30_days(), ac_22_br_11_authenticate_rejects_session_past_90_days(), ac_22_br_11_authenticate_rejects_unknown_token(), ac_23_br_23_issue_stores_hash_and_label_not_the_token(), ac_24_br_12_logout_revokes_only_current_session(), ac_25_br_12_logout_all_revokes_every_session_of_user(), ac_26_br_14_get_returns_email_name_and_pending_flag() (+11 more)

### Community 61 - "Principal"
Cohesion: 0.08
Nodes (17): SecretGenerator, TokenHasher, Principal, IssuedSession, SessionError, Infra, Unauthenticated, SessionService (+9 more)

### Community 62 - "db.sh"
Cohesion: 0.60
Nodes (5): exists(), print_env(), running(), db.sh script, wait_ready()

### Community 64 - "verify_access.usecase.test.rs"
Cohesion: 0.18
Nodes (22): ac_08_br_03_token_for_existing_user_issues_session(), ac_09_br_03_code_for_existing_user_issues_session(), ac_10_br_06_gone_when_token_already_consumed(), ac_11_br_06_gone_when_request_expired(), ac_12_br_07_fifth_wrong_code_is_gone_even_with_right_code(), ac_12_br_07_malformed_code_is_invalid_without_counting(), ac_12_br_07_wrong_code_reports_remaining_attempts(), ac_12_br_24_invalid_email_on_code_path_is_rejected() (+14 more)

### Community 65 - "complete_signup.usecase.test.rs"
Cohesion: 0.21
Nodes (15): ac_15_br_01_second_use_of_signup_token_is_gone(), ac_15_br_01_signup_creates_user_acceptances_and_session(), ac_15_br_13_acceptance_records_version_time_and_ip_for_both_documents(), ac_16_br_21_no_signup_token_means_no_user(), ac_17_br_13_mismatched_version_creates_nothing_and_keeps_token(), ac_18_br_22_expired_signup_token_is_gone(), ac_19_br_15_display_name_over_80_chars_is_rejected_before_consuming(), ac_19_br_15_signup_without_display_name_is_valid() (+7 more)

### Community 66 - "login_requests.rs"
Cohesion: 0.29
Nodes (20): ac_05_br_08_new_request_invalidates_open_ones_of_same_email(), ac_06_br_09_counts_by_email_window_ignore_older_rows(), ac_07_br_09_counts_by_ip_in_last_hour(), ac_10_br_06_consume_returns_the_requested_email(), ac_10_br_06_token_consumed_once_even_in_parallel(), ac_10_br_06_using_the_code_invalidates_the_link(), ac_10_br_06_using_the_link_invalidates_the_code(), ac_11_br_06_request_expires_at_the_boundary() (+12 more)

### Community 71 - "verify_access.controller.test.rs"
Cohesion: 0.26
Nodes (19): ac_08_br_06_verify_token_sets_session_cookie_without_token_in_body(), ac_08_br_06_verify_without_credential_is_422(), ac_09_br_06_verify_code_returns_authenticated(), ac_10_br_06_used_token_is_410(), ac_11_br_06_expired_code_is_410(), ac_12_br_07_malformed_code_is_422_without_attempts_remaining(), ac_12_br_07_wrong_code_is_422_with_attempts_remaining(), ac_14_br_09_ip_limit_is_429() (+11 more)

### Community 75 - "sync_progress.controller.test.rs"
Cohesion: 0.26
Nodes (16): ac_26_br_14_sync_with_terms_pending_is_403(), ac_28_br_16_attempt_with_bad_timestamp_or_blank_fields_is_422(), ac_28_br_16_sync_over_1000_attempts_is_422(), ac_28_br_16_sync_returns_full_progress(), ac_28_br_16_sync_without_session_is_401(), ac_28_br_16_unknown_schema_version_is_422(), ac_29_br_16_sync_repeated_returns_same_total(), ac_30_br_17_sync_with_empty_list_returns_account_attempts() (+8 more)

### Community 76 - "SessionId"
Cohesion: 0.12
Nodes (16): record(), NewSession, SessionRecord, SessionRepository, br_06_lists_specialties(), br_35_listing_specialties_rejects_deactivated_account(), principal(), br_05_search_clamps_the_limit_to_50() (+8 more)

### Community 77 - "PortError"
Cohesion: 0.04
Nodes (16): PgStore, PgStore, stored(), PgStore, stored(), stored(), INSERT_MANY, PgStore (+8 more)

### Community 78 - "SignupError"
Cohesion: 0.40
Nodes (5): SignupError, Gone, Infra, InvalidDisplayName, VersionMismatch

### Community 79 - "AttemptRepository"
Cohesion: 0.19
Nodes (9): AttemptRepository, RecordAttempt, RecordOutcome, AlreadyExisted, Created, ProgressError, Infra, TermsPending (+1 more)

### Community 80 - "datetime"
Cohesion: 0.10
Nodes (23): ac_25_br_12_logout_all_returns_204(), app(), ac_67_br_42_notifications_default_to_twenty(), ac_67_br_42_notifications_list_with_kind_payload_and_read_state(), ac_69_br_42_mark_read_returns_204_and_404_for_someone_elses(), app(), br_35_notifications_are_403_for_a_deactivated_account(), signed_in() (+15 more)

### Community 81 - "Subir o backend e testar os endpoints"
Cohesion: 0.08
Nodes (24): Convenções, Roteiros de requisição da API, Ver o fluxo inteiro, com o selo, 10. Rodar os testes, 11. Encerrar, 12. Problemas comuns, 13. Perfil, selos e conta (módulo 02), 14. Conta de equipe e fila de verificação (+16 more)

### Community 82 - "TermsVersions"
Cohesion: 0.15
Nodes (9): TermsPolicy, TermsVersions, acceptances(), AcceptedTerms, TermsError, Infra, VersionMismatch, SessionView (+1 more)

### Community 83 - "sync_progress.usecase.test.rs"
Cohesion: 0.15
Nodes (24): ac_26_br_14_record_refused_when_terms_pending(), ac_31_br_18_record_creates_attempt(), ac_32_br_18_record_twice_reports_already_existed(), ac_33_br_19_record_does_not_check_question_existence(), attempt(), clock(), NOW, principal() (+16 more)

### Community 84 - "signup.controller.test.rs"
Cohesion: 0.35
Nodes (11): ac_15_br_13_signup_returns_201_and_cookie(), ac_16_br_22_signup_with_expired_token_is_410(), ac_17_br_13_signup_with_old_version_is_422(), ac_19_br_13_signup_without_display_name_is_201(), ac_19_br_15_signup_with_81_char_display_name_is_422(), app(), body_of(), email() (+3 more)

### Community 85 - "accept_terms.usecase.test.rs"
Cohesion: 0.28
Nodes (8): ac_27_br_13_accept_terms_rejects_old_version(), ac_27_br_14_accept_terms_records_current_versions(), accept_service(), accepted(), NOW, principal(), shared(), versions()

### Community 86 - "VerifyError"
Cohesion: 0.13
Nodes (14): Credential, Code, Token, VerifyError, AccountSuspended, Gone, Infra, InvalidCode (+6 more)

### Community 87 - "attempt.dto.rs"
Cohesion: 0.30
Nodes (7): AttemptDto, invalid_request(), to_attempt(), to_dto(), SCHEMA_VERSION, SyncBody, SyncResponse

### Community 88 - "ProfileError"
Cohesion: 0.05
Nodes (42): profile_from_row(), year(), Postgraduate, PostgraduateKind, Doutorado, Mestrado, Profile, UniversityRef (+34 more)

### Community 89 - "access_request.controller.test.rs"
Cohesion: 0.40
Nodes (8): ac_02_br_04_access_response_is_identical_for_sent_and_rate_limited(), ac_04_br_24_invalid_email_is_422_invalid_email_format(), app(), body_of(), content_type(), limited_ports(), post(), sending_ports()

### Community 90 - "uuid"
Cohesion: 0.36
Nodes (5): ac_20_br_10_garbage_cookie_is_401_not_500(), ac_20_br_10_session_without_cookie_is_401(), ac_21_br_11_authenticated_request_renews_the_session(), ac_22_br_11_expired_session_is_401(), app()

### Community 92 - "confirm_institutional_code.usecase.test.rs"
Cohesion: 0.06
Nodes (50): ac_10_br_12_replace_invalidates_the_previous_challenge_and_used_ones_are_closed(), ac_10_br_12_university_for_domain_lookup(), ac_11_br_12_challenge_attempts_never_go_back(), ac_13_br_43_domain_request_is_recorded(), ac_13_br_43_recent_requests_group_by_domain_most_asked_first(), ac_14_br_07_find_open_returns_only_pending(), ac_14_br_07_insert_and_list_for_user(), ac_19_br_15_concurrent_crm_approval_leaves_one_verified() (+42 more)

### Community 95 - "AccountApi"
Cohesion: 0.05
Nodes (30): AccountApi, ClientIpSource, IdGenerator, ProfileAppError, Access, ConflictingUniversity, Duplicate, Infra (+22 more)

### Community 96 - "decide_verification.usecase.test.rs"
Cohesion: 0.14
Nodes (40): ac_15_br_17_crm_approval_locks_name_and_grants_doctor_badge(), ac_16_br_14_non_active_crm_is_refused(), ac_17_br_19_approval_with_rqe_grants_specialist(), ac_18_br_19_title_approval_grants_specialist(), ac_18_br_19_title_approval_needs_the_specialty(), ac_19_br_15_a_conflict_that_appeared_after_submission_blocks_approval(), ac_19_br_15_conflict_blocks_approval(), ac_20_br_16_name_mismatch_blocks_approval() (+32 more)

### Community 97 - "account_test_support.rs"
Cohesion: 0.15
Nodes (22): StaffApi, CrmRegistrationRepository, PostgraduateRepository, ProfileRepository, ResidencyRepository, GetProfile, SuspensionRepository, VerificationRepository (+14 more)

### Community 212 - "wiring.rs"
Cohesion: 0.19
Nodes (15): main(), usage(), Config, DEFAULT_APP_BASE_URL, DEFAULT_LISTEN_ADDR, DEFAULT_STORAGE_DIR, EmailProvider, DevLog (+7 more)

### Community 213 - "auth_flow.rs"
Cohesion: 0.19
Nodes (21): ac_53_br_35_deactivate_then_reactivate_end_to_end(), ac_58_br_37_login_cancels_scheduled_deletion(), ac_59_br_38_deletion_job_erases_personal_data_and_keeps_acceptances(), ac_65_br_41_export_rate_limit_end_to_end(), ac_08_br_16_login_in_second_browser_sums_attempts_without_duplicates(), ac_10_br_06_link_can_only_be_used_once_end_to_end(), ac_15_br_01_visitor_signs_up_and_keeps_progress(), ac_25_br_12_logout_all_invalidates_both_sessions() (+13 more)

### Community 221 - "PrivacyAppError"
Cohesion: 0.11
Nodes (16): PrivacyAppError, Access, ConsentRequired, Infra, NotFound, PublicDisplayTermsPolicy, PublishedQuestionsCounter, DisplayConsentRepository (+8 more)

### Community 222 - "AccessError"
Cohesion: 0.07
Nodes (14): AccessError, AccountNotActive, NotStaff, NotificationAppError, Access, Infra, NotFound, NotificationRepository (+6 more)

### Community 223 - "submit_verification.usecase.test.rs"
Cohesion: 0.14
Nodes (25): ac_11_br_11_student_enrollment_proof_uses_the_user_id_as_item(), ac_14_br_07_submit_creates_pending_and_notifies(), ac_19_br_15_submit_marks_conflict_when_crm_verified_elsewhere(), ac_24_br_20_residency_submission_is_pending(), ac_24_br_20_residency_submission_needs_the_declaration_date(), ac_26_br_21_postgraduate_submission_is_pending(), ac_28_br_22_submit_rejects_invalid_file(), account_user() (+17 more)

### Community 224 - "bootstrap/tests/support/mod.rs"
Cohesion: 0.15
Nodes (23): ac_15_br_14_crm_approved_end_to_end(), ac_46_br_29_public_page_requires_consent_and_never_shows_the_crm(), ac_19_br_15_second_account_gets_conflict_and_the_rejection_reaches_the_user(), ac_43_br_27_revoke_removes_the_badges_and_notifies_the_user(), ac_44_br_28_fraud_suspends_account_and_blocks_login(), approve_crm(), BOUNDARY, bytes_of() (+15 more)

### Community 225 - "badges.rs"
Cohesion: 0.12
Nodes (18): ac_39_br_08_list_active_skips_revoked_and_expired_badges(), ac_41_br_13_expiring_students_query_respects_window_type_and_warning(), ac_41_br_13_revoke_expired_counts_only_past_valid_until(), ac_43_br_27_revoke_for_verification_revokes_derived_badges_only(), ac_44_br_28_revoke_all_revokes_every_badge_of_the_user(), badge(), NOW, store() (+10 more)

### Community 226 - "AccountPorts"
Cohesion: 0.08
Nodes (7): AccountPorts, ac_39_br_08_get_badges_empty(), ac_40_br_10_get_badges_includes_primary_and_every_active_badge(), app(), badge(), br_35_get_badges_for_a_deactivated_account_is_403(), signed_in()

### Community 227 - "AccountStatus"
Cohesion: 0.10
Nodes (18): session_record(), ac_62_br_40_deletion_options_include_export_and_deactivate(), br_40_deletion_options_reject_deactivated_account(), principal(), ac_69_br_42_list_returns_own_notifications_only(), br_35_list_rejects_deactivated_account(), principal(), br_06_removes_own_residency() (+10 more)

### Community 228 - "PgStore"
Cohesion: 0.10
Nodes (9): infra(), infra_or_conflict(), PgStore, select_verifications!, PgStore, stored(), verification_from_row(), PgStore (+1 more)

### Community 229 - "error"
Cohesion: 0.11
Nodes (6): get_public_author(), list_domain_requests(), confirm_fraud(), list_verification_queue(), get_verification_file(), get_verification_review()

### Community 230 - "jobs.test.rs"
Cohesion: 0.11
Nodes (14): ac_66_br_41_purge_deletes_expired_exports_and_their_files(), clock(), NOW, ac_29_br_22_purge_deletes_file_and_keeps_record(), ac_29_br_22_purge_with_nothing_expired_does_nothing(), clock(), NOW, ac_29_br_22_purge_evidence_job_calls_the_use_case() (+6 more)

### Community 231 - "test_db"
Cohesion: 0.19
Nodes (27): ac_01_br_01_schema_profile_defaults_to_hidden_mode_with_a_public_id(), ac_08_br_05_schema_profile_cannot_have_listed_and_foreign_university(), ac_09_br_06_schema_allows_two_crm_registrations_for_one_user_but_not_a_duplicate(), ac_19_br_15_schema_allows_pending_and_other_uf_next_to_a_verified_crm(), ac_19_br_15_schema_rejects_a_second_verified_crm_for_the_same_number_and_uf(), ac_39_br_08_schema_cascades_verifications_and_badges_on_user_delete(), ac_46_br_29_schema_accepts_public_display_document(), ac_46_br_29_schema_rejects_unknown_document() (+19 more)

### Community 232 - "DecisionError"
Cohesion: 0.08
Nodes (18): DecisionError, Access, AlreadyDecided, Badges, Conflict, DeclarationExpired, GraduationYearRequired, Infra (+10 more)

### Community 233 - "VerificationAppError"
Cohesion: 0.09
Nodes (19): VerificationAppError, Access, AlreadyPending, Badges, CodeExpired, CodeLocked, DomainNotListed, GraduationYearRequired (+11 more)

### Community 234 - "VerificationError"
Cohesion: 0.09
Nodes (19): VerificationError, EmptyFile, FileTooLarge, InvalidTransition, MissingReason, UnknownValue, UnsupportedFileType, RejectionReason (+11 more)

### Community 235 - "CrmRegistration"
Cohesion: 0.11
Nodes (7): PgStore, stored(), CrmRegistration, BrazilianUf, .ALL, CrmNumber, MAX_LEN

### Community 236 - "revoke_verification.usecase.test.rs"
Cohesion: 0.19
Nodes (18): StoredVerification, ac_35_br_24_revoke_rejects_non_staff(), ac_43_br_27_revoke_notifies_with_reason(), ac_43_br_27_revoke_without_reason_is_refused(), approved(), br_27_only_an_approved_verification_can_be_revoked(), clock(), finding() (+10 more)

### Community 237 - "verification.controller.test.rs"
Cohesion: 0.24
Nodes (21): ac_14_br_07_upload_returns_201_pending(), ac_24_br_20_residency_upload_needs_the_declaration_date(), ac_28_br_22_upload_far_over_the_limit_is_413_problem_json(), ac_28_br_22_upload_just_over_5mb_is_413(), ac_28_br_22_upload_with_wrong_content_is_415(), ac_28_br_22_upload_without_the_file_or_with_bad_fields_is_422(), ac_31_br_23_list_includes_the_rejection_reason(), ac_32_br_07_list_reports_not_sent() (+13 more)

### Community 238 - "Verification"
Cohesion: 0.15
Nodes (5): business_days_between(), RESIDENCY_DECLARATION_MAX_DAYS, SLA_BUSINESS_DAYS, Verification, ObservedCrmStatus

### Community 239 - "request_institutional_code.usecase.test.rs"
Cohesion: 0.22
Nodes (16): ac_10_br_12_request_stores_the_challenge_and_mails_the_institutional_address(), ac_11_br_12_wrong_university_domain_is_rejected(), ac_13_br_43_unlisted_domain_records_request_and_offers_proof(), br_12_a_profile_without_a_listed_university_cannot_use_the_email_flow(), br_12_invalid_email_is_refused(), br_35_request_rejects_deactivated_account(), clock(), dispatch() (+8 more)

### Community 240 - "DataExportRepository"
Cohesion: 0.17
Nodes (5): BUILD_DOCUMENT, PgStore, DataExportRepository, NewExport, StoredExport

### Community 241 - "account.rs"
Cohesion: 0.23
Nodes (22): ac_46_br_29_consent_records_the_public_display_acceptance(), ac_47_br_30_author_record_has_name_university_situation_and_unrevoked_badges(), ac_49_br_32_set_display_mode_persists_even_without_a_profile_row(), ac_53_br_35_author_record_of_a_deactivated_account_is_inactive_and_unknown_users_are_absent(), ac_53_br_35_set_status_updates_the_user_and_revokes_sessions_only_when_asked(), ac_57_br_37_due_for_deletion_returns_only_overdue_accounts(), ac_57_br_37_set_status_stores_the_deletion_deadline_and_reactivation_clears_it(), ac_59_br_38_erase_removes_user_profile_progress_and_everything_else_personal() (+14 more)

### Community 242 - "LocalFileStorage"
Cohesion: 0.16
Nodes (10): io(), LocalFileStorage, MAX_KEY_LEN, ac_28_br_22_files_and_directory_are_private_to_the_owner(), ac_28_br_22_put_overwrites_the_same_key(), ac_28_br_22_storage_roundtrip_in_a_private_directory(), ac_29_br_22_storage_delete_missing_key_is_ok_and_get_is_none(), ac_30_br_22_storage_rejects_path_traversal_keys() (+2 more)

### Community 243 - "router.rs"
Cohesion: 0.15
Nodes (10): add_residency(), remove_residency(), ApiDoc, account_router(), auth_router(), MAX_UPLOAD_REQUEST_BYTES, public_router(), router() (+2 more)

### Community 244 - "verification_decision.controller.test.rs"
Cohesion: 0.24
Nodes (20): ac_16_br_14_approve_with_non_active_status_is_422(), ac_19_br_15_approve_with_conflict_is_409(), ac_20_br_16_approve_with_name_mismatch_is_422(), ac_34_br_24_approve_returns_204(), ac_34_br_24_approving_twice_is_409(), ac_35_br_24_decisions_are_403_for_regular_users(), ac_36_br_23_reject_returns_204_and_stores_the_reason(), ac_36_br_23_reject_without_a_valid_reason_is_422() (+12 more)

### Community 245 - "VerificationMethod"
Cohesion: 0.11
Nodes (9): detect(), EvidenceFile, MAX_BYTES, normalize(), PersonNameMatch, VerificationMethod, CarteiraCrm, Comprovante (+1 more)

### Community 246 - "request_data_export.usecase.test.rs"
Cohesion: 0.20
Nodes (13): ac_63_br_41_export_stores_json_and_notifies(), ac_65_br_41_an_export_older_than_24h_allows_a_new_one(), ac_65_br_41_second_export_within_24h_is_refused(), br_35_export_rejects_deactivated_account(), clock(), dispatch(), email_only(), ids() (+5 more)

### Community 247 - "uuid"
Cohesion: 0.16
Nodes (14): ac_34_br_24_require_staff_accepts_staff(), ac_35_br_24_require_staff_rejects_regular_principal(), br_35_require_active_accepts_active(), br_35_require_active_rejects_deactivated_and_scheduled_and_suspended(), principal(), ac_09_br_06_adds_second_crm_in_other_uf(), ac_09_br_06_invalid_crm_number_or_uf_is_refused(), br_06_duplicate_crm_is_reported() (+6 more)

### Community 248 - "profile.controller.test.rs"
Cohesion: 0.23
Nodes (16): ac_01_br_01_get_profile_returns_incomplete_flag(), ac_01_br_01_profile_without_a_session_is_401(), ac_02_br_02_get_profile_returns_the_stored_fields(), ac_02_br_02_put_profile_saves_and_returns_the_summary(), ac_04_br_03_put_profile_with_unknown_situation_is_422(), ac_06_br_04_put_profile_oversized_is_422(), ac_09_br_06_get_profile_lists_crm_residency_and_postgraduate_entries(), ac_22_br_17_put_profile_locked_name_is_409() (+8 more)

### Community 249 - "profile.dto.rs"
Cohesion: 0.17
Nodes (10): AddPostgraduateBody, AddPostgraduateInput, PostgraduateDto, ProfileFieldsDto, ProfileResponse, ProfileSummaryResponse, UpdateProfileBody, UpdateProfileInput (+2 more)

### Community 250 - "profiles.rs"
Cohesion: 0.26
Nodes (19): ac_01_br_01_find_without_profile_returns_none(), ac_02_br_02_save_and_find_roundtrip(), ac_02_br_02_save_twice_updates_the_same_row(), ac_08_br_05_foreign_university_roundtrip(), ac_09_br_06_two_crm_registrations_for_one_user(), ac_22_br_17_name_lock_flag_is_returned_and_survives_a_save(), ac_26_br_21_postgraduate_roundtrip_and_delete(), br_05_university_exists() (+11 more)

### Community 251 - "toschema"
Cohesion: 0.21
Nodes (8): AcceptTermsBody, SessionResponse, SignupBody, TermsDto, VerifyResponse, Authenticated, TermsRequired, HealthResponse

### Community 252 - "institutional_email.controller.test.rs"
Cohesion: 0.34
Nodes (15): ac_10_br_12_confirm_returns_200(), ac_10_br_12_request_returns_202_and_mails_the_institutional_address(), ac_11_br_12_wrong_code_is_422_with_the_attempts_left(), ac_11_br_12_wrong_university_is_422(), ac_13_br_43_unlisted_domain_is_409_and_the_request_is_recorded(), app(), br_12_confirm_with_no_open_challenge_is_410_and_a_locked_one_is_429(), br_12_request_with_invalid_email_or_without_a_listed_university_is_422() (+7 more)

### Community 253 - "DisplayMode"
Cohesion: 0.13
Nodes (11): AT_PUBLICATION, AuthorAccountState, Active, Deleted, Inactive, AuthorDisplayInput, COMMUNITY_AUTHOR, VERIFIED_AUTHOR (+3 more)

### Community 254 - "confirm_fraud.usecase.test.rs"
Cohesion: 0.21
Nodes (12): ac_35_br_24_fraud_rejects_non_staff(), ac_44_br_28_fraud_needs_a_note(), ac_44_br_28_fraud_revokes_everything_and_suspends(), clock(), notifier(), NOW, OWNER, principal() (+4 more)

### Community 255 - "database.rs"
Cohesion: 0.16
Nodes (7): ACQUIRE_TIMEOUT, applied_migrations(), connect(), connect_lazy(), MAX_CONNECTIONS, migrate(), POSTGRES_TAG

### Community 256 - "set_display_mode.usecase.test.rs"
Cohesion: 0.23
Nodes (12): ac_45_br_29_hidden_mode_needs_no_acceptance(), ac_46_br_29_public_mode_requires_current_terms_acceptance(), ac_46_br_29_public_mode_with_current_acceptance_is_saved_and_notified(), br_35_set_display_mode_rejects_deactivated_account(), clock(), dispatch(), NOW, principal() (+4 more)

### Community 257 - "BadgeType"
Cohesion: 0.13
Nodes (12): ac_40_br_09_badges_accumulate(), ac_40_br_10_primary_badge_follows_order(), ac_41_br_13_student_badge_expires_after_graduation_year_plus_one(), ac_43_br_27_revoked_badge_is_not_active(), badge(), BadgeType, Doutor, Especialista (+4 more)

### Community 258 - "DomainRequest"
Cohesion: 0.16
Nodes (7): BadgeDto, BadgesResponse, DomainRequestDto, FraudBody, QueueItemDto, BadgesView, DomainRequest

### Community 259 - "schedule_account_deletion.usecase.test.rs"
Cohesion: 0.25
Nodes (11): ac_56_br_37_wrong_confirmation_email_does_not_schedule(), ac_57_br_37_schedule_sets_due_date_and_notifies(), ac_61_br_39_deletion_is_not_blocked_by_open_disputes(), br_37_a_deactivated_account_cannot_schedule_deletion_without_reactivating(), clock(), dispatch(), NOW, principal() (+3 more)

### Community 260 - "health.controller.test.rs"
Cohesion: 0.34
Nodes (10): ac_01_br_01_health_returns_200_with_ok_and_version(), ac_03_br_05_empty_version_is_problem_json(), ac_03_br_05_health_failure_is_problem_json_without_cause(), ac_08_br_05_error_body_has_problem_fields(), app(), content_type(), failing_provider(), json_body() (+2 more)

### Community 261 - "Specialty"
Cohesion: 0.18
Nodes (5): SpecialtyDto, UniversityDto, UniversityQuery, Specialty, University

### Community 262 - "AuthApi"
Cohesion: 0.24
Nodes (11): AuthApi, AcceptTerms, CompleteSignup, code_hash_input(), RequestAccess, RequestAccessError, Infra, InvalidEmail (+3 more)

### Community 263 - "deactivate_account.usecase.test.rs"
Cohesion: 0.24
Nodes (10): ac_53_br_35_deactivate_sets_status_revokes_sessions_and_notifies(), br_35_an_account_that_is_not_active_cannot_be_deactivated(), clock(), dispatch(), email_only(), NOW, principal(), service() (+2 more)

### Community 264 - "preview_display.usecase.test.rs"
Cohesion: 0.29
Nodes (13): ac_50_br_33_preview_exposes_the_public_id_so_the_owner_can_share_the_page(), ac_50_br_33_preview_has_no_public_id_before_the_profile_exists(), ac_50_br_33_preview_of_a_hidden_profile_still_previews_the_public_mode(), ac_50_br_33_preview_shows_both_modes(), ac_50_br_33_preview_without_a_record_is_not_found(), authors_with(), badge(), br_35_preview_rejects_deactivated_account() (+5 more)

### Community 265 - "update_profile.usecase.test.rs"
Cohesion: 0.38
Nodes (14): ac_02_br_02_update_saves_and_reports_complete(), ac_04_br_03_update_rejects_unknown_situation(), ac_06_br_04_update_rejects_oversized_fields(), ac_08_br_05_foreign_university_saves_free_text(), ac_22_br_17_locked_name_cannot_change(), ac_22_br_17_locked_name_may_be_resent_unchanged(), br_05_listed_and_foreign_university_together_are_refused(), br_05_unknown_listed_university_is_refused() (+6 more)

### Community 266 - "StoredNotification"
Cohesion: 0.20
Nodes (3): PgStore, NewNotification, StoredNotification

### Community 267 - "reference.controller.rs"
Cohesion: 0.26
Nodes (5): get_profile(), update_profile(), DEFAULT_LIMIT, list_specialties(), list_universities()

### Community 268 - "data_export.controller.test.rs"
Cohesion: 0.32
Nodes (11): ac_63_br_41_export_returns_202_with_the_id(), ac_64_br_41_download_of_another_account_is_404(), ac_64_br_41_download_returns_the_json_file_to_its_owner(), ac_64_br_41_download_without_session_is_401(), ac_65_br_41_second_export_is_429(), ac_66_br_41_expired_download_is_404(), app(), DOWNLOAD (+3 more)

### Community 269 - "FlowProbe"
Cohesion: 0.22
Nodes (3): AcceptanceTrace, FlowProbe, RemainingRows

### Community 270 - "mark_notification_read.usecase.test.rs"
Cohesion: 0.20
Nodes (5): NOW, ac_69_br_42_mark_read_records_the_time_for_the_owner(), ac_69_br_42_marking_someone_elses_notification_is_not_found(), principal(), service()

### Community 271 - "AuthorRecord"
Cohesion: 0.18
Nodes (6): AuthorRecord, Situation, Especialista, Estudante, Medico, Residente

### Community 272 - "get_public_author.usecase.test.rs"
Cohesion: 0.31
Nodes (10): ac_47_br_30_public_page_has_profile_data_and_question_count(), ac_49_br_30_public_page_is_not_found_when_hidden_or_deactivated(), ac_49_br_30_unknown_public_id_is_not_found(), ac_51_br_31_public_page_never_has_crm(), authors_with(), badge(), clock(), NOW (+2 more)

### Community 273 - "resolve_author_display.usecase.test.rs"
Cohesion: 0.31
Nodes (10): ac_48_br_30_resolve_hidden_without_badge(), ac_49_br_32_resolve_reflects_the_stored_mode(), ac_52_br_34_resolve_deleted_author_with_stored_badge(), author(), authors_with(), badge(), clock(), NOW (+2 more)

### Community 274 - "verification.entity.test.rs"
Cohesion: 0.25
Nodes (11): ac_10_br_12_automatic_approval_has_no_decider(), ac_14_br_07_submitted_is_pending(), ac_23_br_18_crm_check_keeps_only_status_and_specialties(), ac_34_br_24_decision_records_who_and_when(), ac_36_br_23_reject_requires_reason(), ac_38_br_26_decided_verification_is_never_overdue(), ac_38_br_26_pending_over_seven_business_days_is_overdue(), ac_38_br_26_weekends_do_not_count_toward_the_deadline() (+3 more)

### Community 275 - "versions"
Cohesion: 0.32
Nodes (9): ac_27_br_13_accept_terms_with_old_version_is_422(), ac_27_br_14_accept_terms_returns_204_even_when_terms_are_pending(), ac_27_br_14_accept_terms_without_session_is_401(), app(), ac_21_br_11_session_response_has_no_user_id(), ac_26_br_14_session_reports_terms_pending(), ac_48_br_30_session_returns_account_status_and_staff_flag(), app() (+1 more)

### Community 276 - "AuthorDisplay"
Cohesion: 0.31
Nodes (6): AuthorDisplayDto, DisplayPreviewResponse, PublicAuthorDto, DisplayPreview, AuthorDisplay, PublicAuthor

### Community 277 - "verification_review.dto.rs"
Cohesion: 0.24
Nodes (5): AddCrmRegistrationBody, CrmRegistrationDto, ReviewResponse, ReviewVerificationDto, ReviewView

### Community 278 - "json.test.rs"
Cohesion: 0.23
Nodes (7): ac_01_br_03_valid_body_passes_through(), ac_04_br_24_malformed_body_is_problem_json(), ac_04_br_24_missing_field_is_422_problem_json(), ac_04_br_24_wrong_content_type_is_problem_json(), Body1, call(), echo()

### Community 279 - "Attempt"
Cohesion: 0.23
Nodes (3): Attempt, ac_33_br_19_attempt_accepts_any_question_id(), AttemptId

### Community 280 - "progress.rs"
Cohesion: 0.36
Nodes (11): ac_28_br_16_insert_many_skips_existing_attempt_ids(), ac_28_br_16_insert_many_with_empty_slice_inserts_nothing(), ac_29_br_16_repeating_the_batch_inserts_zero(), ac_30_br_17_list_returns_all_attempts_of_user_only_in_answer_order(), ac_30_br_17_list_round_trips_every_field(), ac_32_br_18_insert_one_reports_duplicate(), ac_33_br_19_attempt_with_unknown_question_is_stored(), attempt() (+3 more)

### Community 281 - "download_data_export.usecase.test.rs"
Cohesion: 0.36
Nodes (9): ac_64_br_41_download_refuses_other_account(), ac_64_br_41_download_returns_the_file_to_its_owner(), ac_66_br_41_download_of_unknown_export_is_not_found(), ac_66_br_41_download_refuses_expired_link(), clock(), NOW, principal(), service() (+1 more)

### Community 282 - "VerificationItemType"
Cohesion: 0.19
Nodes (8): ItemStatus, status_of(), VerificationItemType, Crm, Especialista, Matricula, Pos, Residencia

### Community 283 - "get_verification_for_review.usecase.test.rs"
Cohesion: 0.29
Nodes (11): ac_29_br_22_a_purged_file_is_not_found(), ac_30_br_22_staff_reads_the_file_with_its_content_type(), ac_30_br_22_the_file_is_read_only_by_staff(), ac_33_br_24_review_shows_profile_and_crm_next_to_the_request(), OWNER, PDF, pending(), principal() (+3 more)

### Community 284 - "list_verification_queue.usecase.test.rs"
Cohesion: 0.31
Nodes (10): ac_33_br_24_queue_is_ordered_by_arrival(), ac_35_br_24_queue_rejects_non_staff(), ac_38_br_26_queue_flags_overdue(), at(), clock(), NOW, OWNER, principal() (+2 more)

### Community 285 - "account.controller.test.rs"
Cohesion: 0.38
Nodes (10): ac_53_br_35_deactivate_returns_204(), ac_55_br_36_reactivate_is_allowed_for_a_deactivated_principal(), ac_56_br_37_wrong_email_is_422(), ac_57_br_37_account_routes_without_a_session_are_401(), ac_57_br_37_deletion_returns_202_with_the_due_date(), ac_62_br_40_deletion_options_lists_three_destinations(), app(), br_35_deactivating_an_already_deactivated_account_is_403() (+2 more)

### Community 286 - "privacy.controller.test.rs"
Cohesion: 0.39
Nodes (10): ac_45_br_29_hidden_mode_needs_no_acceptance(), ac_45_br_29_unknown_mode_is_422(), ac_46_br_29_public_mode_with_the_current_acceptance_returns_204(), ac_46_br_29_public_mode_without_acceptance_is_422(), ac_50_br_33_preview_returns_both_modes(), app(), badge(), br_35_privacy_routes_are_403_for_a_deactivated_account() (+2 more)

### Community 287 - "verification.controller.rs"
Cohesion: 0.32
Nodes (4): list_verifications(), missing(), multipart_error(), submit_verification()

### Community 288 - "router.test.rs"
Cohesion: 0.36
Nodes (5): ac_01_br_01_post_health_keeps_405(), ac_01_br_01_unknown_route_keeps_404(), app(), provider_returning(), send()

### Community 289 - "dispatch_notification.usecase.test.rs"
Cohesion: 0.35
Nodes (8): ac_54_br_35_deactivated_account_gets_only_account_related_email(), ac_57_br_37_scheduled_deletion_account_still_gets_deletion_emails(), ac_67_br_42_dispatches_email_and_site(), ac_68_br_42_site_only_sends_no_email(), br_42_payload_travels_with_the_email_and_the_site_notice(), NOW, service(), target()

### Community 290 - "notification.controller.rs"
Cohesion: 0.33
Nodes (3): DEFAULT_LIMIT, list_notifications(), mark_notification_read()

### Community 291 - "crm_registration.controller.test.rs"
Cohesion: 0.36
Nodes (7): ac_09_br_06_post_crm_returns_201_with_the_normalized_entry(), ac_09_br_06_post_crm_with_invalid_number_or_uf_is_422(), app(), br_06_delete_crm_returns_204_and_404_for_unknown(), br_06_post_duplicate_crm_is_409(), problem_json(), signed_in()

### Community 292 - "verification.dto.rs"
Cohesion: 0.24
Nodes (6): ConfirmInstitutionalCodeBody, InstitutionalConfirmedResponse, RequestInstitutionalCodeBody, SubmittedVerificationResponse, SubmitVerificationForm, VerificationItemDto

### Community 293 - "adapters-postgres/src/modules/privacy/repositories/public_author.repository.rs"
Cohesion: 0.35
Nodes (3): select_author!, PgStore, stored()

### Community 296 - "account.dto.rs"
Cohesion: 0.24
Nodes (4): DeletionOptionsResponse, DeletionScheduledResponse, ExportRequestedResponse, ScheduleDeletionBody

### Community 297 - "verification_review.controller.test.rs"
Cohesion: 0.53
Nodes (8): ac_30_br_22_staff_downloads_the_file_with_safe_headers(), ac_30_br_22_the_file_is_403_for_regular_users_and_404_once_purged(), ac_33_br_24_review_of_an_unknown_request_is_404(), ac_33_br_24_review_shows_the_request_profile_and_crm(), app(), pending(), staff(), stored()

### Community 298 - "list_badges.usecase.test.rs"
Cohesion: 0.38
Nodes (7): ac_39_br_08_list_without_verified_items_is_empty(), ac_40_br_10_list_reports_primary_badge(), badge(), br_35_list_rejects_deactivated_account(), NOW, principal(), service()

### Community 299 - "list_my_verifications.usecase.test.rs"
Cohesion: 0.47
Nodes (8): ac_31_br_23_list_shows_rejection_reason_and_allows_resubmission(), ac_31_br_23_the_latest_submission_wins(), ac_32_br_07_list_reports_not_sent(), br_35_list_rejects_deactivated_account(), crm(), crm_verification(), principal(), service()

### Community 300 - "wiring.test.rs"
Cohesion: 0.36
Nodes (8): ac_01_br_01_router_serves_health_with_package_version(), ac_01_br_01_router_serves_the_openapi_document_with_auth_routes(), ac_04_br_24_router_serves_public_access_route_and_validates_email(), ac_20_br_10_router_requires_session_on_protected_routes(), ac_47_br_30_the_public_author_route_exists_and_needs_no_session(), br_35_router_requires_session_on_the_account_and_staff_routes(), br_35_the_openapi_document_lists_the_account_staff_and_public_routes(), test_router()

### Community 301 - "author_display.entity.test.rs"
Cohesion: 0.40
Nodes (9): ac_47_br_30_br_31_public_display_never_has_crm(), ac_47_br_30_public_page_lists_all_active_badges_and_ignores_revoked(), ac_48_br_30_hidden_without_badge_is_community_author(), ac_49_br_32_hidden_with_badge_is_verified_author(), ac_49_br_32_inactive_account_is_shown_as_hidden(), ac_51_br_31_public_author_has_no_crm_field(), ac_52_br_34_deleted_author_uses_stored_badge_with_note(), badge() (+1 more)

### Community 302 - "account.controller.rs"
Cohesion: 0.58
Nodes (4): deactivate_account(), get_deletion_options(), reactivate_account(), schedule_account_deletion()

### Community 303 - "add_residency.usecase.test.rs"
Cohesion: 0.53
Nodes (6): br_06_adds_residency_with_a_known_specialty(), br_06_end_year_before_start_year_is_refused(), br_06_unknown_specialty_is_refused(), input(), principal(), service()

### Community 304 - "get_profile.usecase.test.rs"
Cohesion: 0.44
Nodes (6): ac_01_br_01_profile_is_optional_for_empty_profile(), ac_02_br_02_get_profile_reports_complete(), ac_09_br_06_get_profile_lists_every_crm_registration(), br_35_get_profile_rejects_deactivated_account(), principal(), service()

### Community 305 - "evidence_file.value_object.test.rs"
Cohesion: 0.22
Nodes (3): JPG, PDF, PNG

### Community 307 - "public_author.controller.test.rs"
Cohesion: 0.54
Nodes (6): ac_47_br_30_public_page_has_no_crm_and_needs_no_session(), ac_49_br_30_public_page_hidden_is_404(), ac_49_br_30_public_page_of_an_unknown_author_is_404(), badge(), public_app(), record()

### Community 310 - "fraud.controller.test.rs"
Cohesion: 0.46
Nodes (6): ac_35_br_24_fraud_is_403_for_regular_users(), ac_44_br_28_fraud_returns_204(), ac_44_br_28_fraud_without_a_note_is_422(), app(), FRAUD, staff()

### Community 312 - "notifications.rs"
Cohesion: 0.54
Nodes (6): ac_67_br_42_notifications_list_newest_first_and_only_the_owners(), ac_67_br_42_payload_round_trips(), ac_69_br_42_mark_read_only_for_the_owner_and_keeps_the_first_time(), notice(), NOW, user()

### Community 313 - "grant_badges_for_verification.usecase.test.rs"
Cohesion: 0.50
Nodes (5): ac_17_br_19_grant_stores_every_requested_badge_with_detail(), ac_39_br_08_grant_with_no_badges_stores_nothing(), ac_41_br_13_grant_keeps_valid_until(), grant(), service()

### Community 314 - "postgraduate.controller.test.rs"
Cohesion: 0.62
Nodes (5): ac_26_br_21_post_postgraduate_returns_201(), ac_27_br_21_post_postgraduate_with_unknown_kind_is_422(), app(), br_06_delete_postgraduate_returns_204(), signed_in()

### Community 315 - "reference.controller.test.rs"
Cohesion: 0.62
Nodes (5): app(), br_05_universities_are_listed_with_the_query_and_a_clamped_limit(), br_05_universities_default_to_ten_results_without_a_query(), br_06_specialties_are_listed(), signed_in()

### Community 316 - "residency.controller.test.rs"
Cohesion: 0.62
Nodes (5): app(), br_06_delete_unknown_residency_is_404(), br_06_post_residency_returns_201(), br_06_post_residency_with_unknown_specialty_is_422(), signed_in()

### Community 317 - "residency.dto.rs"
Cohesion: 0.43
Nodes (3): AddResidencyBody, AddResidencyInput, ResidencyDto

### Community 319 - "add_postgraduate.usecase.test.rs"
Cohesion: 0.62
Nodes (5): ac_26_br_21_adds_completed_master(), ac_27_br_21_unknown_kind_or_status_is_refused(), input(), principal(), service()

### Community 320 - ".check"
Cohesion: 0.48
Nodes (4): ApproveInput, Checked, plain(), spec()

### Community 323 - "profile.entity.test.rs"
Cohesion: 0.48
Nodes (5): ac_02_br_02_student_with_name_situation_university_is_complete(), ac_03_br_02_doctor_without_graduation_year_is_incomplete(), ac_05_br_03_preparing_residency_does_not_change_completeness(), ac_08_br_05_foreign_university_is_accepted(), student()

### Community 324 - "verification_decision.dto.rs"
Cohesion: 0.40
Nodes (4): ApproveBody, ApproveInput, RejectBody, RevokeBody

### Community 325 - "reactivate_account.usecase.test.rs"
Cohesion: 0.53
Nodes (4): ac_55_br_36_reactivate_restores_active(), br_36_a_suspended_account_cannot_reactivate_itself(), br_36_reactivating_an_active_account_is_refused(), principal()

### Community 326 - "get_health.usecase.test.rs"
Cohesion: 0.60
Nodes (4): ac_01_br_01_reports_status_ok(), ac_03_br_05_propagates_version_failure(), ac_05_br_04_returns_version_from_replaced_port(), use_case_with()

## Knowledge Gaps
- **188 isolated node(s):** `Internal`, `Access`, `Invalid`, `EmailMismatch`, `TooSoon` (+183 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 833 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **190 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `UserId` connect `PortError` to `set_display_mode.usecase.test.rs`, `schedule_account_deletion.usecase.test.rs`, `deactivate_account.usecase.test.rs`, `preview_display.usecase.test.rs`, `update_profile.usecase.test.rs`, `StoredNotification`, `data_export.controller.test.rs`, `mark_notification_read.usecase.test.rs`, `accounts.rs`, `test_support.rs`, `AuthorRecord`, `DocumentVersion`, `versions`, `get_public_author.usecase.test.rs`, `.pool`, `User`, `Attempt`, `progress.rs`, `download_data_export.usecase.test.rs`, `request_access.usecase.test.rs`, `get_verification_for_review.usecase.test.rs`, `list_verification_queue.usecase.test.rs`, `DispatchNotification`, `dispatch_notification.usecase.test.rs`, `adapters-postgres/src/modules/privacy/repositories/public_author.repository.rs`, `list_badges.usecase.test.rs`, `list_my_verifications.usecase.test.rs`, `Clock`, `add_residency.usecase.test.rs`, `get_profile.usecase.test.rs`, `notifications.rs`, `grant_badges_for_verification.usecase.test.rs`, `Principal`, `adapters-postgres/src/modules/verification/repositories/email_domain.repository.rs`, `add_postgraduate.usecase.test.rs`, `verify_access.usecase.test.rs`, `complete_signup.usecase.test.rs`, `.check`, `reactivate_account.usecase.test.rs`, `verify_access.controller.test.rs`, `SessionId`, `datetime`, `TermsVersions`, `sync_progress.usecase.test.rs`, `accept_terms.usecase.test.rs`, `ProfileError`, `confirm_institutional_code.usecase.test.rs`, `PrivacyAppError`, `AccessError`, `resolve_author_display.usecase.test.rs`, `AccountApi`, `account_test_support.rs`, `badges.rs`, `AccountStatus`, `PgStore`, `error`, `decide_verification.usecase.test.rs`, `submit_verification.usecase.test.rs`, `DecisionError`, `CrmRegistration`, `revoke_verification.usecase.test.rs`, `Verification`, `request_institutional_code.usecase.test.rs`, `DataExportRepository`, `account.rs`, `request_data_export.usecase.test.rs`, `uuid`, `profiles.rs`, `DisplayMode`, `confirm_fraud.usecase.test.rs`?**
  _High betweenness centrality (0.109) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `UserId` (e.g. with `ac_27_br_14_accept_terms_returns_204_even_when_terms_are_pending()` and `ac_25_br_12_logout_all_returns_204()`) actually correct?**
  _`UserId` has 5 INFERRED edges - model-reasoned connections that need verification._
- **What connects `Internal`, `Access`, `Invalid` to the rest of the system?**
  _188 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `package.json` be split into smaller, more focused modules?**
  _Cohesion score 0.12554112554112554 - nodes in this community are weakly interconnected._
- **Why does `Principal` connect `Principal` to `set_display_mode.usecase.test.rs`, `schedule_account_deletion.usecase.test.rs`, `AuthApi`, `deactivate_account.usecase.test.rs`, `preview_display.usecase.test.rs`, `update_profile.usecase.test.rs`, `reference.controller.rs`, `mark_notification_read.usecase.test.rs`, `download_data_export.usecase.test.rs`, `VerificationItemType`, `get_verification_for_review.usecase.test.rs`, `list_verification_queue.usecase.test.rs`, `Problem`, `verification.controller.rs`, `DispatchNotification`, `notification.controller.rs`, `data_export.controller.rs`, `list_badges.usecase.test.rs`, `privacy.controller.rs`, `ApiJson`, `list_my_verifications.usecase.test.rs`, `account.controller.rs`, `Clock`, `add_residency.usecase.test.rs`, `get_profile.usecase.test.rs`, `crm_registration.controller.rs`, `postgraduate.controller.rs`, `institutional_email.controller.rs`, `add_postgraduate.usecase.test.rs`, `reactivate_account.usecase.test.rs`, `SessionId`, `PortError`, `TermsVersions`, `ProfileError`, `dtos`, `confirm_institutional_code.usecase.test.rs`, `PrivacyAppError`, `AccessError`, `AccountApi`, `decide_verification.usecase.test.rs`, `account_test_support.rs`, `submit_verification.usecase.test.rs`, `AccountStatus`, `error`, `DecisionError`, `VerificationAppError`, `revoke_verification.usecase.test.rs`, `request_institutional_code.usecase.test.rs`, `router.rs`, `request_data_export.usecase.test.rs`, `uuid`, `confirm_fraud.usecase.test.rs`?**
  _High betweenness centrality (0.101) - this node is a cross-community bridge._
- **Should `frontend` be split into smaller, more focused modules?**
  _Cohesion score 0.05398110661268556 - nodes in this community are weakly interconnected._
- **Why does `PortError` connect `PortError` to `Specialty`, `AuthApi`, `StoredNotification`, `mark_notification_read.usecase.test.rs`, `accounts.rs`, `AuthorRecord`, `test_support.rs`, `DocumentVersion`, `Email`, `.pool`, `User`, `Attempt`, `PortError`, `DispatchNotification`, `adapters-postgres/src/modules/privacy/repositories/public_author.repository.rs`, `Clock`, `Principal`, `adapters-postgres/src/modules/verification/repositories/email_domain.repository.rs`, `SessionId`, `SignupError`, `AttemptRepository`, `TermsVersions`, `auth_flow.rs`, `VerifyError`, `ProfileError`, `confirm_institutional_code.usecase.test.rs`, `PrivacyAppError`, `AccessError`, `AccountApi`, `bootstrap/tests/support/mod.rs`, `badges.rs`, `AccountStatus`, `PgStore`, `DecisionError`, `VerificationAppError`, `CrmRegistration`, `Verification`, `DataExportRepository`, `LocalFileStorage`, `uuid`, `profiles.rs`, `DisplayMode`?**
  _High betweenness centrality (0.066) - this node is a cross-community bridge._