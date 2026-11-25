# Backend em módulos (hexagonal)

Decisão de 2026-11-23. O backend passa a ser organizado por **módulo** e, dentro dele, por **tipo**, sem mudar comportamento.

## Decisões

1. Caminho: `crates/<crate>/src/modules/<modulo>/<tipo>/<nome>.<tipo>.rs`; o módulo tem o mesmo nome em todos os crates.
2. Módulos iniciais: `health`, `auth`, `progress`, mais `shared/` em cada crate (`Clock`, `PortError`, `SystemClock`). Única dependência entre módulos: `progress` -> `auth` (via `SessionService`), sem ciclos. `auth` só é dividido quando um fluxo novo justificar.
3. O `mod.rs` do módulo é a API pública: pastas de tipo privadas, `pub use` só do necessário, mocks sob `#[cfg(any(test, feature = "mocks"))]`.
4. Ficam na raiz do crate: `settings.rs`, `config.rs`, `dotenv.rs`, `wiring.rs`, `router.rs`, `state.rs`, `openapi.rs`, `error.rs`, `json.rs`, `database.rs`, `pg_store.rs`, `client_ip.rs`, `cookie.rs`, `user_agent_label.rs`; seus testes continuam em `src/__tests__/`.
5. `DomainError` é dividido por módulo (única mudança de tipos). `SessionService` e os tipos que moram em arquivos de repositório ficam como estão.
6. Testes unitários seguem em `__tests__/` dentro do módulo; testes de integração e migrations não mudam de lugar.
7. Fiação: `wiring.rs` só compõe; cada módulo ganha `<modulo>.module.rs`.

## Referências

- [project-structure-general](../../knowledge/guides/commons/project-structure-general.md)
- [structure-guide-backend](../../knowledge/guides/backend/structure-guide-backend.md)
- [GAPS](../../knowledge/guides/GAPS.md)

## Resultado

Executado em 2026-11-23 na branch `refactor/backend-modules` de `repos/medsafari`, fora do fluxo Tiger/Turtle/Termite (refatoração independente, sem história funcional). Sem push.

Commits: `514aea9` (`health`), `7504ddf` (`progress`), `688d833` (`auth` e `shared`, `DomainError` dividido), `1c5c7ee` (guarda em `architecture.rs`).

Evidência: lista de testes unitários igual ao baseline (175) mais 5 testes novos da guarda; perfis `unit` (180) e `integration` (44) verdes; JSON do OpenAPI idêntico; sem testes órfãos; única aresta `progress -> auth`; `E0603` ao importar a pasta de tipo de outro módulo; `Cargo.toml`, migrations e `frontend/` sem alteração; asserts alterados só pela troca de `DomainError` por `HealthError`/`AuthError`.

O que divergiu da proposta:
- Dois testes que misturavam módulos mudaram de arquivo, sem mudar nome nem asserts: `ac_15_br_01_..._value_equality` foi para `progress` (domain) e `ac_21_br_11_system_clock_and_id_generator_...` foi para `auth` (bootstrap), para não criar `auth -> progress` nem `shared -> auth`.
- `test_support.rs` (adapters-http) também ficou na raiz.
- `From<...Error> for ApiError` continua em `adapters-http/src/error.rs` (GAPS #25).
- Os `mod.rs` dos módulos reexportam todos os itens públicos; a poda não foi feita.
- Os commits rodaram com o hook de pre-commit ativo, sem `LEFTHOOK=0`.
- A guarda foi escrita depois da migração, sem passo RED.
- Pendente: graphify do repo (rodado depois pelo responsável).
