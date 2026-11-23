# Cadastro, login e sessão - backend - Verification report

## Summary

**PASS** · tentativa 3 de 3 (`verifyRetries` = 2, o máximo permitido; uma nova mudança de código depois desta aprovação exigiria decisão do humano). Demanda DEM-20261118-login-register-backend, verificação rodada em 2026-11-19.

- A tentativa 1 passou, mas o humano pediu duas mudanças depois dela, ambas com código: (1) reestruturar o backend conforme a premissa de estrutura (`commons/project-structure-general.md`), retry 1; (2) tirar valores fixos do código e guardar configuração e segredos num `.env`, com `LISTEN_ADDR` configurável, retry 2.
- 175 testes unitários e 44 de integração (Postgres 17 via Podman) passaram, 0 falhas, 0 ignorados: 219 testes. Em relação ao conjunto anterior à refatoração (210), nenhum foi removido ou renomeado e 9 foram acrescentados (configuração, `LISTEN_ADDR` e `.env`).
- Dos 219 testes, 18 são herdados da demanda anterior (`refatorar-backend-hexagonal`) e 201 são desta; a rastreabilidade conta só os 201.
- Todos os 33 AC e os 24 BR têm pelo menos um teste desta demanda, e todos passaram.
- Checks de estrutura (novos no VERIFY): saída vazia nos três; nenhum `ports.rs`, nenhum `mod tests { ... }` com corpo e nenhum `*.test.rs` órfão (44 arquivos de teste).
- Nenhum segredo no git: o `.env` está ignorado e fora do índice; o `.env.example` só traz o modelo (`AUTH_SECRET=change-me`, recusado pela API por ter menos de 32 caracteres).
- Frontend: não se aplica (demanda só de backend).

## Commands

Rodados em `repos/medsafari/backend` (e `repos/medsafari` para o lefthook), com `DOCKER_HOST=unix:///run/user/1000/podman/podman.sock` nos de integração.

| command | repo | exit code | result |
|---|---|---|---|
| `cargo fmt --check` | medsafari | 0 | sem diferenças |
| `cargo clippy --workspace -- -D warnings` | medsafari | 0 | sem erros |
| `cargo clippy --workspace --all-targets -- -D warnings` | medsafari | 0 | sem erros (inclui os arquivos de teste) |
| `cargo nextest run --workspace --profile unit --no-fail-fast` | medsafari | 0 | 175 passaram |
| `cargo nextest run --workspace --profile integration --no-fail-fast` | medsafari | 0 | 44 passaram |
| `lefthook run pre-commit --all-files` | medsafari | 0 | fmt, clippy e unit executados e verdes (sem `--all-files` os comandos são pulados por falta de arquivos em stage) |
| loop de órfãos do guia (`find crates -path '*/src/*/__tests__/*.test.rs'` + `grep` no arquivo de código) | medsafari | 0 | saída vazia; 44 arquivos de teste, todos declarados |
| mesmo loop estendido a `src/__tests__/` (arquivos na raiz do crate) | medsafari | 0 | saída vazia |
| `ports.rs` ou `mod tests {` com corpo em arquivos criados ou alterados (`git diff --name-only origin/main..HEAD`) | medsafari | 0 | saída vazia |
| `git ls-files` (arquivo `.env`) e `git diff origin/main..HEAD` buscando `AUTH_SECRET=`/`DATABASE_URL=` | medsafari | 0 | `.env` não versionado e ignorado (`.gitignore:11`); só aparecem o modelo `.env.example`, valores falsos de teste e a URL local de desenvolvimento |
| `find src -name '*.spec.ts' -not -path '*/__tests__/*'` | medsafari | n/a | não aplicável (sem frontend nesta demanda) |
| `npx ajv validate ... demand-context.json` | workspace | 0 | `valid` |

Sanidade do check de órfãos: com um `zzz.value_object.test.rs` solto o loop imprimiu `ORPHAN: ...`; o arquivo foi removido em seguida.

O loop de órfãos do guia usa `*/src/*/__tests__/*.test.rs`, que não enxerga `src/__tests__/` (arquivos na raiz do crate, como `router.rs` e `config.rs`). Por isso rodei também a versão estendida; o guia precisa dessa correção.

Verificações manuais (banco local com Podman, porta 55432, removido no fim com `dev/db.sh purge`):

