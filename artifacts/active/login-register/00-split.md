# Split: login-register em backend e frontend

Fonte: `delivery/01-login-e-cadastro-coleta-tech.md` (módulo 01, v2, decisões D-01 a D-10).

Duas partes distintas e correlacionadas da mesma história, no mesmo workspace (`backend/` e `frontend/`). Cada uma percorre o fluxo completo (Tiger → Turtle → Termite). **O frontend só inicia depois que o backend chegar a `done`**, porque consome o contrato real da API.

| Ordem | Slug | demandType | Repositório |
|---|---|---|---|
| 1 | `login-register/backend` | backend | `repos/medsafari` (a confirmar no intake) |
| 2 | `login-register/frontend` | frontend | repositório Angular (ainda não está em `repos/`) |

A coleta técnica (`delivery/01-login-e-cadastro-coleta-tech.md`) fica na raiz do workspace como fonte comum às duas partes.

## 1. Escopo do backend (demanda 1)

- Modelo de dados e migrações: `users`, `login_requests`, `sessions`, `terms_acceptances`, `attempts` (seção 11).
- Pedido de acesso: normalização do e-mail, resposta genérica sempre igual (RN-04), geração de token (32 bytes) e código (6 dígitos) guardados como hash, validade 15 min, uso único, 5 tentativas de código, invalidação de pedidos anteriores (seção 6.1, RN-20).
- Envio do e-mail transacional (seção 8) atrás de uma porta, com provedor de teste no desenvolvimento (D-06 em aberto).
- Verificação por link ou código; conta existente cria sessão, conta nova devolve estado "termos pendentes".
- Aceite de termos: cria a conta, marca e-mail confirmado, grava versão e data do aceite, cria sessão (RN-01, RN-19, RN-24). Exigência de novo aceite quando a versão dos termos muda.
- Sessão: cookie `HttpOnly`, `Secure`, `SameSite=Lax`, hash no banco, validade deslizante de 30 dias, limite absoluto de 90 (seção 6.2, RN-22). Rótulo do navegador.
- Logout do dispositivo e de todos os dispositivos (lado servidor).
- Limites contra abuso por e-mail e por IP, com a mesma resposta genérica (seção 6.3).
- Progresso: recebimento idempotente de tentativas por `attempt_id`, retorno do progresso completo da conta, recebimento de tentativa isolada no estudo logado (seções 7.2 a 7.4, RN-21).
- Rotinas de retenção: `login_requests` 30 dias, sessões 90 dias (seção 11).

**Cenários Gherkin cobertos (seção 12):** resposta igual para e-mail com e sem conta; token usado uma vez; limite de envios; login por código (lado servidor); soma de progresso sem duplicar (lado servidor); criação de conta com 12 tentativas migradas (lado servidor); logout (encerramento da sessão).

## 2. Escopo do frontend (demanda 2)

- `device_id` gerado e guardado no `localStorage`; tentativas locais com `attempt_id` (seção 5.1, 7.1).
- Aviso "salve seu progresso" após 10 respostas, sem bloquear (D-09).
- Tela "informe seu e-mail" única para entrar e cadastrar, com a mensagem genérica, reenvio após 60 s e lembrete de spam (seções 5.2 e 9).
- Tela de código de 6 dígitos com contagem de tentativas restantes.
- Página do link com botão "Entrar" que só então consome o token (seção 6.1).
- Tela de termos (versão exibida por configuração) para contas novas; fechar a tela não cria conta.
- Migração e sincronização no cliente: enviar tentativas locais, substituir o `localStorage` pelo progresso devolvido, manter local se o envio falhar, fila de reenvio, aviso quando não há `localStorage` (seções 7.2, 7.4, 7.5).
- Tratamento de sessão expirada no meio do estudo e de nova versão de termos (seção 9).
- Tela de conta com "Sair deste dispositivo" (apaga o `localStorage`) e "Sair de todos os dispositivos" (RN-23).
- Estados de erro: link expirado, já usado ou substituído; código errado.

**Cenários Gherkin cobertos:** os mesmos da seção 12, na perspectiva do usuário na interface. Logout em computador compartilhado é essencialmente do frontend (apagar o progresso local).

## 3. Contrato entre as duas partes

A forma exata (rotas, payloads, códigos de erro) será decidida pelo Turtle da demanda 1 e registrada em `backend/delivery/02-tech-spec.md`. O frontend parte desse documento. Pontos que o contrato precisa cobrir:

| Ponto | Observação |
|---|---|
| Pedir acesso | Sempre a mesma resposta, mesmo ao estourar limite |
| Verificar link ou código | Retorna "sessão criada" ou "termos pendentes" |
| Aceitar termos | Recebe versões aceitas; devolve sessão criada |
| Sessão atual | Usuário, estado e se há termos novos a aceitar |
| Enviar tentativas | Lote idempotente por `attempt_id`; devolve progresso completo |
| Enviar tentativa avulsa | Para o estudo logado |
| Sair | Do dispositivo e de todos |
| Erros | Link inválido/usado/expirado, código errado com tentativas restantes |
| Cookies e CORS | Cookie de sessão entre origens do front e da API |

## 4. Dependências e riscos

- **Pendências da seção 14 da coleta** (advogado, provedor de e-mail, termos provisórios) não bloqueiam o backend, mas o provedor real e a versão dos termos precisam existir antes do frontend ir ao ar.
- **Cookie entre origens:** se front e API ficarem em domínios diferentes, `SameSite=Lax` e CORS com credenciais precisam de decisão no Turtle do backend.
- **Questões (`question_id`):** `attempts` referencia a tabela de questões. Confirmar se ela já existe no repositório; se não, o backend decide entre chave estrangeira ou validação diferida.
- **Repositório do frontend** ainda não está em `repos/`. Clonar antes do `/turtle` da parte frontend.

## 5. Próximos passos

1. Rodar `/tiger login-register (parte backend)` apontando para a coleta e este split. O intake deve herdar só o escopo da seção 1.
2. Concluir o fluxo agêntico do backend até `done` (com graphify manual).
3. Rodar `/tiger login-register (parte frontend)`, desta vez anexando o `02-tech-spec.md` do backend e referências de design em `design/`.
