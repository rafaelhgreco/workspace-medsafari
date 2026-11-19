# Cadastro, login e sessão - backend

Demanda DEM-20261118-login-register-backend · 2026-11-18.

Primeira parte da história `login-register` (módulo 01). Cobre apenas o backend: pedido de acesso por e-mail, confirmação por link ou código de 6 dígitos, criação da conta com aceite de termos, sessão em cookie, logout e recebimento do progresso de estudo. Telas, `localStorage`, fila de reenvio e aviso "salve seu progresso" pertencem à parte frontend. Retenção de dados antigos, provedor real de e-mail e validação da existência da questão ficam fora desta demanda. Fontes: `login-register/delivery/01-login-e-cadastro-coleta-tech.md` e `login-register/00-split.md`.

## Business rules

| ID | Rule | Rationale | Source |
|---|---|---|---|
| BR-01 | A conta só passa a existir quando o e-mail é confirmado e os termos são aceitos. | Garante que o e-mail é de quem pediu e que há aceite registrado. | demand |
| BR-02 | O e-mail de acesso traz apenas um link, um código de 6 dígitos e a validade, sem conteúdo promocional, sem dados do usuário e sem identificador de sessão. | Um identificador de sessão na caixa de entrada seria uma senha permanente. | demand |
| BR-03 | O acesso é feito por link ou por código de 6 dígitos enviados ao e-mail, no mesmo fluxo para entrar e para se cadastrar. | Simplifica o fluxo e atende quem lê o e-mail em outro aparelho. | demand |
| BR-04 | A resposta ao pedido de acesso é sempre a mesma, exista ou não conta para o e-mail e mesmo quando um limite foi excedido. | Não revelar quais e-mails têm conta. | demand |
| BR-05 | Um e-mail corresponde a uma única conta. O e-mail é normalizado (sem espaços nas pontas, em minúsculas, mantendo pontos e `+`), tem formato válido e no máximo 254 caracteres. | Evita contas duplicadas e entradas inválidas. | demand |
| BR-06 | Link e código valem 15 minutos, são de uso único e só podem ser guardados em forma de hash. Usar um invalida o outro. | Reduz o risco de reaproveitamento ou vazamento. | demand |
| BR-07 | Cada pedido admite até 5 códigos errados. Na 5ª tentativa errada o pedido é invalidado, e cada erro informa quantas tentativas restam. | Impede adivinhação do código. | demand |
| BR-08 | Um novo pedido de acesso invalida os pedidos anteriores ainda abertos do mesmo e-mail. | Só o acesso mais recente vale. | demand |
| BR-09 | Os limites de abuso são: 3 envios a cada 15 minutos e 10 por dia por e-mail, 20 envios por hora por IP e 30 tentativas de código por hora por IP. Os valores são ajustáveis com dados do piloto. | Proteger contra spam e força bruta. | demand |
| BR-10 | A sessão é transportada em cookie `HttpOnly`, `Secure` e `SameSite=Lax`, com identificador aleatório guardado só em forma de hash, e nunca é exposta de outra forma. | Scripts da página não conseguem ler a sessão. | demand |
| BR-11 | A sessão vale 30 dias, renovados a cada uso, com limite absoluto de 90 dias desde a criação. Passado o limite, é preciso um novo acesso por e-mail. | Equilibra conveniência e segurança. | demand |
| BR-12 | Sair do dispositivo encerra a sessão atual. Sair de todos os dispositivos encerra todas as sessões da conta. | Controle do usuário sobre onde está logado. | demand |
| BR-13 | O aceite dos Termos de Uso e da Ciência da Política de Privacidade guarda a versão, a data e hora e o IP. A versão aceita precisa ser a versão vigente, definida por configuração. | Prova do aceite (LGPD). | demand, human answer |
| BR-14 | Quando a versão vigente dos termos muda, o usuário precisa aceitar a nova versão para continuar usando a conta; até lá, os recursos da conta ficam bloqueados. | Garantir consentimento sobre a versão em vigor. | demand |
| BR-15 | O cadastro pede somente o e-mail e os aceites. O nome de exibição é opcional e não há restrição de idade. | Reduz dados pessoais e atrito. | demand |
| BR-16 | Ao entrar, as tentativas anônimas enviadas são somadas às da conta sem perda e sem duplicação. Uma tentativa cujo identificador já foi gravado é ignorada. | Perder o estudo já feito é o pior motivo para não se cadastrar. | demand |
| BR-17 | Depois do cadastro o banco é a fonte de verdade do progresso, e a resposta de entrada devolve o progresso completo da conta. | O navegador mantém só uma cópia. | demand |
| BR-18 | O usuário logado pode enviar tentativas avulsas, que ficam ligadas à conta. Reenviar a mesma tentativa não a duplica. | Permite reenviar após falha de rede sem duplicar. | demand |
| BR-19 | Nesta etapa a tentativa guarda o identificador da questão sem verificar se a questão existe. | A tabela de questões ainda não existe; o módulo 03 acrescenta a validação. | human answer |
| BR-20 | Abrir ou visualizar o link de acesso não consome o token. Ele só é consumido quando o usuário confirma explicitamente a entrada. | Leitores de e-mail que abrem links sozinhos não podem gastar o token. | demand |
| BR-21 | Para um e-mail sem conta, confirmar o acesso não cria a conta. A conta é criada apenas quando os termos são aceitos em seguida. Sem o aceite, nada é criado e é preciso pedir novo acesso. | O aceite não pode aparecer antes do envio, para não revelar quem tem conta. | demand |
| BR-22 | Depois da confirmação, o aceite dos termos de uma conta nova precisa acontecer em até 15 minutos; passado esse prazo, é preciso pedir novo acesso. | Evita confirmação pendente indefinida. | human answer |
| BR-23 | Cada sessão registra data de criação, último uso e um rótulo do navegador (ex.: "Chrome no Windows"). Não há consulta à lista de dispositivos nesta etapa; ela fica para uma demanda futura. | O rótulo prepara uma futura lista de dispositivos sem ampliar o escopo agora. | human answer |
| BR-24 | Um e-mail com formato inválido ou acima de 254 caracteres é recusado com o erro de título "Invalid Email Format" e status 422, sem enviar nada e sem revelar se há conta. | Dar retorno claro sem expor contas. | human answer |