- Task 16 (tentativa 1): `dev/db.sh up`, `migrate` duas vezes sem erro e as 7 tabelas mais `_sqlx_migrations`.
- Task 18: `dev/init-env.sh` criou o `.env` (permissão 600, `AUTH_SECRET` de 64 caracteres hexadecimais). Só com o arquivo, o `migrate` listou `0001 auth` e `0002 attempts` e a API respondeu em `127.0.0.1:3199` (`/api/health` 200, `POST /api/auth/access-requests` 202, link e código no log em `APP_ENV=dev`). Com `LISTEN_ADDR=127.0.0.1:3198` no ambiente, a API passou a escutar em 3198, ou seja, o ambiente vence o arquivo.
- Task 18, erros: `LISTEN_ADDR=nao-e-endereco` -> `InvalidListenAddr`; `AUTH_SECRET=change-me` -> `SecretTooShort`; linha inválida no `.env` -> `DotEnv(...)`. Todos encerram a API com mensagem clara.

## Traceability

A ligação entre critério e teste segue a convenção de nome `ac_<nn>_br_<nn>_<comportamento>` (testes de esquema usam só `br_<nn>_`); o relatório confirma que existe um teste passando por AC e por BR, mas não prova por si só que cada teste cobre todo o critério.

Os testes unitários agora ficam em `crates/<crate>/src/<pasta-do-tipo>/__tests__/<nome>.<tipo>.test.rs` (ou `src/__tests__/<nome>.test.rs` para arquivos da raiz); os de integração continuam em `crates/adapters-postgres/tests` e `crates/bootstrap/tests/auth_flow.rs`. Até 3 testes por linha; `(+n)` indica mais testes.

### Acceptance criteria

