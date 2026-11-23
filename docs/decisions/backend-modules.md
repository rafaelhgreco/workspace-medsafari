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