## Epics and stories

### EP-01 Acesso por e-mail

O visitante informa o e-mail, recebe link e código, confirma o acesso e, se for novo, aceita os termos para criar a conta.

#### ST-01 Pedir acesso por e-mail

- As a visitante
- I want informar meu e-mail e receber um link e um código de acesso
- So that eu entre ou crie minha conta sem senha

**Functional tasks**
- FT-01 Receber o e-mail, normalizá-lo e validá-lo.
- FT-02 Enviar um único e-mail com link, código e validade.
- FT-03 Responder sempre com a mesma mensagem, exista a conta ou não.
- FT-04 Invalidar pedidos anteriores abertos do mesmo e-mail.
- FT-05 Aplicar os limites de envio por e-mail e por IP.

**Acceptance criteria**

```gherkin
@AC-01 @BR-02 @BR-03
Scenario: Pedido de acesso envia link e código
  Given um e-mail válido
  When o visitante pede acesso
  Then o sistema envia um e-mail com um link, um código de 6 dígitos e a validade de 15 minutos
  And o e-mail não contém identificador de sessão nem conteúdo promocional

@AC-02 @BR-04
Scenario: Resposta idêntica com e sem conta
  Given um e-mail que já tem conta e outro que não tem
  When o acesso é pedido para cada um
  Then as duas respostas são idênticas

@AC-03 @BR-05
Scenario: E-mail normalizado leva à mesma conta
  Given uma conta cadastrada com "ana@exemplo.com"
  When o acesso é pedido para "  Ana@Exemplo.com  "
  Then o pedido é tratado como sendo da mesma conta

@AC-04 @BR-24
Scenario: E-mail inválido é recusado
  Given um texto que não é um e-mail válido ou que passa de 254 caracteres
  When o visitante pede acesso
  Then o sistema recusa com o erro "Invalid Email Format" e status 422
  And nenhum e-mail é enviado

@AC-05 @BR-08
Scenario: Novo pedido invalida o anterior
  Given um pedido de acesso aberto para um e-mail
  When um novo pedido é feito para o mesmo e-mail
  Then o link e o código do pedido anterior deixam de funcionar

@AC-06 @BR-09 @BR-04
Scenario: Limite de envios por e-mail
  Given que o e-mail recebeu 3 acessos nos últimos 15 minutos
  When um 4º acesso é pedido
  Then a resposta é a mesma mensagem de sempre
  And nenhum e-mail é enviado

@AC-07 @BR-09 @BR-04
Scenario: Limite de envios por IP
  Given que um IP fez 20 pedidos de acesso na última hora
  When esse IP faz mais um pedido
  Then a resposta é a mesma mensagem de sempre
  And nenhum e-mail é enviado
```