| AC | testes | tipo | resultado |
|---|---|---|---|
| AC-01 | `ac_01_br_03_valid_body_passes_through`, `ac_01_br_01_openapi_describes_every_auth_and_progress_route`, `ac_01_br_04_openapi_lists_auth_access_routes` (+20) | unit | PASS |
| AC-02 | `ac_02_br_04_access_response_is_identical_for_sent_and_rate_limited`, `ac_02_br_04_internal_error_does_not_leak_cause`, `ac_02_br_04_result_is_ok_for_sent_and_for_rate_limited` (+4) | unit | PASS |
| AC-03 | `ac_03_br_05_normalizes_email_before_counting_and_storing`, `ac_03_br_05_email_is_trimmed_and_lowercased`, `ac_03_br_05_email_keeps_dots_and_plus` | unit | PASS |
| AC-04 | `ac_04_br_24_invalid_email_is_422_invalid_email_format`, `ac_04_br_24_problem_json_has_type_title_status_detail`, `ac_04_br_24_malformed_body_is_problem_json` (+6) | unit | PASS |
| AC-05 | `ac_05_br_08_invalidates_open_requests_before_inserting`, `ac_05_br_08_new_request_invalidates_open_ones_of_same_email` | integration+unit | PASS |
| AC-06 | `ac_06_br_09_settings_limits_match_the_spec`, `ac_06_br_09_eleventh_request_in_a_day_is_silent_ok`, `ac_06_br_09_fourth_request_in_15_minutes_is_silent_ok` (+2) | integration+unit | PASS |
| AC-07 | `ac_07_br_09_falls_back_to_socket_when_header_is_missing_or_blank`, `ac_07_br_09_header_is_ignored_when_not_configured`, `ac_07_br_09_trusted_header_is_used_when_configured` (+3) | integration+unit | PASS |
| AC-08 | `ac_08_br_06_verify_token_sets_session_cookie_without_token_in_body`, `ac_08_br_06_verify_without_credential_is_422`, `ac_08_br_03_token_for_existing_user_issues_session` (+1) | integration+unit | PASS |
| AC-09 | `ac_09_br_06_verify_code_returns_authenticated`, `ac_09_br_03_code_for_existing_user_issues_session` | unit | PASS |
| AC-10 | `ac_10_br_06_used_token_is_410`, `ac_10_br_06_gone_when_token_already_consumed`, `ac_10_br_06_consume_returns_the_requested_email` (+4) | integration+unit | PASS |
| AC-11 | `ac_11_br_06_expired_code_is_410`, `ac_11_br_06_gone_when_request_expired`, `ac_11_br_06_request_expires_at_the_boundary` | integration+unit | PASS |
| AC-12 | `ac_12_br_07_malformed_code_is_422_without_attempts_remaining`, `ac_12_br_07_wrong_code_is_422_with_attempts_remaining`, `ac_12_br_07_problem_can_carry_attempts_remaining` (+9) | integration+unit | PASS |
| AC-13 | `ac_13_br_20_get_on_verify_route_is_405`, `ac_13_br_20_token_is_consumed_once_per_execute`, `ac_13_br_11_postgres_adapter_depends_only_inward` | unit | PASS |
| AC-14 | `ac_14_br_09_ip_limit_is_429`, `ac_14_br_09_code_attempt_above_ip_limit_is_rejected_before_checking`, `ac_14_br_09_code_attempts_by_ip_are_counted` | integration+unit | PASS |
| AC-15 | `ac_15_br_13_signup_returns_201_and_cookie`, `ac_15_br_21_verify_for_unknown_email_returns_terms_required`, `ac_15_br_01_second_use_of_signup_token_is_gone` (+10) | integration+unit | PASS |
| AC-16 | `ac_16_br_22_signup_with_expired_token_is_410`, `ac_16_br_21_no_signup_token_means_no_user` | unit | PASS |
| AC-17 | `ac_17_br_13_signup_with_old_version_is_422`, `ac_17_br_13_mismatched_version_creates_nothing_and_keeps_token`, `ac_17_br_13_document_version_rejects_blank` | unit | PASS |
| AC-18 | `ac_18_br_22_settings_signup_window_is_15_minutes`, `ac_18_br_22_expired_signup_token_is_gone`, `ac_18_br_22_pending_signup_is_single_use_and_expires` | integration+unit | PASS |
| AC-19 | `ac_19_br_13_signup_without_display_name_is_201`, `ac_19_br_15_signup_with_81_char_display_name_is_422`, `ac_19_br_15_display_name_over_80_chars_is_rejected_before_consuming` (+3) | unit | PASS |
| AC-20 | `ac_20_br_10_clear_cookie_expires_in_the_past`, `ac_20_br_10_read_cookie_ignores_empty_and_garbage`, `ac_20_br_10_read_cookie_returns_the_session_value` (+6) | unit | PASS |
| AC-21 | `ac_21_br_11_session_response_has_no_user_id`, `ac_21_br_11_authenticated_request_renews_the_session`, `ac_21_br_11_authenticate_extends_expiry_to_30_days` (+4) | integration+unit | PASS |
| AC-22 | `ac_22_br_11_expired_session_is_401`, `ac_22_br_11_authenticate_rejects_session_past_90_days`, `ac_22_br_11_authenticate_rejects_unknown_token` (+4) | integration+unit | PASS |
| AC-23 | `ac_23_br_23_label_falls_back_when_unknown`, `ac_23_br_23_label_names_browser_and_system`, `ac_23_br_23_issue_stores_hash_and_label_not_the_token` (+1) | integration+unit | PASS |
| AC-24 | `ac_24_br_12_logout_clears_cookie_and_returns_204`, `ac_24_br_12_second_logout_with_same_cookie_is_401`, `ac_24_br_12_logout_revokes_only_current_session` (+1) | integration+unit | PASS |
| AC-25 | `ac_25_br_12_logout_all_returns_204`, `ac_25_br_12_logout_all_revokes_every_session_of_user`, `ac_25_br_12_revoke_all_covers_every_session_of_user` (+1) | integration+unit | PASS |
| AC-26 | `ac_26_br_14_record_with_terms_pending_is_403`, `ac_26_br_14_session_reports_terms_pending`, `ac_26_br_14_sync_with_terms_pending_is_403` (+6) | integration+unit | PASS |
| AC-27 | `ac_27_br_13_accept_terms_with_old_version_is_422`, `ac_27_br_14_accept_terms_returns_204_even_when_terms_are_pending`, `ac_27_br_14_accept_terms_without_session_is_401` (+3) | integration+unit | PASS |
| AC-28 | `ac_28_br_16_attempt_with_bad_timestamp_or_blank_fields_is_422`, `ac_28_br_16_sync_over_1000_attempts_is_422`, `ac_28_br_16_sync_returns_full_progress` (+9) | integration+unit | PASS |
| AC-29 | `ac_29_br_16_sync_repeated_returns_same_total`, `ac_29_br_16_sync_with_same_attempts_adds_nothing`, `ac_29_br_16_repeating_the_batch_inserts_zero` | integration+unit | PASS |
| AC-30 | `ac_30_br_17_sync_with_empty_list_returns_account_attempts`, `ac_30_br_17_sync_returns_attempts_of_account_not_only_sent`, `ac_30_br_17_list_returns_all_attempts_of_user_only_in_answer_order` (+1) | integration+unit | PASS |
| AC-31 | `ac_31_br_18_record_new_attempt_is_201`, `ac_31_br_18_record_creates_attempt` | unit | PASS |
| AC-32 | `ac_32_br_18_record_existing_attempt_is_200`, `ac_32_br_18_record_twice_reports_already_existed`, `ac_32_br_18_insert_one_reports_duplicate` | integration+unit | PASS |
| AC-33 | `ac_33_br_19_record_accepts_unknown_question_id`, `ac_33_br_19_record_does_not_check_question_existence`, `ac_33_br_19_attempt_accepts_any_question_id` (+1) | integration+unit | PASS |

