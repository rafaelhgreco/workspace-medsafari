# Rotas de health: live e ready

Demanda DEM-20261114-health-live-ready · 2026-11-14.

Separar a consulta de saúde do backend em duas rotas de operação: `live` (o processo está no ar) e `ready` (a aplicação está pronta para receber tráfego), mantendo a rota `/api/health` existente sem alterações.

## Business rules

| ID | Rule | Rationale | Source |
|---|---|---|---|
| BR-01 | A rota `GET /api/health/live` responde 200 com o corpo `{"status":"ok"}` sempre que o processo estiver em execução. | Permitir que a plataforma saiba se o processo está vivo. | demand |
| BR-02 | A rota `GET /api/health/ready` responde 200 com o corpo `{"status":"ready"}` quando a aplicação está pronta para receber tráfego. | Permitir que a plataforma só envie tráfego a instâncias prontas. | demand |
| BR-03 | Enquanto a aplicação não tiver dependências externas, ela é considerada pronta assim que está em execução; o caso `503 {"status":"not_ready"}` está fora do escopo até existir uma dependência a verificar. | Evitar regras de prontidão sem nada a verificar. | human answer |
| BR-04 | A rota `GET /api/health` continua respondendo 200 com `{"status":"ok","version":"<versão>"}`, sem alteração. | Não quebrar quem já usa a rota existente. | human answer |
| BR-05 | As três rotas de health são públicas (não exigem autenticação) e aceitam somente o método GET. | Permitir sondagens da plataforma sem credenciais. | human answer |
| BR-06 | As respostas de `live` e de `ready` não incluem o campo `version`. | Manter as sondas mínimas; a versão continua em `/api/health`. | human answer |
| BR-07 | O arquivo `backend/docs/requests.http` lista as requisições das rotas `live` e `ready`. | Facilitar o teste manual das novas rotas. | human answer |
| BR-08 | Métodos diferentes de GET nas rotas de health recebem 405 (Method Not Allowed). | Deixar explícito o comportamento para métodos não aceitos (BR-05). | inferred |

## Epics and stories

### EP-01 Rotas de saúde da aplicação

Disponibilizar sondas de liveness e readiness sem alterar a rota de saúde existente.

#### ST-01 Consultar se o processo está vivo

- As a operador da plataforma
- I want consultar `GET /api/health/live`
- So that eu saiba se o processo está em execução

**Functional tasks**
- FT-01 Disponibilizar a rota `GET /api/health/live` com a resposta `{"status":"ok"}` e sem `version`.

**Acceptance criteria**

```gherkin
@AC-01 @BR-01
Scenario: Processo em execução responde ok
  Given a aplicação está em execução
  When um cliente faz GET em /api/health/live
  Then a resposta tem status 200
  And o corpo é {"status":"ok"}

@AC-02 @BR-06
Scenario: A resposta de live não inclui a versão
  Given a aplicação está em execução
  When um cliente faz GET em /api/health/live
  Then o corpo não contém o campo "version"
```

#### ST-02 Consultar se a aplicação está pronta

- As a operador da plataforma
- I want consultar `GET /api/health/ready`
- So that eu saiba se a instância pode receber tráfego

**Functional tasks**
- FT-02 Disponibilizar a rota `GET /api/health/ready` com a resposta `{"status":"ready"}` e sem `version`.

**Acceptance criteria**

```gherkin
@AC-03 @BR-02 @BR-03
Scenario: Aplicação sem dependências externas está pronta
  Given a aplicação está em execução e não possui dependências externas
  When um cliente faz GET em /api/health/ready
  Then a resposta tem status 200
  And o corpo é {"status":"ready"}

@AC-04 @BR-06
Scenario: A resposta de ready não inclui a versão
  Given a aplicação está em execução
  When um cliente faz GET em /api/health/ready
  Then o corpo não contém o campo "version"
```

#### ST-03 Manter o health existente e o acesso às rotas

- As a operador da plataforma
- I want que `/api/health` continue igual e que as rotas de health sejam públicas e somente GET
- So that as sondas e os usos atuais continuem funcionando

**Functional tasks**
- FT-03 Manter a resposta atual de `GET /api/health`.
- FT-04 Manter as rotas de health públicas e aceitar somente GET.

**Acceptance criteria**

```gherkin
@AC-05 @BR-04
Scenario: A rota existente não muda
  Given a aplicação está em execução
  When um cliente faz GET em /api/health
  Then a resposta tem status 200
  And o corpo contém "status" igual a "ok" e o campo "version"

@AC-06 @BR-05
Scenario: As rotas de health não exigem autenticação
  Given um cliente sem credenciais
  When o cliente faz GET em /api/health, /api/health/live e /api/health/ready
  Then cada resposta tem status 200

@AC-07 @BR-05 @BR-08
Scenario: Método diferente de GET é recusado
  Given a aplicação está em execução
  When um cliente faz POST em /api/health/live
  Then a resposta tem status 405
```

#### ST-04 Documentar as novas rotas

- As a pessoa desenvolvedora do backend
- I want ter as requisições das novas rotas no arquivo de exemplos
- So that eu possa testá-las manualmente

**Functional tasks**
- FT-05 Incluir as requisições de `live` e `ready` em `backend/docs/requests.http`.

**Acceptance criteria**

```gherkin
@AC-08 @BR-07
Scenario: Exemplos de requisição das novas rotas
  Given o arquivo backend/docs/requests.http
  When a pessoa desenvolvedora o consulta
  Then ele contém uma requisição GET para /api/health/live
  And ele contém uma requisição GET para /api/health/ready
```

## Use cases

### UC-01 Consultar a saúde da aplicação

- **Actor:** Operador da plataforma (orquestrador ou monitoramento)
- **Preconditions:** A aplicação está em execução.
- **Postconditions:** O operador sabe se o processo está vivo e se a instância está pronta.
- **Main flow:**
  1. O operador faz GET em `/api/health/live`.
  2. O sistema responde 200 com `{"status":"ok"}`.
  3. O operador faz GET em `/api/health/ready`.
  4. O sistema responde 200 com `{"status":"ready"}`.
- **Alternative flows:**
  - 1a. O operador consulta `/api/health`: o sistema responde 200 com `status` e `version`, como hoje.
- **Exceptions:**
  - E1. O operador usa um método diferente de GET: o sistema responde 405.
- **Related:** BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-08, ST-01, ST-02, ST-03

## Traceability

| BR | AC | UC | ST |
|---|---|---|---|
| BR-01 | AC-01 | UC-01 | ST-01 |
| BR-06 | AC-02 | UC-01 | ST-01 |
| BR-02, BR-03 | AC-03 | UC-01 | ST-02 |
| BR-06 | AC-04 | UC-01 | ST-02 |
| BR-04 | AC-05 | UC-01 | ST-03 |
| BR-05 | AC-06 | UC-01 | ST-03 |
| BR-05, BR-08 | AC-07 | UC-01 | ST-03 |
| BR-07 | AC-08 | - | ST-04 |

## Open questions

| ID | Question | Related | Status |
|---|---|---|---|
| OQ-01 | Métodos diferentes de GET devem responder 405? (BR-08 foi inferida a partir de BR-05.) | BR-08 | open |
| OQ-02 | Quando existir uma dependência externa, quais falhas devem deixar `ready` em 503? (Fora do escopo desta demanda, conforme BR-03.) | BR-03 | open |