#### ST-02 Confirmar o acesso por link ou código

- As a visitante com um pedido de acesso aberto
- I want confirmar o acesso pelo link ou digitando o código
- So that eu entre na minha conta, inclusive abrindo o e-mail em outro aparelho

**Functional tasks**
- FT-06 Confirmar o acesso por link ou por código de 6 dígitos.
- FT-07 Tornar link e código de uso único, com validade de 15 minutos.
- FT-08 Contar erros de código e informar as tentativas restantes.
- FT-09 Não consumir o link ao ser apenas visualizado.
- FT-10 Limitar tentativas de código por IP.

**Acceptance criteria**

```gherkin
@AC-08 @BR-03 @BR-06
Scenario: Entrar com o link em conta existente
  Given um pedido de acesso aberto para um e-mail com conta
  When o usuário confirma a entrada pelo link
  Then uma sessão é criada

@AC-09 @BR-03 @BR-06
Scenario: Entrar com o código em outro aparelho
  Given um pedido de acesso aberto para um e-mail com conta
  When o código de 6 dígitos correto é informado, mesmo por quem abriu o e-mail em outro aparelho
  Then uma sessão é criada para quem informou o código

@AC-10 @BR-06
Scenario: Token de uso único
  Given que o usuário entrou com o link
  When o mesmo link ou o código do mesmo pedido é usado de novo
  Then o sistema informa que o acesso já foi usado
  And não cria sessão

@AC-11 @BR-06
Scenario: Acesso expirado
  Given um pedido de acesso criado há mais de 15 minutos
  When o link ou o código é usado
  Then o sistema informa que o acesso expirou
  And não cria sessão

@AC-12 @BR-07
Scenario: Código errado e invalidação na quinta tentativa
  Given um pedido de acesso aberto
  When 5 códigos errados são informados em sequência
  Then cada erro informa quantas tentativas restam
  And na 5ª tentativa o pedido é invalidado, inclusive para o código correto e para o link

@AC-13 @BR-20
Scenario: Visualizar o link não consome o token
  Given um pedido de acesso aberto
  When o link é apenas aberto para visualização, sem confirmar a entrada
  Then o link e o código continuam válidos

@AC-14 @BR-09
Scenario: Limite de tentativas de código por IP
  Given que um IP fez 30 tentativas de código na última hora
  When esse IP tenta mais um código
  Then a tentativa é recusada sem conferir o código
```

#### ST-03 Criar a conta aceitando os termos

- As a visitante sem conta que confirmou o acesso
- I want aceitar os termos para concluir meu cadastro
- So that minha conta seja criada com o e-mail confirmado