### Business rules

| BR | testes | tipo | resultado |
|---|---|---|---|
| BR-01 | `ac_01_br_01_openapi_describes_every_auth_and_progress_route`, `ac_15_br_01_second_use_of_signup_token_is_gone`, `ac_15_br_01_signup_creates_user_acceptances_and_session` (+13) | integration+unit | PASS |
| BR-02 | `ac_01_br_02_stores_only_hashes_of_token_and_code`, `ac_01_br_02_config_reads_optional_overrides`, `ac_01_br_02_config_requires_database_url_secret_and_env` (+8) | unit | PASS |
| BR-03 | `ac_01_br_03_valid_body_passes_through`, `ac_01_br_03_sends_email_with_link_code_and_15_minutes`, `ac_08_br_03_token_for_existing_user_issues_session` (+1) | unit | PASS |
| BR-04 | `ac_02_br_04_access_response_is_identical_for_sent_and_rate_limited`, `ac_02_br_04_internal_error_does_not_leak_cause`, `ac_01_br_04_openapi_lists_auth_access_routes` (+2) | unit | PASS |
| BR-05 | `ac_03_br_05_normalizes_email_before_counting_and_storing`, `ac_03_br_05_email_is_trimmed_and_lowercased`, `ac_03_br_05_email_keeps_dots_and_plus` (+1) | integration+unit | PASS |
| BR-06 | `ac_08_br_06_verify_token_sets_session_cookie_without_token_in_body`, `ac_08_br_06_verify_without_credential_is_422`, `ac_09_br_06_verify_code_returns_authenticated` (+14) | integration+unit | PASS |
| BR-07 | `ac_12_br_07_malformed_code_is_422_without_attempts_remaining`, `ac_12_br_07_wrong_code_is_422_with_attempts_remaining`, `ac_12_br_07_problem_can_carry_attempts_remaining` (+8) | integration+unit | PASS |
| BR-08 | `ac_05_br_08_invalidates_open_requests_before_inserting`, `ac_05_br_08_new_request_invalidates_open_ones_of_same_email` | integration+unit | PASS |
| BR-09 | `ac_07_br_09_falls_back_to_socket_when_header_is_missing_or_blank`, `ac_07_br_09_header_is_ignored_when_not_configured`, `ac_07_br_09_trusted_header_is_used_when_configured` (+11) | integration+unit | PASS |
| BR-10 | `ac_20_br_10_clear_cookie_expires_in_the_past`, `ac_20_br_10_read_cookie_ignores_empty_and_garbage`, `ac_20_br_10_read_cookie_returns_the_session_value` (+6) | unit | PASS |
| BR-11 | `ac_21_br_11_session_response_has_no_user_id`, `ac_21_br_11_authenticated_request_renews_the_session`, `ac_22_br_11_expired_session_is_401` (+12) | integration+unit | PASS |
| BR-12 | `ac_25_br_12_logout_all_returns_204`, `ac_24_br_12_logout_clears_cookie_and_returns_204`, `ac_24_br_12_second_logout_with_same_cookie_is_401` (+5) | integration+unit | PASS |
| BR-13 | `ac_27_br_13_accept_terms_with_old_version_is_422`, `ac_15_br_13_signup_returns_201_and_cookie`, `ac_17_br_13_signup_with_old_version_is_422` (+10) | integration+unit | PASS |
| BR-14 | `ac_27_br_14_accept_terms_returns_204_even_when_terms_are_pending`, `ac_27_br_14_accept_terms_without_session_is_401`, `ac_26_br_14_record_with_terms_pending_is_403` (+10) | integration+unit | PASS |
| BR-15 | `ac_19_br_15_signup_with_81_char_display_name_is_422`, `ac_19_br_15_display_name_over_80_chars_is_rejected_before_consuming`, `ac_19_br_15_signup_without_display_name_is_valid` (+2) | unit | PASS |
| BR-16 | `ac_28_br_16_attempt_with_bad_timestamp_or_blank_fields_is_422`, `ac_28_br_16_sync_over_1000_attempts_is_422`, `ac_28_br_16_sync_returns_full_progress` (+14) | integration+unit | PASS |
| BR-17 | `ac_30_br_17_sync_with_empty_list_returns_account_attempts`, `ac_30_br_17_sync_returns_attempts_of_account_not_only_sent`, `ac_30_br_17_list_returns_all_attempts_of_user_only_in_answer_order` (+1) | integration+unit | PASS |
| BR-18 | `ac_31_br_18_record_new_attempt_is_201`, `ac_32_br_18_record_existing_attempt_is_200`, `ac_31_br_18_record_creates_attempt` (+2) | integration+unit | PASS |
| BR-19 | `ac_33_br_19_record_accepts_unknown_question_id`, `ac_33_br_19_record_does_not_check_question_existence`, `ac_33_br_19_attempt_accepts_any_question_id` (+2) | integration+unit | PASS |
| BR-20 | `ac_13_br_20_get_on_verify_route_is_405`, `ac_13_br_20_token_is_consumed_once_per_execute` | unit | PASS |
| BR-21 | `ac_15_br_21_verify_for_unknown_email_returns_terms_required`, `ac_16_br_21_no_signup_token_means_no_user`, `ac_15_br_21_unknown_email_returns_terms_required_without_creating_user` | unit | PASS |
| BR-22 | `ac_16_br_22_signup_with_expired_token_is_410`, `ac_18_br_22_settings_signup_window_is_15_minutes`, `ac_18_br_22_expired_signup_token_is_gone` (+1) | integration+unit | PASS |
| BR-23 | `ac_23_br_23_label_falls_back_when_unknown`, `ac_23_br_23_label_names_browser_and_system`, `ac_23_br_23_issue_stores_hash_and_label_not_the_token` (+1) | integration+unit | PASS |
| BR-24 | `ac_04_br_24_invalid_email_is_422_invalid_email_format`, `ac_04_br_24_problem_json_has_type_title_status_detail`, `ac_04_br_24_malformed_body_is_problem_json` (+7) | unit | PASS |

