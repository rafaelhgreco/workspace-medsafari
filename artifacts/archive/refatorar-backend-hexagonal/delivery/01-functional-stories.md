# Refatorar backend Rust para arquitetura hexagonal

Demand DEM-20261118-refatorar-backend-hexagonal · 2026-11-18.

O backend atual é um único `main.rs` que concentra contrato, estado, handler, roteamento, inicialização e testes do endpoint de saúde. A demanda reorganiza esse backend segundo a arquitetura hexagonal definida nos guias do workspace, preservando o comportamento observável e entregando o ferramental de desenvolvimento exigido pelos guias.

## Business rules

| ID | Rule | Rationale | Source |
|---|---|---|---|
| BR-01 | O endpoint `GET /api/health` continua respondendo 200 com `{"status":"ok","version":"<versão do pacote>"}` e o servidor continua escutando em `127.0.0.1:3000`. | Clientes e o frontend dependem do contrato atual; a refatoração não pode mudá-lo. | human answer |
| BR-02 | O código do backend é organizado em camadas `domain`, `application`, `adapters-http` e `bootstrap`, e cada camada só pode depender das camadas internas a ela. | Isolar regras de negócio de frameworks e infraestrutura. | demand |
| BR-03 | A camada de domínio não depende de nenhuma outra camada, de runtime assíncrono nem de tipos de framework. | Mantém o núcleo testável e independente de tecnologia. | demand |
| BR-04 | A obtenção da versão da aplicação é um caso de uso da camada de aplicação, acessado por uma porta (contrato) que o adaptador de composição implementa. | Torna o comportamento substituível e testável sem a infraestrutura real. | human answer |
| BR-05 | Falhas são representadas por tipos de erro próprios de cada camada e apresentadas ao cliente HTTP no formato `application/problem+json`, sem expor tipos de infraestrutura às camadas internas. | Padroniza o tratamento de erros e evita vazamento de detalhes internos. | demand |
| BR-06 | A superfície HTTP é descrita por um documento OpenAPI exposto em `GET /api-docs/openapi.json`, que lista o endpoint de saúde. | Permite ao frontend gerar o cliente a partir de um contrato publicado. | human answer |
| BR-07 | Somente a camada de composição (`bootstrap`) liga adaptadores concretos aos casos de uso e inicia o servidor; ela não contém regra de negócio. | Concentra a configuração em um único ponto. | demand |
| BR-08 | Todo comportamento do backend é coberto por testes unitários rastreáveis que rodam sem Docker nem banco de dados. | Feedback rápido e determinístico. | demand |
| BR-09 | Formatação, lint sem avisos e testes unitários são verificados automaticamente antes de cada commit. | Impede regressão de qualidade e mantém o padrão do time. | human answer |
| BR-10 | O ambiente de desenvolvimento disponibiliza as ferramentas e dependências previstas nos guias: `cargo-nextest` com perfil `unit`, `lefthook`, e as bibliotecas `thiserror`, `async-trait`, `utoipa`, `sqlx`, `mockall`, `tracing` e `tower-http`, mais a ferramenta `sqlx-cli`, declaradas no nível do workspace. | Garante que qualquer desenvolvedor aplique os guias sem configuração manual. | human answer |
| BR-11 | O crate `adapters-postgres`, as migrations, o perfil de testes `integration`, a autenticação e o frontend ficam fora desta entrega; o `sqlx` é apenas disponibilizado como dependência do workspace, sem uso no código. | O backend ainda não tem caso de uso com persistência; a dependência fica pronta para a próxima demanda. | human answer |

## Epics and stories

### EP-01 Backend em arquitetura hexagonal

Reorganizar o backend em camadas isoladas, sem alterar o contrato do endpoint de saúde, com contrato OpenAPI publicado e ferramental de qualidade ativo.

#### ST-01 Manter o contrato do endpoint de saúde

- As a consumidor da API
- I want que `GET /api/health` continue respondendo como antes
- So that nenhuma integração existente quebre com a refatoração

**Functional tasks**
- FT-01 Responder 200 com status `ok` e a versão do pacote em `GET /api/health`.
- FT-02 Continuar escutando em `127.0.0.1:3000`.

**Acceptance criteria**