**Functional tasks**
- FT-11 Sinalizar que o e-mail confirmado ainda não tem conta e que os termos estão pendentes.
- FT-12 Aceitar os termos e a política vigentes, criando a conta e a sessão.
- FT-13 Registrar versão, data e hora e IP de cada aceite.
- FT-14 Não criar conta quando o aceite não acontece.
- FT-15 Aceitar nome de exibição opcional.

**Acceptance criteria**

```gherkin
@AC-15 @BR-01 @BR-21 @BR-13
Scenario: Conta criada após confirmar e aceitar os termos
  Given um e-mail sem conta com o acesso confirmado
  When o visitante aceita os Termos de Uso e a Política de Privacidade vigentes
  Then a conta é criada com o e-mail confirmado
  And o aceite de cada documento guarda versão, data e hora e IP
  And uma sessão é criada

@AC-16 @BR-21
Scenario: Sem aceite não há conta
  Given um e-mail sem conta com o acesso confirmado
  When o visitante não aceita os termos
  Then nenhuma conta é criada
  And um novo acesso precisa ser pedido

@AC-17 @BR-13
Scenario: Versão dos termos diferente da vigente é recusada
  Given que a versão vigente dos termos é "2"
  When o aceite é enviado com a versão "1"
  Then o sistema recusa o aceite
  And a conta não é criada

@AC-18 @BR-22
Scenario: Aceite fora do prazo
  Given um e-mail sem conta com o acesso confirmado há mais de 15 minutos
  When o visitante tenta aceitar os termos
  Then o sistema recusa
  And um novo acesso precisa ser pedido

@AC-19 @BR-15
Scenario: Cadastro só com e-mail e aceites
  Given um e-mail sem conta com o acesso confirmado
  When o visitante aceita os termos sem informar nome de exibição
  Then a conta é criada sem nome de exibição
  And nenhum outro dado é exigido
```

### EP-02 Sessão e termos

Depois de entrar, o usuário mantém a sessão, pode encerrá-la e precisa aceitar versões novas dos termos.

#### ST-04 Manter a sessão

- As a usuário cadastrado
- I want continuar logado sem repetir o acesso por e-mail a cada visita
- So that eu estude sem interrupções

**Functional tasks**
- FT-16 Entregar a sessão por cookie protegido.
- FT-17 Renovar a validade a cada uso, respeitando o limite absoluto.
- FT-18 Registrar criação, último uso e rótulo do navegador.

**Acceptance criteria**

```gherkin
@AC-20 @BR-10
Scenario: Sessão entregue em cookie protegido
  Given um acesso confirmado
  When a sessão é criada
  Then ela é entregue em cookie HttpOnly, Secure e SameSite=Lax
  And o identificador da sessão não aparece no corpo da resposta

@AC-21 @BR-11
Scenario: Uso renova a validade
  Given uma sessão com 10 dias de uso
  When o usuário faz uma requisição autenticada
  Then a validade passa a contar 30 dias a partir daquele uso

@AC-22 @BR-11
Scenario: Sessão expira no limite absoluto
  Given uma sessão criada há 91 dias, usada com frequência
  When o usuário faz uma requisição autenticada
  Then o sistema recusa por sessão expirada
  And um novo acesso por e-mail é necessário

@AC-23 @BR-23
Scenario: Sessão registra dados de uso
  Given um acesso confirmado por um navegador identificável
  When a sessão é criada
  Then ela guarda a data de criação, o último uso e o rótulo do navegador
```

#### ST-05 Sair do dispositivo ou de todos

- As a usuário cadastrado
- I want encerrar minha sessão neste dispositivo ou em todos
- So that ninguém continue usando minha conta depois que eu sair

**Functional tasks**
- FT-19 Encerrar a sessão atual.
- FT-20 Encerrar todas as sessões da conta.

**Acceptance criteria**

```gherkin
@AC-24 @BR-12
Scenario: Sair deste dispositivo
  Given um usuário com sessões em dois dispositivos
  When ele escolhe sair deste dispositivo
  Then a sessão atual é encerrada
  And a sessão do outro dispositivo continua válida

@AC-25 @BR-12
Scenario: Sair de todos os dispositivos
  Given um usuário com sessões em dois dispositivos
  When ele escolhe sair de todos os dispositivos
  Then todas as sessões da conta são encerradas
```

