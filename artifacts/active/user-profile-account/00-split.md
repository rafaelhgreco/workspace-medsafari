# Split: user-profile-account em backend e frontend

Fonte: coleta de refino (a anexar em `delivery/`).

Duas partes da mesma história, no mesmo workspace. Cada uma percorre o fluxo completo (Tiger → Turtle → Termite). **Neste momento só a parte backend será desenvolvida.** O frontend só inicia depois que o backend chegar a `done`, pois consome o contrato real da API.

| Ordem | Parte | demandType | dependsOn | Repositório |
|---|---|---|---|---|
| 1 | `user-profile-account/backend` | backend | - | `repos/medsafari` (a confirmar no intake) |
| 2 | `user-profile-account/frontend` | frontend | `backend` | a definir (fora do escopo agora) |

## 1. Escopo de backend

A preencher após o refino. O Tiger da parte herda só este escopo.

## 2. Escopo de frontend

Adiado. Será definido quando o backend estiver `done`.

## 3. Contrato entre as partes

A forma exata (rotas, payloads, erros) será decidida pelo Turtle do backend e registrada em `backend/delivery/02-tech-spec.md`.

## 4. Dependências e riscos

- Depende do módulo de login/sessão (`login-register`, arquivado): perfil e conta pressupõem usuário autenticado.
- Demais pontos a levantar no refino.

## 5. Próximos passos

1. Anexar a coleta/refino em `delivery/` e completar a seção 1.
2. Rodar `/tiger user-profile-account/backend`.
3. Frontend só depois do backend `done`.