```gherkin
@AC-01 @BR-01 @BR-04
Scenario: Consultar a saúde da aplicação
  Given o backend refatorado em execução
  When um consumidor faz GET em /api/health
  Then a resposta tem status 200
  And o corpo contém status "ok" e a versão do pacote

@AC-02 @BR-01
Scenario: Endereço de escuta preservado
  Given o backend refatorado iniciado sem configuração adicional
  When o servidor está pronto
  Then ele atende requisições em 127.0.0.1 na porta 3000

@AC-03 @BR-05
Scenario: Falha ao obter a versão
  Given que a obtenção da versão falha
  When um consumidor faz GET em /api/health
  Then a resposta tem status 500 com tipo de conteúdo application/problem+json
  And o corpo não expõe detalhes internos da falha
```

#### ST-02 Separar o backend em camadas hexagonais

- As a desenvolvedor do backend
- I want o código dividido em domínio, aplicação, adaptador HTTP e composição
- So that eu evolua regras de negócio sem acoplamento a frameworks

**Functional tasks**
- FT-03 Isolar o domínio sem dependências de outras camadas, de runtime assíncrono ou de framework.
- FT-04 Expor a obtenção da versão como caso de uso acessado por uma porta.
- FT-05 Concentrar a ligação dos adaptadores e a inicialização do servidor na composição.

**Acceptance criteria**

```gherkin
@AC-04 @BR-02 @BR-03
Scenario: Regra de dependência entre camadas respeitada
  Given o backend organizado em camadas
  When as dependências de cada camada são inspecionadas
  Then o domínio não depende de nenhuma outra camada nem de framework
  And a aplicação depende apenas do domínio
  And o adaptador HTTP não depende da composição

@AC-05 @BR-04
Scenario: Caso de uso testável com porta substituída
  Given uma porta de versão substituída por um duplo de teste
  When o caso de uso de consulta da versão é executado
  Then ele devolve a versão fornecida pelo duplo
  And nenhuma infraestrutura real é usada

@AC-06 @BR-07
Scenario: Composição sem regra de negócio
  Given a camada de composição
  When seu conteúdo é revisado
  Then ela apenas lê configuração, liga adaptadores aos casos de uso e inicia o servidor
```

#### ST-03 Publicar o contrato OpenAPI

- As a desenvolvedor do frontend
- I want obter o documento OpenAPI do backend
- So that eu gere o cliente da API a partir do contrato

**Functional tasks**
- FT-06 Expor o documento OpenAPI em `GET /api-docs/openapi.json`.
- FT-07 Descrever o endpoint de saúde e o formato de erro no documento.

**Acceptance criteria**

```gherkin
@AC-07 @BR-06
Scenario: Obter o documento OpenAPI
  Given o backend em execução
  When um consumidor faz GET em /api-docs/openapi.json
  Then a resposta tem status 200 com um documento OpenAPI válido
  And o documento descreve GET /api/health

@AC-08 @BR-05
Scenario: Erro apresentado como problem+json
  Given um caso de uso que falha com erro de aplicação
  When o adaptador HTTP converte o erro em resposta
  Then o corpo segue application/problem+json com type, title, status e detail
```

#### ST-04 Ferramental de qualidade e dependências do time

- As a desenvolvedor do backend
- I want ferramentas e dependências dos guias disponíveis e verificações automáticas no commit
- So that todo código siga o mesmo padrão sem configuração manual

**Functional tasks**
- FT-08 Disponibilizar `cargo-nextest` com perfil `unit`, `lefthook` e as bibliotecas dos guias no nível do workspace.
- FT-09 Executar formatação, lint sem avisos e testes unitários antes de cada commit.
- FT-10 Rodar os testes unitários sem Docker nem banco de dados.

**Acceptance criteria**

```gherkin
@AC-09 @BR-08 @BR-10
Scenario: Testes unitários isolados
  Given o ambiente sem Docker e sem banco de dados
  When os testes unitários são executados pelo perfil unit
  Then todos passam
  And cada teste cita a regra de negócio que verifica

@AC-10 @BR-09
Scenario: Verificação antes do commit
  Given código com problema de formatação ou aviso de lint
  When o desenvolvedor tenta commitar com as verificações ativas
  Then o commit é recusado com a indicação do problema

@AC-11 @BR-09
Scenario: Código conforme é aceito
  Given código formatado, sem avisos de lint e com testes passando
  When o desenvolvedor tenta commitar com as verificações ativas
  Then o commit é aceito

@AC-12 @BR-10
Scenario: Dependências no nível do workspace
  Given o workspace do backend
  When as dependências são inspecionadas
  Then thiserror, async-trait, utoipa, sqlx, mockall, tracing e tower-http estão declaradas no nível do workspace

@AC-13 @BR-11
Scenario: Persistência fora do escopo
  Given o backend refatorado
  When os crates e dependências são listados
  Then não existem crate de adaptador Postgres, migrations nem perfil integration
  And o sqlx não é usado por nenhum crate
```