#### ST-06 Aceitar nova versão dos termos

- As a usuário cadastrado
- I want ser avisado quando os termos mudam e aceitar a nova versão
- So that meu consentimento continue valendo para a versão em uso

**Functional tasks**
- FT-21 Indicar que há uma versão nova de termos ou política pendente de aceite.
- FT-22 Bloquear os recursos da conta enquanto o aceite estiver pendente.
- FT-23 Registrar o aceite da nova versão.

**Acceptance criteria**

```gherkin
@AC-26 @BR-14
Scenario: Versão nova bloqueia recursos até o aceite
  Given um usuário logado que aceitou a versão "1" dos termos
  And a versão vigente passou a ser "2"
  When ele tenta usar um recurso da conta
  Then o sistema informa que há termos pendentes de aceite
  And o recurso não é executado

@AC-27 @BR-14 @BR-13
Scenario: Aceitar a nova versão libera o uso
  Given um usuário com termos novos pendentes
  When ele aceita a versão vigente
  Then o aceite guarda versão, data e hora e IP
  And os recursos da conta voltam a funcionar
```

### EP-03 Progresso de estudo

O progresso feito sem login é enviado no acesso e somado ao da conta; depois, cada tentativa é gravada na conta.

#### ST-07 Somar o progresso ao entrar

- As a usuário que estudou antes de entrar
- I want que minhas respostas anteriores sejam somadas às da conta
- So that eu não perca o que já estudei

**Functional tasks**
- FT-24 Receber a lista de tentativas anônimas ao entrar.
- FT-25 Ignorar tentativas cujo identificador já foi gravado.
- FT-26 Devolver o progresso completo da conta.

**Acceptance criteria**

```gherkin
@AC-28 @BR-16 @BR-17
Scenario: Soma sem perda
  Given uma conta com 30 tentativas
  And um navegador novo com 5 tentativas anônimas
  When o usuário entra nesse navegador e envia as 5 tentativas
  Then a conta passa a ter 35 tentativas
  And a resposta devolve as 35 tentativas

@AC-29 @BR-16
Scenario: Reenviar as mesmas tentativas não duplica
  Given uma conta com 35 tentativas, 5 delas vindas do navegador
  When as mesmas 5 tentativas são enviadas de novo
  Then a conta continua com 35 tentativas

@AC-30 @BR-17
Scenario: Entrar em outro navegador devolve o progresso da conta
  Given uma conta com 30 tentativas
  When o usuário entra em um navegador sem tentativas locais
  Then a resposta devolve as 30 tentativas da conta
```

#### ST-08 Registrar tentativas depois de logado

- As a usuário logado
- I want que cada resposta minha seja gravada na conta
- So that o banco seja a fonte de verdade do meu progresso

**Functional tasks**
- FT-27 Receber uma tentativa avulsa do usuário logado.
- FT-28 Ignorar reenvios de tentativa já gravada.
- FT-29 Aceitar o identificador da questão sem verificar sua existência.

**Acceptance criteria**

```gherkin
@AC-31 @BR-18
Scenario: Tentativa avulsa fica na conta
  Given um usuário logado
  When ele envia uma tentativa
  Then a tentativa passa a fazer parte do progresso da conta

@AC-32 @BR-18
Scenario: Reenvio da mesma tentativa não duplica
  Given uma tentativa já gravada na conta
  When a mesma tentativa é enviada de novo após falha de rede
  Then o progresso da conta não muda

@AC-33 @BR-19
Scenario: Identificador de questão não é verificado nesta etapa
  Given um usuário logado
  When ele envia uma tentativa com um identificador de questão ainda desconhecido
  Then a tentativa é gravada normalmente
```

## Use cases

### UC-01 Entrar ou criar conta por e-mail