## Changed repositories

| repo | branch | commits |
|---|---|---|
| medsafari | `feat/login-register-backend` | 24 (17 tarefas do plano, 1 correção do timeout do pool, 5 de refatoração de estrutura e 1 de configuração por `.env`) |

## Failures and retries

Nenhuma falha na verificação final. `verifyRetries` = 2: o retry 1 foi a mudança de estrutura e o retry 2 foi a configuração por `.env`, ambos pedidos pelo humano depois de uma verificação aprovada nos testes.

### Configuração por `.env` (retry 2)

Pedido: tirar valores fixos do código e guardar configuração e segredos num `.env`.

- `LISTEN_ADDR` deixou de ser constante: a API lê a variável (padrão `127.0.0.1:3000`, que o `proxy.conf.json` do frontend espera) e recusa valor inválido. A constante virou `DEFAULT_LISTEN_ADDR`.
- Novo módulo `bootstrap/src/dotenv.rs` (`Env`): procura o `.env` no diretório atual e nos pais, sem alterar o ambiente do processo; a variável de ambiente de verdade tem precedência. Sem `.env` segue só com o ambiente; arquivo malformado é erro. `main.rs` e o binário `migrate` usam o mesmo caminho. Dependência nova: `dotenvy`.
- `backend/.env.example` documenta cada variável (placeholder `AUTH_SECRET=change-me`, que a API recusa); `dev/init-env.sh` cria o `.env` com um segredo aleatório e permissão 600 e não sobrescreve um existente; `dev/db.sh up` agora aponta para ele.
- Continuam como padrões no código, de propósito: os limites de negócio (`AuthSettings`, ajustáveis com dados do piloto), o tamanho e o timeout do pool, o caminho do link `/entrar/confirmar` e o nome do cookie `session`, que fazem parte do contrato com o frontend.