## Use cases

### UC-01 Consultar a saúde da aplicação

- **Actor:** Consumidor da API
- **Preconditions:** O backend está em execução.
- **Postconditions:** O consumidor conhece o estado e a versão da aplicação; nada é alterado.
- **Main flow:**
  1. O consumidor solicita o estado de saúde.
  2. O sistema obtém a versão da aplicação.
  3. O sistema responde com status "ok" e a versão.
- **Alternative flows:**
  - 1a. O consumidor solicita o documento do contrato; o sistema devolve o OpenAPI com a descrição da consulta de saúde.
- **Exceptions:**
  - E1. A obtenção da versão falha: o sistema responde com erro padronizado (problem+json) sem expor detalhes internos.
- **Related:** BR-01, BR-04, BR-05, BR-06, ST-01, ST-03

### UC-02 Evoluir o backend respeitando as camadas

- **Actor:** Desenvolvedor do backend
- **Preconditions:** O ambiente tem as ferramentas e dependências dos guias instaladas.
- **Postconditions:** A mudança está commitada, verificada e coberta por testes unitários rastreáveis.
- **Main flow:**
  1. O desenvolvedor escreve primeiro o teste da mudança.
  2. O desenvolvedor implementa a mudança na camada correta, do domínio para fora.
  3. O desenvolvedor executa os testes unitários, sem Docker nem banco.
  4. O desenvolvedor realiza o commit.
  5. O sistema executa formatação, lint e testes antes de aceitar o commit.
- **Alternative flows:**
  - 2a. A mudança exige nova capacidade: o desenvolvedor define antes a porta na camada de aplicação.
- **Exceptions:**
  - E1. Formatação ou lint com problema, ou teste falhando: o commit é recusado com a indicação do problema.
  - E2. A mudança faz uma camada depender de uma camada externa: a regra de dependência é violada e a mudança deve ser corrigida.
- **Related:** BR-02, BR-03, BR-07, BR-08, BR-09, BR-10, BR-11, ST-02, ST-04

## Traceability

| BR | AC | UC | ST |
|---|---|---|---|
| BR-01, BR-04 | AC-01 | UC-01 | ST-01 |
| BR-01 | AC-02 | UC-01 | ST-01 |
| BR-05 | AC-03 | UC-01 | ST-01 |
| BR-02, BR-03 | AC-04 | UC-02 | ST-02 |
| BR-04 | AC-05 | - | ST-02 |
| BR-07 | AC-06 | UC-02 | ST-02 |
| BR-06 | AC-07 | UC-01 | ST-03 |
| BR-05 | AC-08 | UC-01 | ST-03 |
| BR-08, BR-10 | AC-09 | UC-02 | ST-04 |
| BR-09 | AC-10 | UC-02 | ST-04 |
| BR-09 | AC-11 | UC-02 | ST-04 |
| BR-10 | AC-12 | UC-02 | ST-04 |
| BR-11 | AC-13 | UC-02 | ST-04 |

## Open questions

| ID | Question | Related | Status |
|---|---|---|---|
| OQ-01 | A obtenção da versão hoje não falha. AC-03 pressupõe que a porta pode falhar (erro tipado, resposta 500 em problem+json). Manter a porta falível para exercitar o tratamento de erros? Proposta: sim. | BR-04, BR-05 | open |
| OQ-02 | `tracing` e `tower-http` entram só como dependências do workspace, sem a pilha de middlewares (request id, timeout, CORS, autenticação). Confirmar que a pilha fica para outra demanda. Proposta: sim. | BR-10 | open |
| OQ-03 | O `sqlx` fica declarado sem uso. Confirmar que não há problema em uma dependência sem consumidor (lints como `cargo-udeps` não fazem parte do escopo). Proposta: sim. | BR-11 | open |