- **Actor:** Visitante
- **Preconditions:** O visitante tem acesso a um e-mail. Pode ou não ter conta.
- **Postconditions:** O visitante tem uma sessão e, se for novo, uma conta com e-mail confirmado e aceites registrados.
- **Main flow:**
  1. O visitante informa o e-mail.
  2. O sistema normaliza o e-mail, responde com a mensagem padrão e envia o e-mail com link e código.
  3. O visitante confirma o acesso pelo link ou pelo código.
  4. O sistema confere o acesso e cria a sessão.
- **Alternative flows:**
  - 4a. O e-mail não tem conta: o sistema pede o aceite dos termos vigentes; ao aceitar, cria a conta, registra os aceites e cria a sessão.
  - 3a. O visitante abre o e-mail em outro aparelho e digita o código no aparelho de origem.
  - 2a. Existe pedido aberto para o mesmo e-mail: o sistema o invalida ao criar o novo.
- **Exceptions:**
  - E1. E-mail inválido: o sistema recusa com o erro "Invalid Email Format" (422).
  - E2. Limite de envios excedido: a resposta é a padrão e nada é enviado.
  - E3. Link ou código usado, expirado ou invalidado: o sistema informa e não cria sessão.
  - E4. Código errado: o sistema informa as tentativas restantes e invalida o pedido na 5ª.
  - E5. Limite de tentativas de código por IP excedido: a tentativa é recusada.
  - E6. O visitante não aceita os termos ou o prazo de aceite vence: nenhuma conta é criada.
  - E7. Versão de termos diferente da vigente: o aceite é recusado.
- **Related:** BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-07, BR-08, BR-09, BR-13, BR-15, BR-20, BR-21, BR-22, BR-24, ST-01, ST-02, ST-03

### UC-02 Manter e encerrar a sessão

- **Actor:** Usuário cadastrado
- **Preconditions:** O usuário tem uma sessão ativa.
- **Postconditions:** A sessão segue válida, ou foi encerrada, e os termos vigentes estão aceitos.
- **Main flow:**
  1. O usuário usa recursos da conta.
  2. O sistema valida a sessão e renova a validade.
  3. O usuário escolhe sair deste dispositivo.
  4. O sistema encerra a sessão atual.
- **Alternative flows:**
  - 3a. O usuário escolhe sair de todos os dispositivos: o sistema encerra todas as sessões da conta.
  - 1a. A versão dos termos mudou: o sistema pede o aceite da versão vigente; ao aceitar, os recursos voltam a funcionar.
- **Exceptions:**
  - E1. Sessão expirada ou além de 90 dias: o sistema recusa e exige novo acesso.
  - E2. Termos novos pendentes: os recursos da conta ficam bloqueados até o aceite.
- **Related:** BR-10, BR-11, BR-12, BR-13, BR-14, BR-23, ST-04, ST-05, ST-06

### UC-03 Sincronizar o progresso de estudo

- **Actor:** Usuário cadastrado
- **Preconditions:** O usuário tem sessão ativa e possui tentativas feitas antes ou durante o estudo logado.
- **Postconditions:** As tentativas estão gravadas na conta, sem duplicação, e o usuário recebe o progresso completo.
- **Main flow:**
  1. O usuário entra e envia as tentativas anônimas do navegador.
  2. O sistema grava as tentativas novas ligadas à conta.
  3. O sistema devolve o progresso completo da conta.
  4. Depois, a cada resposta, o usuário envia a tentativa.
  5. O sistema a grava na conta.
- **Alternative flows:**
  - 2a. Algumas tentativas já existem: o sistema as ignora e grava só as novas.
  - 1a. O navegador não tem tentativas: o sistema só devolve o progresso da conta.
- **Exceptions:**
  - E1. Sessão expirada: o envio é recusado e as tentativas não são gravadas.
  - E2. Identificador de questão desconhecido: a tentativa é gravada mesmo assim.
- **Related:** BR-16, BR-17, BR-18, BR-19, ST-07, ST-08

