# Refatorar backend Rust para arquitetura hexagonal - Verification report

Demand DEM-20261118-refatorar-backend-hexagonal · 2026-11-18 · Branch `refactor/backend-hexagonal` (repo `medsafari`)

## Summary

**PASS com ressalvas** · tentativa 1 (`verifyRetries` = 0).

Todos os comandos de verificação terminaram com código 0 e os 19 testes unitários passaram. Ressalvas que dependem de decisão humana:

1. **Teste de fumaça do binário: resolvido.** Na primeira tentativa a porta 3000 estava ocupada por um processo `backend` anterior à refatoração (pid 30993, binário antigo). O usuário o encerrou e o teste foi refeito com o binário novo: `GET /api/health` -> 200 `{"status":"ok","version":"0.1.0"}` (`content-type: application/json`); `GET /api-docs/openapi.json` -> OpenAPI `3.1.0` com o path `/api/health` e os schemas `HealthResponse` e `Problem`; escuta em `127.0.0.1:3000`. O processo foi encerrado ao final.
2. **AC-06 sem teste automático**, por decisão registrada na spec (INF-10): verificado por revisão (`main.rs` com 14 linhas, só configuração e fiação; nenhum `fn health`, `struct Health` ou `trait VersionProvider` em `crates/bootstrap/src`).
3. **AC-10/AC-11** foram demonstrados rodando `lefthook run pre-commit` (RED: `fmt` reprovou com formatação quebrada; GREEN: `fmt`, `clippy` e `unit` aprovados com `--all-files`). Os commits das tarefas usaram `LEFTHOOK=0`, como manda o guia, então nenhum commit passou pelo hook. O código de saída do run vermelho não foi capturado (a saída passou por um pipe); o marcador de falha do `fmt` foi observado.
4. O `cargo` emite avisos informativos `unused workspace dependency` para `async-trait`, `sqlx`, `tracing` e `tower-http` (4 avisos), que são declaradas de propósito e sem uso (BR-10, BR-11). Não afetam o código de saída de `clippy -D warnings`.

## Commands

| command | repo | exit code | result |
|---|---|---|---|
| `cargo fmt --check` | medsafari/backend | 0 | sem diferenças |
| `cargo clippy --workspace -- -D warnings` | medsafari/backend | 0 | sem avisos de código |
| `cargo nextest run --workspace --profile unit` | medsafari/backend | 0 | 19 testes, 19 passaram, 0 falharam, 0 ignorados |
| `lefthook run pre-commit --all-files` | medsafari | 0 | `fmt`, `clippy` e `unit` aprovados |
| `docker info` / perfil `integration` | medsafari | n/a | não aplicável: nenhuma tarefa é `unit+integration` |
| frontend (`npm run lint`, testes) | medsafari/frontend | n/a | fora do escopo (demanda `backend`) |
| smoke: `target/debug/backend` + `curl` (health, openapi, `ss -ltn`) | medsafari/backend | 0 | health 200 com `ok`/`0.1.0`; OpenAPI 3.1.0 com `/api/health`; escuta em 127.0.0.1:3000 |

## Traceability

| ID | Teste (crate · nome) | Tipo | Resultado |
|---|---|---|---|
| AC-01 / BR-01, BR-04 | `adapters-http` · `ac_01_br_01_health_returns_200_with_ok_and_version`; `bootstrap` · `ac_01_br_01_router_serves_health_with_package_version`; `application` · `ac_01_br_01_reports_status_ok` | unit | PASS |
| AC-02 / BR-01 | `bootstrap` · `ac_02_br_01_listens_on_127_0_0_1_3000` (valida a constante `LISTEN_ADDR`); smoke test: `ss -ltn` mostrou o binário escutando em `127.0.0.1:3000` | unit + smoke | PASS |
| AC-03 / BR-05 | `adapters-http` · `ac_03_br_05_health_failure_is_problem_json_without_cause`, `ac_03_br_05_empty_version_is_problem_json`; `application` · `ac_03_br_05_propagates_version_failure` | unit | PASS |
| AC-04 / BR-02, BR-03 | `bootstrap` (tests/architecture.rs) · `ac_04_br_02_layers_only_depend_inward`, `ac_04_br_03_domain_has_no_framework_or_runtime_dependency`; `domain` · `ac_04_br_03_app_version_accepts_non_empty_text`, `..._rejects_empty_text`, `..._rejects_blank_text` | unit | PASS |
| AC-05 / BR-04 | `application` · `ac_05_br_04_returns_version_from_replaced_port`; `bootstrap` · `ac_01_br_04_cargo_version_reads_package_version` | unit | PASS |
| AC-06 / BR-07 | sem teste automático (INF-10); revisão: `crates/bootstrap/src/main.rs` (14 linhas) e `grep` sem ocorrências do código antigo | revisão | PASS por revisão |
| AC-07 / BR-06 | `adapters-http` · `ac_07_br_06_openapi_describes_health` | unit | PASS |
| AC-08 / BR-05 | `adapters-http` · `ac_08_br_05_error_body_has_problem_fields` | unit | PASS |
| AC-09 / BR-08, BR-10 | execução completa do perfil `unit` (19 testes, sem Docker nem banco); todos os testes têm nome `ac_<nn>_br_<nn>_...` | unit | PASS |
| AC-10 / BR-09 | `lefthook run pre-commit` com formatação quebrada: job `fmt` reprovou (demonstração manual, Task 7) | manual | PASS (ver ressalva 3) |
| AC-11 / BR-09 | `lefthook run pre-commit --all-files`, saída 0, três jobs aprovados | manual | PASS (ver ressalva 3) |
| AC-12 / BR-10 | `Cargo.toml` `[workspace.dependencies]` contém `thiserror`, `async-trait`, `utoipa`, `sqlx`, `mockall`, `tracing`, `tower-http`; `cargo-nextest` 0.9.152, `sqlx-cli` 0.9.1 e `lefthook` 2.2.2 instalados | inspeção | PASS |
| AC-13 / BR-11 | `bootstrap` · `ac_13_br_11_no_postgres_crate_and_no_sqlx_user`; não existem `crates/adapters-postgres`, `migrations/` nem perfil `integration` | unit | PASS |

Cada BR-01..BR-11 aparece em ao menos uma linha acima. A prova de RED do teste de arquitetura foi feita injetando violações (tokio no domain, sqlx na application, crate não classificado): os três testes falharam e passaram de volta após reverter.

## Changed repositories

| repo | branch | commits |
|---|---|---|
| medsafari | `refactor/backend-hexagonal` | 7 (`1875a03`, `912c1a8`, `ec3cd65`, `87add74`, `fbfcfe0`, `ad0af72`, `7f1a5fe`) |

## Failures and retries

Nenhuma falha de verificação; `verifyRetries` permanece 0. Ocorrências durante o CODE, todas resolvidas antes do commit da tarefa:
- Task 1: `rustfmt` recusou `lib.rs` vazio; o filtro do nextest com `package(adapters-postgres)` é recusado enquanto o pacote não existe (risco R-04). O perfil `unit` ficou sem filtro, com comentário; o filtro entra junto com o crate Postgres.
- Task 6: a injeção de violação `domain -> application` criou um ciclo e quebrou o `cargo metadata`; refeita sem ciclo e revertida com `git checkout` dos arquivos commitados.