### Refatoração de estrutura (retry 1)

Premissa: um item por arquivo, pastas por tipo, `<nome>.<tipo>.rs`, testes unitários em `__tests__/`. Só os caminhos mudaram: nomes de teste, comportamento e caminhos públicos (`application::X`, `domain::X`) ficaram iguais por reexport. A cada crate o conjunto de testes foi comparado com o baseline antes do commit; nos cinco foi idêntico.

- `domain`: `entities/`, `value_objects/`, `errors/`.
- `application`: `repositories/`, `ports/`, `usecases/`, `errors/`; `ports.rs` deixou de existir. `settings.rs` ficou na raiz.
- `adapters-postgres`: `repositories/` (uma implementação por porta), `database.rs`, `pg_store.rs`.
- `adapters-http`: `controllers/` (um por rota), `dtos/`, `middlewares/`, `router.rs`; helpers de erro compartilhados foram para `error.rs`.
- `bootstrap`: um arquivo por adaptador e por responsabilidade, em `src/`.

Pontos que seguem decisões [PROPOSED] dos guias e precisam de confirmação (GAPS #13): `errors/port.error.rs` na `application`, `middlewares/` com `.middleware.rs`, e como arquivos planos da raiz `settings.rs`, `state.rs`, `cookie.rs`, `client_ip.rs`, `json.rs`, `user_agent_label.rs`, `test_support.rs`, `router.rs` e os adaptadores do `bootstrap`.

### Ocorrências durante a fase CODE (tentativa 1)

- **Falha intermitente de integração, não reproduzida.** Ao fechar a Task 17, `ac_15_br_13_failed_acceptance_rolls_back_the_user` falhou uma vez. Reexecutei: 6 execuções isoladas do teste e 4 rodadas completas (44/44) passaram, e as rodadas de verificação das duas tentativas também. A causa não foi identificada; se voltar a aparecer, o primeiro passo é capturar a saída completa do teste.
- **Commit com integração vermelha.** Por causa do pipeline do meu script de apoio, o commit da Task 17 (`c0b9faa`) foi criado mesmo com essa falha. O código desse commit é o mesmo que passou nas rodadas seguintes; o script foi corrigido para parar na falha.
- **Task 17 passou de primeira.** O teste de fluxo completo só falhou por compilação (faltava `build_router_with_email`) e depois passou sem ajuste de comportamento. Ele funciona como teste de regressão ponta a ponta.

### Desvios do plano aprovado

- `RequestAccess::new` e `CompleteSignup::new` recebem também o `IdGenerator`; `VerifyAccess::new` não o recebe.
- `router(health)` manteve a assinatura; as rotas de acesso, sessão e progresso estão em `auth_router(api)`, e o `bootstrap` junta os dois com `merge`.
- O `bootstrap` não usa o `sqlx` diretamente: `adapters-postgres` expõe `PgPool`, `connect`, `connect_lazy`, `migrate` e `applied_migrations`, mantendo o teste de arquitetura que só permite o `sqlx` nesse crate.
- `APP_ENV` é obrigatório (`dev`); `prod` recusa subir enquanto não houver provedor real de e-mail.
- `Config::from_env` passou a ler também o `.env` (`Env::load`), e a constante pública `LISTEN_ADDR` deixou de existir (`DEFAULT_LISTEN_ADDR` e `Config::listen_addr`).
- Foi acrescentado `build_router_with_email` para os testes de fluxo completo capturarem link e código.
- Filtros do nextest: `unit` = `not (package(adapters-postgres) | binary(auth_flow))`, `integration` = `package(adapters-postgres) | binary(auth_flow)`.
- Timeout de aquisição de conexão do pool reduzido para 5 s (commit `36784a5`).