## Traceability

| BR | AC | UC | ST |
|---|---|---|---|
| BR-02 | AC-01 | UC-01 | ST-01 |
| BR-03 | AC-01 | UC-01 | ST-01 |
| BR-04 | AC-02 | UC-01 | ST-01 |
| BR-05 | AC-03 | UC-01 | ST-01 |
| BR-24 | AC-04 | UC-01 | ST-01 |
| BR-08 | AC-05 | UC-01 | ST-01 |
| BR-09 | AC-06 | UC-01 | ST-01 |
| BR-04 | AC-06 | UC-01 | ST-01 |
| BR-09 | AC-07 | UC-01 | ST-01 |
| BR-04 | AC-07 | UC-01 | ST-01 |
| BR-03 | AC-08 | UC-01 | ST-02 |
| BR-06 | AC-08 | UC-01 | ST-02 |
| BR-03 | AC-09 | UC-01 | ST-02 |
| BR-06 | AC-09 | UC-01 | ST-02 |
| BR-06 | AC-10 | UC-01 | ST-02 |
| BR-06 | AC-11 | UC-01 | ST-02 |
| BR-07 | AC-12 | UC-01 | ST-02 |
| BR-20 | AC-13 | UC-01 | ST-02 |
| BR-09 | AC-14 | UC-01 | ST-02 |
| BR-01 | AC-15 | UC-01 | ST-03 |
| BR-21 | AC-15 | UC-01 | ST-03 |
| BR-13 | AC-15 | UC-01 | ST-03 |
| BR-21 | AC-16 | UC-01 | ST-03 |
| BR-13 | AC-17 | UC-01 | ST-03 |
| BR-22 | AC-18 | UC-01 | ST-03 |
| BR-15 | AC-19 | UC-01 | ST-03 |
| BR-10 | AC-20 | UC-02 | ST-04 |
| BR-11 | AC-21 | UC-02 | ST-04 |
| BR-11 | AC-22 | UC-02 | ST-04 |
| BR-23 | AC-23 | UC-02 | ST-04 |
| BR-12 | AC-24 | UC-02 | ST-05 |
| BR-12 | AC-25 | UC-02 | ST-05 |
| BR-14 | AC-26 | UC-02 | ST-06 |
| BR-14 | AC-27 | UC-02 | ST-06 |
| BR-13 | AC-27 | UC-02 | ST-06 |
| BR-16 | AC-28 | UC-03 | ST-07 |
| BR-17 | AC-28 | UC-03 | ST-07 |
| BR-16 | AC-29 | UC-03 | ST-07 |
| BR-17 | AC-30 | UC-03 | ST-07 |
| BR-18 | AC-31 | UC-03 | ST-08 |
| BR-18 | AC-32 | UC-03 | ST-08 |
| BR-19 | AC-33 | UC-03 | ST-08 |

## Open questions

| ID | Question | Related | Status |
|---|---|---|---|
| OQ-01 | O prazo de 15 minutos para aceitar os termos depois da confirmação é adequado? Resposta: sim. | BR-22 | answered |
| OQ-02 | A lista de dispositivos vira demanda futura? Resposta: sim, demanda futura. | BR-23 | answered |
| OQ-03 | Qual o erro para e-mail inválido? Resposta: título "Invalid Email Format", status 422. | BR-24 | answered |
| OQ-04 | Quando entra a rotina de retenção (`login_requests` por 30 dias, sessões por 90 dias)? Resposta: fica registrada para uma demanda futura. | BR-06, BR-11 | answered |
| OQ-05 | Base legal da LGPD (D-05), ECA Digital e textos dos termos. Resposta: os termos de uso entram em demanda futura; aqui a versão vigente vem de configuração. | BR-13, BR-15 | answered |
| OQ-06 | O provedor real de e-mail (D-06) entra quando? Resposta: em demanda futura; esta entrega só o adaptador de desenvolvimento. | BR-02 | answered |
