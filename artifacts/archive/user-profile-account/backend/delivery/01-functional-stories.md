# Perfil, selos e conta - backend

Demanda DEM-20261125-user-profile-account-backend · 2026-11-25.

Parte backend do módulo 02: perfil acadêmico, verificação (e-mail institucional, CRM, títulos, comprovantes), selos, privacidade de exibição, desativação e exclusão da conta, exportação de dados (LGPD) e as operações da fila manual da equipe. Fonte: `delivery/02-perfil-e-conta-coleta-tech.md` (v3, decisões D-11 a D-19) e respostas do intake. Telas, gestão de questões (módulo 03), Overwatch e webservice do CFM ficam fora.

## Business rules

| ID | Rule | Rationale | Source |
|---|---|---|---|
| BR-01 | O perfil é opcional para estudar. Ele só é exigido para criar questões. | Não criar atrito para quem só quer praticar. | demand |
| BR-02 | Perfil completo exige nome completo, situação e universidade; médicos também informam o ano de conclusão. | Define quem pode criar questões. | demand |
| BR-03 | A situação é uma entre estudante, médico, residente e especialista. "Em preparação para residência" é uma marcação opcional que não gera selo. | Duas opções de médico gerariam o mesmo selo. | demand |
| BR-04 | O nome completo tem até 120 caracteres, o breve histórico até 500 caracteres em texto simples, e o Lattes aceita apenas URL de `lattes.cnpq.br`. | Limitar abuso e dados inválidos. | demand |
| BR-05 | A universidade é escolhida da lista de cursos de Medicina do e-MEC ou informada em texto livre como "Instituição estrangeira". | Padronizar a instituição e permitir exceção. | demand |
| BR-06 | O usuário pode ter zero ou mais residências e pós-graduações e mais de um CRM, de UFs diferentes; basta um CRM verificado para o selo. | Refletir trajetórias reais. | demand |
| BR-07 | Todo item verificável tem um status: não enviado, pendente, aprovado, recusado (com motivo) ou revogado (com motivo). | Dar transparência ao usuário e à equipe. | demand |
| BR-08 | Todo selo depende de um item verificado; sem item verificado o usuário fica sem selo. | Selo vale como confiança, não como autodeclaração. | demand |
| BR-09 | Os selos são cumulativos e não dão peso nem ordem às questões. | A ordem das questões é aleatória. | demand |
| BR-10 | O selo principal é o primeiro ativo na ordem Doutor, Mestre, Especialista, Residente, Médico, Estudante; o perfil público mostra todos os ativos. | Escolher o que cabe no cartão da questão. | demand |
| BR-11 | O selo de Estudante exige verificação por e-mail institucional (automática) ou por comprovante de matrícula do semestre atual (fila manual). | Evitar autodeclaração. | demand |
| BR-12 | O e-mail institucional só é aceito se o domínio estiver na lista da universidade escolhida; recebe um código de 6 dígitos com as regras de validade e tentativas do módulo 01; serve só para a verificação e não vira login nem recebe outras mensagens. | Verificar sem criar novo canal de contato. | demand |
| BR-13 | O selo de Estudante vale até o ano de conclusão previsto mais um ano; depois disso o usuário precisa verificar de novo ou passar a médico. | Evitar selo eterno. | demand |
| BR-14 | No piloto o CRM é verificado manualmente: o usuário envia número, UF e a carteira, e a curadoria confere na Busca por Médicos do CFM; só a situação ativa gera o selo de Médico, e inscrição cancelada, suspensa ou cassada é recusada sem expor o motivo publicamente. | O webservice do CFM está fora do piloto (D-12). | demand |
| BR-15 | Um CRM só pode estar verificado em uma conta; a segunda conta entra na fila marcada como conflito e fica sem selo até a análise. | Impedir uso do mesmo CRM por duas pessoas. | demand |
| BR-16 | O nome do perfil precisa bater com o registro do CRM, sem considerar acentos e maiúsculas. | Confirmar que quem se cadastra é o médico. | demand |
| BR-17 | O nome completo fica travado depois da verificação do CRM; mudá-lo exige nova verificação. | Preservar a identidade verificada. | demand |
| BR-18 | O projeto não copia, não raspa e não guarda a base de médicos do CFM; guarda só o que a curadoria conferiu sobre o próprio usuário (situação e especialidades com RQE). | Respeitar a fonte e a minimização de dados. | demand |
| BR-19 | O selo de Especialista exige RQE conferido na mesma consulta do CRM ou título de especialista sem RQE (certificado de residência ou de sociedade), e mostra a especialidade. | Diferenciar a especialidade na exibição. | demand |
| BR-20 | O selo de Residente exige declaração do programa ou da COREME emitida há até 90 dias. | Garantir que a residência está em curso. | demand |
| BR-21 | Os selos de Mestre e Doutor exigem pós-graduação stricto sensu concluída e verificada por diploma ou ata de defesa, e só valem para área da saúde. | Selo só para formação concluída e relevante. | demand |
| BR-22 | Comprovantes aceitam PDF, JPG ou PNG de até 5 MB, ficam em armazenamento privado acessível só à fila manual e são apagados 90 dias depois da decisão, mantendo apenas o registro (tipo, decisão, data, decisor). | Proteger dado pessoal e cumprir a retenção. | demand |
| BR-23 | Toda recusa tem motivo escolhido de uma lista (ilegível, documento vencido, nome diferente, documento não aceito, outro), e o usuário pode reenviar. | Dar caminho de correção. | demand |
| BR-24 | A fila manual é acessível só à equipe, lista pendências por ordem de chegada, mostra o comprovante e os dados do perfil, permite aprovar ou recusar com motivo e registra quem decidiu e quando. | Rastreabilidade das decisões. | demand |
| BR-25 | Se a Busca por Médicos do CFM estiver fora do ar, o pedido permanece pendente até a consulta voltar. | Não decidir sem conferir. | demand |
| BR-26 | O prazo de resposta da fila manual é de 7 dias úteis. | Compromisso do piloto (D-17). | demand |
| BR-27 | Não há reconsulta periódica no piloto; a curadoria reconfere o CRM em caso de denúncia ou por amostragem anual, e se a situação deixou de ser ativa o selo é revogado com motivo e o usuário é avisado. | Manter o selo confiável sem webservice. | demand |
| BR-28 | Fraude confirmada revoga todos os selos do usuário, suspende a conta e envia as questões dele para revisão da curadoria; o selo revogado por fraude some também das cópias guardadas nas questões. | Conter dano à confiança. | demand |
| BR-29 | O modo oculto é o padrão; o modo público exige o aceite do termo de exibição pública, versionado. | Privacidade por padrão. | demand |
| BR-30 | No modo público a questão mostra nome completo, selo principal, situação e universidade e a página pública mostra os dados do perfil e o número de questões publicadas; no modo oculto mostra "Autor verificado" e o selo principal ("Autor da comunidade" se não houver selo) e não há página pública. | Controle do autor sobre a exposição. | demand |
| BR-31 | O número do CRM nunca é exibido publicamente, em nenhum modo. | Dado sensível. | demand |
| BR-32 | O nome do autor é montado na exibição; trocar o modo vale na hora para todas as questões dele, inclusive as antigas. | Evitar gravar o nome na questão. | demand |
| BR-33 | Antes de escolher o modo, o usuário vê uma prévia de como aparece em cada um. | Decisão informada. | demand |
| BR-34 | Para autor de conta excluída, a exibição mostra "Autor da comunidade" e o selo principal guardado na publicação, com a indicação "na data da publicação". | Manter confiança sem identificar ninguém. | demand |
| BR-35 | Desativar a conta é uma pausa reversível: encerra todas as sessões, tira do ar a página pública, faz as questões mostrarem o autor como no modo oculto, mantém questões, progresso, perfil, selos e verificações e interrompe os e-mails transacionais, exceto os ligados à própria conta. | Permitir sumir sem perder dados. | demand |
| BR-36 | Entrar de novo em conta desativada pergunta se o usuário quer reativar, e ao confirmar tudo volta como estava; não há prazo máximo de desativação. | Reversão simples. | demand |
| BR-37 | Excluir a conta exige confirmação digitando o próprio e-mail e coloca a conta em exclusão agendada por 30 dias, com o mesmo efeito da desativação; o usuário recebe e-mail com a data e a forma de cancelar (entrar de novo), e ao fim do prazo a exclusão é executada com e-mail final de confirmação. | Evitar exclusão por engano. | demand |
| BR-38 | Na exclusão são apagados e-mail, nome, perfil, CRM, e-mail institucional, verificações, comprovantes, progresso, sessões e registros de login; ficam as questões publicadas (com autor "Autor da comunidade"), os comentários e contestações (autor anônimo), as avaliações sem ligação com a pessoa e os aceites de termos sem ligação com dados identificáveis. | Equilibrar LGPD e o acervo sob CC BY-SA. | demand |
| BR-39 | Questões em contestação não impedem a exclusão; as contestações continuam abertas para a curadoria. | Não travar o direito do usuário. | demand |
| BR-40 | A exclusão oferece antes a exportação dos dados, a desativação como alternativa e o caminho para as questões do usuário. | Dar alternativas antes de perder dados. | demand |
| BR-41 | A exportação gera um arquivo JSON com conta, perfil, selos, histórico de verificações (sem comprovantes), aceites, progresso completo, questões publicadas, comentários e contestações; o link vai por e-mail, vale 7 dias, exige estar logado, e só é permitido um pedido a cada 24 horas. | Direito de acesso e portabilidade (LGPD). | demand |
| BR-42 | O usuário é notificado (e-mail e/ou site, conforme o evento) de: verificação aprovada ou recusada com motivo, selo revogado com motivo, selo de Estudante a 30 dias de vencer, modo de exibição alterado, conta desativada, exclusão agendada e concluída, exportação pronta e comprovante recebido. | Manter o usuário informado. | demand |
| BR-43 | Se o domínio do e-mail institucional não estiver na lista, o sistema oferece o envio de comprovante e registra um pedido de inclusão do domínio para a equipe. | Não bloquear o estudante. | demand |

## Epics and stories

### EP-01 Perfil acadêmico

O usuário logado informa e mantém seus dados pessoais e acadêmicos.

#### ST-01 Preencher e manter o perfil

- As a usuário logado
- I want informar e editar meus dados pessoais e acadêmicos
- So that eu possa criar questões e ser identificado de forma adequada

**Functional tasks**
- FT-01 Permitir estudar sem perfil preenchido e indicar se o perfil está completo.
- FT-02 Registrar situação, marcação de preparação para residência, universidade e anos de formação.
- FT-03 Registrar vários CRMs, residências e pós-graduações.
- FT-04 Validar limites de nome, breve histórico e Lattes.

**Acceptance criteria**

```gherkin
@AC-01 @BR-01
Scenario: Estudar sem perfil preenchido
  Given um usuário logado sem perfil preenchido
  When ele pratica questões
  Then a prática funciona normalmente
  And ele é informado de que precisa de perfil completo para criar questões

@AC-02 @BR-02
Scenario: Perfil completo de estudante
  Given um usuário com nome completo, situação "estudante" e universidade informados
  When o perfil é consultado
  Then ele consta como completo

@AC-03 @BR-02
Scenario: Perfil de médico sem ano de conclusão
  Given um usuário com situação "médico", nome e universidade, sem ano de conclusão
  When o perfil é consultado
  Then ele consta como incompleto

@AC-04 @BR-03
Scenario: Situação fora das opções
  Given um usuário editando o perfil
  When ele informa a situação "aposentado"
  Then o sistema recusa a alteração

@AC-05 @BR-03
Scenario: Preparação para residência não gera selo
  Given um usuário que marca "em preparação para residência"
  When o perfil é salvo
  Then nenhum selo é concedido por essa marcação

@AC-06 @BR-04
Scenario: Limites dos campos
  Given um usuário editando o perfil
  When ele informa um nome com 121 caracteres ou um breve histórico com 501
  Then o sistema recusa a alteração

@AC-07 @BR-04
Scenario: Lattes de outro domínio
  Given um usuário editando o perfil
  When ele informa o link "https://exemplo.com/cv"
  Then o sistema recusa o link

@AC-08 @BR-05
Scenario: Instituição estrangeira
  Given um usuário que formou-se fora do Brasil
  When ele escolhe "Instituição estrangeira" e informa o nome em texto livre
  Then a universidade é aceita

@AC-09 @BR-06
Scenario: Vários CRMs, um verificado
  Given um usuário com CRM 111/SP e CRM 222/RJ informados
  When apenas o CRM 111/SP é verificado
  Then ele recebe o selo "Médico"
```

### EP-02 Verificação e selos

O usuário comprova seus dados e recebe selos; a equipe decide pela fila manual.

#### ST-02 Verificar matrícula por e-mail institucional

- As a estudante de Medicina
- I want confirmar minha matrícula com um código enviado ao e-mail da universidade
- So that eu receba o selo de Estudante sem esperar a fila manual

**Functional tasks**
- FT-05 Aceitar o e-mail apenas se o domínio pertencer à universidade escolhida.
- FT-06 Enviar o código de 6 dígitos e confirmar a verificação.
- FT-07 Oferecer comprovante e registrar pedido de inclusão quando o domínio não está na lista.

**Acceptance criteria**

```gherkin
@AC-10 @BR-11 @BR-12
Scenario: Selo de Estudante por e-mail institucional
  Given um estudante da universidade "USP" cujo domínio "usp.br" está na lista
  When ele informa "ana@usp.br" e confirma o código recebido
  Then a matrícula fica aprovada
  And ele recebe o selo "Estudante de Medicina"

@AC-11 @BR-12
Scenario: Domínio de outra universidade
  Given um usuário com universidade "USP"
  When ele informa um e-mail de domínio "outra.edu.br"
  Then o sistema recusa o e-mail para essa universidade

@AC-12 @BR-12
Scenario: E-mail institucional não vira login
  Given uma matrícula verificada por "ana@usp.br"
  When ele tenta entrar com "ana@usp.br"
  Then o e-mail não é reconhecido como login
  And nenhuma outra mensagem é enviada a esse endereço

@AC-13 @BR-43
Scenario: Domínio fora da lista
  Given um usuário cuja universidade não tem o domínio do e-mail na lista
  When ele informa o e-mail institucional
  Then o sistema oferece o envio de comprovante
  And registra um pedido de inclusão do domínio para a equipe
```

#### ST-03 Enviar comprovante de matrícula

- As a estudante sem e-mail institucional aceito
- I want enviar o comprovante de matrícula do semestre
- So that a equipe confirme e eu receba o selo

**Functional tasks**
- FT-08 Receber o comprovante e criar o pedido pendente.

**Acceptance criteria**

```gherkin
@AC-14 @BR-11 @BR-07
Scenario: Comprovante de matrícula enviado
  Given um estudante sem verificação por e-mail
  When ele envia o comprovante de matrícula do semestre atual
  Then o pedido fica "pendente" na fila manual
```

#### ST-04 Verificar CRM e especialidade

- As a médico
- I want enviar meu CRM e a carteira para verificação
- So that eu receba os selos de Médico e Especialista

**Functional tasks**
- FT-09 Receber número, UF e carteira e criar o pedido pendente.
- FT-10 Sinalizar conflito quando o CRM já está verificado em outra conta.
- FT-11 Conferir o nome do perfil contra o registro e travar o nome após a aprovação.
- FT-12 Registrar situação e especialidades com RQE vistas na conferência.
- FT-13 Receber título de especialista sem RQE.

**Acceptance criteria**

```gherkin
@AC-15 @BR-14 @BR-17
Scenario: CRM aprovado pela fila manual
  Given um usuário com nome "Ana Souza" no perfil que enviou número, UF e carteira do CRM
  When a curadoria aprova registrando situação "ativa"
  Then ele recebe o selo "Médico"
  And o nome completo fica travado

@AC-16 @BR-14
Scenario: CRM com situação não ativa
  Given um pedido de CRM pendente
  When a curadoria registra situação "cassada" e recusa
  Then nenhum selo é concedido
  And o motivo não aparece no perfil público

@AC-17 @BR-19
Scenario: Especialidade com RQE
  Given que a curadoria aprova um CRM
  And registra a especialidade "Cardiologia" com RQE
  Then o usuário recebe também o selo "Especialista · Cardiologia"

@AC-18 @BR-19
Scenario: Especialista por título sem RQE
  Given um usuário que enviou certificado de residência em "Pediatria"
  When a curadoria aprova o título
  Then ele recebe o selo "Especialista · Pediatria"

@AC-19 @BR-15
Scenario: CRM já verificado em outra conta
  Given que o CRM 12345/SP já está verificado na conta A
  When a conta B envia o mesmo CRM
  Then o pedido entra na fila marcado como conflito
  And a conta B fica sem o selo até a análise

@AC-20 @BR-16
Scenario: Nome diferente do registro
  Given um usuário com nome "Ana Souza" e registro do CRM em nome "Maria Lima"
  When a curadoria analisa o pedido
  Then ela recusa com motivo "nome diferente"

@AC-21 @BR-16
Scenario: Nome igual sem considerar acentos e maiúsculas
  Given um perfil com nome "JOSE AGUIAR" e registro do CRM "José Aguiar"
  When a curadoria confere o nome
  Then o nome é considerado igual

@AC-22 @BR-17
Scenario: Mudar o nome depois do CRM verificado
  Given um usuário com CRM verificado
  When ele tenta alterar o nome completo
  Then a alteração só é aplicada após nova verificação

@AC-23 @BR-18
Scenario: Apenas dados do próprio usuário são guardados
  Given uma conferência concluída
  When os dados da verificação são armazenados
  Then só constam situação, especialidades com RQE e quem conferiu
  And nenhum dado de outros médicos é guardado
```

#### ST-05 Verificar residência e pós-graduação

- As a residente, mestre ou doutor
- I want comprovar minha residência ou titulação
- So that eu receba o selo correspondente

**Functional tasks**
- FT-14 Receber declaração de residência e diploma ou ata de pós-graduação.
- FT-15 Aplicar as regras de validade e de área da saúde.

**Acceptance criteria**

```gherkin
@AC-24 @BR-20
Scenario: Residente com declaração recente
  Given um usuário com residência em curso e declaração emitida há 30 dias
  When a curadoria aprova
  Then ele recebe o selo "Residente"

@AC-25 @BR-20
Scenario: Declaração de residência antiga
  Given uma declaração emitida há 120 dias
  When a curadoria analisa o pedido
  Then ela recusa com motivo "documento vencido"

@AC-26 @BR-21
Scenario: Mestrado concluído na saúde
  Given um mestrado concluído em área da saúde com diploma enviado
  When a curadoria aprova
  Then o usuário recebe o selo "Mestre"

@AC-27 @BR-21
Scenario: Pós-graduação em curso ou fora da saúde
  Given um doutorado em curso, ou um mestrado concluído fora da área da saúde
  When o perfil é avaliado
  Then nenhum selo é concedido por essa pós-graduação
```

#### ST-06 Enviar e acompanhar comprovantes

- As a usuário
- I want enviar documentos com segurança e ver o andamento
- So that eu saiba o que foi aprovado, recusado ou está pendente

**Functional tasks**
- FT-16 Validar formato e tamanho do arquivo.
- FT-17 Mostrar o status de cada item e o motivo das recusas.
- FT-18 Permitir reenvio após recusa.
- FT-19 Apagar comprovantes 90 dias após a decisão, mantendo o registro.

**Acceptance criteria**

```gherkin
@AC-28 @BR-22
Scenario: Arquivo fora das regras
  Given um usuário enviando um comprovante
  When o arquivo é um ".docx" ou tem mais de 5 MB
  Then o sistema recusa o envio

@AC-29 @BR-22
Scenario: Apagar comprovante após 90 dias
  Given uma verificação decidida há 91 dias com comprovante guardado
  When a rotina de retenção é executada
  Then o arquivo é apagado
  And o registro (tipo, decisão, data e decisor) é mantido

@AC-30 @BR-22
Scenario: Comprovante inacessível ao usuário comum
  Given um comprovante armazenado
  When um usuário sem papel de equipe tenta acessá-lo
  Then o acesso é negado

@AC-31 @BR-23 @BR-07
Scenario: Recusa com motivo e reenvio
  Given um pedido recusado com motivo "ilegível"
  When o usuário consulta o item
  Then vê o status "recusado" e o motivo
  And pode reenviar um novo comprovante

@AC-32 @BR-07
Scenario: Item sem envio
  Given um usuário que nunca enviou comprovante de CRM
  When ele consulta o status do CRM
  Then o status é "não enviado"
```

#### ST-07 Analisar a fila manual

- As a membro da equipe
- I want revisar pendências e aprovar ou recusar
- So that selos só existam para itens comprovados

**Functional tasks**
- FT-20 Listar pendências por ordem de chegada, com o tipo do item.
- FT-21 Mostrar comprovante e dados do perfil e o aviso de conflito de CRM.
- FT-22 Aprovar ou recusar com motivo e registrar decisor e data.
- FT-23 Manter pendente enquanto a consulta do CFM estiver indisponível.

**Acceptance criteria**

```gherkin
@AC-33 @BR-24
Scenario: Fila por ordem de chegada
  Given três pedidos pendentes enviados em horários diferentes
  When a equipe lista a fila
  Then o mais antigo aparece primeiro, com o tipo de cada item

@AC-34 @BR-24
Scenario: Decisão registrada
  Given um pedido aberto na fila
  When um membro da equipe aprova ou recusa
  Then ficam registrados quem decidiu e quando

@AC-35 @BR-24
Scenario: Usuário comum não acessa a fila
  Given um usuário sem papel de equipe
  When ele tenta listar a fila
  Then o acesso é negado

@AC-36 @BR-23
Scenario: Recusa sem motivo
  Given um pedido aberto na fila
  When a equipe tenta recusar sem escolher motivo
  Then o sistema não aceita a recusa

@AC-37 @BR-25
Scenario: CFM fora do ar
  Given um pedido de CRM e a consulta do CFM indisponível
  When a equipe não consegue conferir
  Then o pedido permanece "pendente"

@AC-38 @BR-26
Scenario: Pedido além do prazo
  Given um pedido pendente há mais de 7 dias úteis
  When a equipe lista a fila
  Then o pedido é sinalizado como atrasado
```

#### ST-08 Selos e selo principal

- As a autor com verificações aprovadas
- I want ter meus selos exibidos corretamente
- So that leitores confiem nas minhas questões

**Functional tasks**
- FT-24 Conceder selos a partir de verificações aprovadas.
- FT-25 Calcular o selo principal pela ordem definida.
- FT-26 Expirar o selo de Estudante e avisar 30 dias antes.

**Acceptance criteria**

```gherkin
@AC-39 @BR-08
Scenario: Sem verificação, sem selo
  Given um usuário com situação "médico" e CRM informado, sem verificação aprovada
  When seus selos são consultados
  Then não há nenhum selo

@AC-40 @BR-09 @BR-10
Scenario: Selo principal no cartão
  Given um autor com os selos "Especialista · Cardiologia" e "Mestre"
  When o autor de uma questão dele é exibido
  Then o selo principal é "Mestre"
  And a página pública mostra os dois selos

@AC-41 @BR-13
Scenario: Selo de Estudante vencido
  Given um estudante com conclusão prevista em 2026
  When chega 2028
  Then o selo "Estudante" deixa de valer

@AC-42 @BR-13 @BR-42
Scenario: Aviso de vencimento do selo
  Given um selo de Estudante que vence em 30 dias
  When a rotina de avisos é executada
  Then o usuário recebe aviso por e-mail e no site
```

#### ST-09 Revogar selos

- As a curadoria
- I want reconferir e revogar selos indevidos
- So that a confiança nos selos se mantenha

**Functional tasks**
- FT-27 Reconferir CRM por denúncia ou amostragem anual e revogar com motivo.
- FT-28 Tratar fraude confirmada: revogar, suspender e enviar questões para revisão.

**Acceptance criteria**

```gherkin
@AC-43 @BR-27 @BR-42
Scenario: CRM deixa de estar ativo
  Given um usuário com selo "Médico"
  When a curadoria reconfere e registra situação "cancelada"
  Then o selo é revogado com motivo
  And o usuário recebe aviso

@AC-44 @BR-28
Scenario: Fraude confirmada
  Given um comprovante confirmado como falso
  When a curadoria registra a fraude
  Then todos os selos do usuário são revogados
  And a conta fica suspensa
  And as questões dele vão para revisão da curadoria
  And o selo revogado some das cópias guardadas nas questões
```

### EP-03 Privacidade de exibição

#### ST-10 Escolher como aparecer como autor

- As a autor
- I want escolher entre aparecer com meu nome ou de forma oculta
- So that eu controle minha exposição

**Functional tasks**
- FT-29 Mostrar prévia de cada modo.
- FT-30 Trocar o modo, exigindo aceite do termo para o modo público.
- FT-31 Montar a exibição do autor conforme o modo, o selo e o estado da conta.

**Acceptance criteria**

```gherkin
@AC-45 @BR-29
Scenario: Modo padrão oculto
  Given um usuário recém-criado
  When o modo de exibição é consultado
  Then é "oculto"

@AC-46 @BR-29
Scenario: Modo público exige aceite do termo
  Given um usuário em modo oculto
  When ele tenta mudar para público sem aceitar o termo de exibição
  Then a mudança é recusada
  And após aceitar a versão vigente a mudança é aplicada

@AC-47 @BR-30 @BR-31
Scenario: Exibição no modo público
  Given um autor público com selo "Médico", CRM 12345/SP
  When uma questão dele é exibida
  Then aparecem nome completo, selo, situação e universidade
  And o número do CRM não aparece

@AC-48 @BR-30
Scenario: Exibição no modo oculto sem selo
  Given um autor oculto sem selos
  When uma questão dele é exibida
  Then aparece "Autor da comunidade"

@AC-49 @BR-32
Scenario: Troca para o modo oculto
  Given um autor em modo público com 10 questões publicadas
  When ele muda para o modo oculto
  Then as 10 questões passam a mostrar "Autor verificado" e o selo principal
  And a página pública dele sai do ar

@AC-50 @BR-33
Scenario: Prévia antes de escolher
  Given um usuário na tela de privacidade
  When ele pede a prévia
  Then vê como apareceria em cada modo

@AC-51 @BR-31
Scenario: CRM fora da página pública
  Given um autor público com CRM verificado
  When a página pública dele é consultada
  Then o número do CRM não é exibido

@AC-52 @BR-34
Scenario: Autor de conta excluída
  Given uma questão cujo autor excluiu a conta e tinha selo "Residente" na publicação
  When a questão é exibida
  Then aparece "Autor da comunidade"
  And "Residente na data da publicação"
```

### EP-04 Conta e dados pessoais

#### ST-11 Desativar e reativar a conta

- As a usuário
- I want pausar minha conta e voltar depois
- So that eu possa sumir por um tempo sem perder meu progresso

**Functional tasks**
- FT-32 Desativar a conta com todos os efeitos da pausa.
- FT-33 Perguntar sobre reativação ao entrar e restaurar tudo.

**Acceptance criteria**

```gherkin
@AC-53 @BR-35
Scenario: Desativar a conta
  Given um autor logado em dois dispositivos, com página pública e questões publicadas
  When ele desativa a conta
  Then as duas sessões são encerradas
  And a página pública sai do ar
  And as questões mostram o autor como no modo oculto
  And progresso, perfil, selos e verificações continuam guardados

@AC-54 @BR-35
Scenario: E-mails com a conta desativada
  Given uma conta desativada
  When ocorre um evento de e-mail transacional não ligado à conta
  Then nenhum e-mail é enviado

@AC-55 @BR-36
Scenario: Reativar a conta
  Given uma conta desativada há 6 meses
  When o usuário entra pelo login
  Then o sistema pergunta se deseja reativar
  And ao confirmar tudo volta como estava
```

#### ST-12 Excluir a conta

- As a usuário
- I want excluir minha conta e meus dados pessoais
- So that eu exerça meu direito de apagar, mantendo o acervo de questões anônimo

**Functional tasks**
- FT-34 Exigir confirmação pelo próprio e-mail e agendar a exclusão em 30 dias.
- FT-35 Cancelar a exclusão quando o usuário entra de novo.
- FT-36 Executar a exclusão e enviar o e-mail final.
- FT-37 Oferecer exportação e desativação antes de excluir.

**Acceptance criteria**

```gherkin
@AC-56 @BR-37
Scenario: Confirmação por e-mail digitado
  Given um usuário na tela de exclusão
  When ele digita um e-mail diferente do seu
  Then a exclusão não é agendada

@AC-57 @BR-37
Scenario: Exclusão agendada
  Given um usuário que confirmou digitando o próprio e-mail
  When a exclusão é agendada
  Then a conta fica em "exclusão agendada" por 30 dias com os efeitos da desativação
  And ele recebe e-mail com a data e a forma de cancelar

@AC-58 @BR-37
Scenario: Cancelar a exclusão
  Given uma conta em exclusão agendada há 10 dias
  When o usuário entra de novo
  Then a exclusão é cancelada
  And a conta volta ao normal

@AC-59 @BR-38
Scenario: Exclusão com questões publicadas
  Given um autor com 5 questões publicadas e selo "Residente"
  When passam 30 dias da exclusão agendada
  Then e-mail, perfil e progresso são apagados
  And as 5 questões continuam no simulado com "Autor da comunidade"
  And um e-mail final confirma a exclusão

@AC-60 @BR-38
Scenario: O que permanece após a exclusão
  Given uma conta excluída com comentários, avaliações e aceites de termos
  When os dados são consultados
  Then comentários e contestações permanecem com autor anônimo
  And avaliações permanecem sem ligação com a pessoa
  And aceites permanecem sem ligação com dados identificáveis

@AC-61 @BR-39
Scenario: Exclusão com questões em contestação
  Given um autor com uma questão em contestação
  When ele exclui a conta
  Then a exclusão segue
  And a contestação continua aberta para a curadoria

@AC-62 @BR-40
Scenario: Alternativas antes de excluir
  Given um usuário na tela de exclusão
  When a tela é aberta
  Then há opções de exportar os dados, desativar em vez de excluir e ir para "Minhas questões"
```

#### ST-13 Exportar meus dados

- As a usuário
- I want receber uma cópia dos meus dados
- So that eu exerça meu direito de acesso e portabilidade

**Functional tasks**
- FT-38 Gerar o arquivo e enviar o link por e-mail.
- FT-39 Limitar a um pedido por 24 horas.

**Acceptance criteria**

```gherkin
@AC-63 @BR-41
Scenario: Exportação gerada
  Given um usuário logado
  When ele pede a exportação
  Then recebe por e-mail um link válido por 7 dias
  And o arquivo traz conta, perfil, selos, verificações sem comprovantes, aceites, progresso, questões, comentários e contestações

@AC-64 @BR-41
Scenario: Link exige login
  Given um link de exportação válido
  When alguém o abre sem estar logado
  Then o download é negado

@AC-65 @BR-41
Scenario: Segundo pedido em 24 horas
  Given uma exportação pedida há 2 horas
  When o usuário pede outra
  Then o sistema recusa o novo pedido

@AC-66 @BR-41
Scenario: Link expirado
  Given um link de exportação gerado há 8 dias
  When o usuário o abre
  Then o download é negado
```

#### ST-14 Receber notificações da conta

- As a usuário
- I want ser avisado dos eventos da minha conta
- So that eu acompanhe verificações, selos e prazos

**Functional tasks**
- FT-40 Disparar as notificações de e-mail e site conforme o evento.

**Acceptance criteria**

```gherkin
@AC-67 @BR-42
Scenario: Verificação decidida
  Given um pedido de verificação do usuário
  When a equipe aprova ou recusa com motivo
  Then o usuário recebe a decisão por e-mail e no site

@AC-68 @BR-42
Scenario: Comprovante recebido
  Given um usuário que enviou um comprovante
  When o envio é registrado
  Then ele vê a confirmação de recebimento no site

@AC-69 @BR-42
Scenario: Modo de exibição alterado
  Given um usuário que troca o modo de exibição
  When a troca é concluída
  Then ele vê o aviso no site
```

## Use cases

### UC-01 Manter o perfil acadêmico

- **Actor:** Usuário logado
- **Preconditions:** O usuário tem sessão ativa.
- **Postconditions:** O perfil reflete os dados informados e consta como completo ou incompleto.
- **Main flow:**
  1. O usuário informa ou altera dados pessoais e acadêmicos.
  2. O sistema valida os limites e salva.
  3. O sistema indica se o perfil está completo.
- **Alternative flows:**
  - 1a. O usuário informa universidade estrangeira em texto livre.
  - 1b. O usuário adiciona vários CRMs, residências ou pós-graduações.
- **Exceptions:**
  - E1. Situação fora das opções ou campo acima do limite: o sistema recusa a alteração (AC-04, AC-06).
  - E2. Lattes fora de `lattes.cnpq.br`: o sistema recusa o link (AC-07).
  - E3. Nome travado após CRM verificado: a alteração exige nova verificação (AC-22).
- **Related:** BR-01, BR-02, BR-03, BR-04, BR-05, BR-06, BR-17, ST-01

### UC-02 Verificar matrícula de estudante

- **Actor:** Estudante
- **Preconditions:** O perfil tem universidade escolhida.
- **Postconditions:** A matrícula está aprovada (selo concedido) ou pendente na fila.
- **Main flow:**
  1. O estudante informa o e-mail institucional.
  2. O sistema confere o domínio e envia o código de 6 dígitos.
  3. O estudante informa o código.
  4. O sistema aprova a matrícula e concede o selo de Estudante.
- **Alternative flows:**
  - 1a. O domínio não está na lista: o sistema oferece envio de comprovante e registra pedido de inclusão do domínio.
  - 1b. O estudante opta direto pelo comprovante de matrícula; o pedido fica pendente.
- **Exceptions:**
  - E1. Domínio de outra universidade: o sistema recusa o e-mail (AC-11).
- **Related:** BR-07, BR-11, BR-12, BR-13, BR-43, ST-02, ST-03

### UC-03 Verificar CRM e especialidade

- **Actor:** Médico
- **Preconditions:** O perfil tem nome completo.
- **Postconditions:** O CRM está aprovado (selos concedidos), recusado ou em conflito.
- **Main flow:**
  1. O médico informa número, UF e envia a carteira do CRM.
  2. O sistema cria o pedido pendente.
  3. A curadoria confere na Busca por Médicos do CFM número, UF, nome e situação.
  4. A curadoria aprova, registrando situação e especialidades com RQE.
  5. O sistema concede o selo de Médico (e de Especialista, se houver RQE) e trava o nome.
- **Alternative flows:**
  - 1a. O médico envia título de especialista sem RQE.
  - 2a. O CRM já está verificado em outra conta: o pedido entra marcado como conflito.
- **Exceptions:**
  - E1. Situação não ativa ou nome diferente: a curadoria recusa com motivo (AC-16, AC-20).
  - E2. CFM fora do ar: o pedido permanece pendente (AC-37).
- **Related:** BR-14, BR-15, BR-16, BR-17, BR-18, BR-19, BR-25, ST-04

### UC-04 Verificar residência ou pós-graduação

- **Actor:** Residente, mestre ou doutor
- **Preconditions:** O item foi informado no perfil.
- **Postconditions:** O item está aprovado (selo concedido) ou recusado.
- **Main flow:**
  1. O usuário envia declaração do programa ou diploma/ata.
  2. O sistema cria o pedido pendente.
  3. A curadoria confere o documento e aprova.
  4. O sistema concede o selo correspondente.
- **Exceptions:**
  - E1. Declaração com mais de 90 dias: recusa por documento vencido (AC-25).
  - E2. Pós-graduação em curso ou fora da saúde: nenhum selo (AC-27).
- **Related:** BR-20, BR-21, BR-23, ST-05

### UC-05 Enviar comprovante e acompanhar o status

- **Actor:** Usuário logado
- **Preconditions:** Existe um item a comprovar.
- **Postconditions:** O comprovante está guardado de forma privada e o status é visível.
- **Main flow:**
  1. O usuário envia o arquivo.
  2. O sistema valida formato e tamanho e guarda em área privada.
  3. O sistema confirma o recebimento.
  4. O usuário acompanha o status e, se recusado, vê o motivo e reenvia.
- **Exceptions:**
  - E1. Formato ou tamanho inválido: o sistema recusa o envio (AC-28).
  - E2. Comprovante com mais de 90 dias da decisão: é apagado, mantendo o registro (AC-29).
- **Related:** BR-07, BR-22, BR-23, ST-06

### UC-06 Decidir pedidos na fila manual

- **Actor:** Membro da equipe
- **Preconditions:** O membro tem papel de equipe; há pedidos pendentes.
- **Postconditions:** O pedido está aprovado ou recusado, com decisor e data.
- **Main flow:**
  1. O membro lista a fila por ordem de chegada.
  2. O membro abre um pedido e vê comprovante, dados do perfil e aviso de conflito.
  3. O membro aprova ou recusa com motivo.
  4. O sistema registra quem decidiu e quando e notifica o usuário.
- **Exceptions:**
  - E1. Usuário sem papel de equipe: acesso negado (AC-35).
  - E2. Recusa sem motivo: o sistema não aceita (AC-36).
  - E3. Pedido além de 7 dias úteis: sinalizado como atrasado (AC-38).
- **Related:** BR-23, BR-24, BR-25, BR-26, BR-42, ST-07, ST-14

### UC-07 Conceder e exibir selos

- **Actor:** Sistema, em favor do autor
- **Preconditions:** Há verificações aprovadas.
- **Postconditions:** O autor tem os selos ativos e um selo principal.
- **Main flow:**
  1. O sistema concede um selo a cada item aprovado.
  2. O sistema determina o selo principal pela ordem Doutor a Estudante.
  3. O sistema usa o selo principal na exibição da questão e todos na página pública.
- **Alternative flows:**
  - 1a. O selo de Estudante chega ao vencimento: expira, e o usuário é avisado 30 dias antes.
- **Exceptions:**
  - E1. Sem verificação aprovada: nenhum selo (AC-39).
- **Related:** BR-08, BR-09, BR-10, BR-13, ST-08

### UC-08 Revogar selos

- **Actor:** Curadoria
- **Preconditions:** Há denúncia, amostragem anual ou suspeita de fraude.
- **Postconditions:** Selos revogados e usuário avisado, ou conta suspensa em fraude.
- **Main flow:**
  1. A curadoria reconfere o item.
  2. A curadoria registra a situação encontrada.
  3. O sistema revoga o selo com motivo e avisa o usuário.
- **Alternative flows:**
  - 1a. Fraude confirmada: revoga todos os selos, suspende a conta e envia as questões para revisão.
- **Related:** BR-27, BR-28, BR-42, ST-09

### UC-09 Escolher o modo de exibição

- **Actor:** Autor
- **Preconditions:** O usuário está logado.
- **Postconditions:** O modo escolhido vale na hora para todas as questões.
- **Main flow:**
  1. O autor vê a prévia de cada modo.
  2. O autor escolhe o modo.
  3. O sistema aplica e avisa no site.
- **Alternative flows:**
  - 2a. O autor escolhe público: o sistema exige o aceite do termo de exibição vigente.
- **Exceptions:**
  - E1. Aceite ausente: mudança recusada (AC-46).
- **Related:** BR-29, BR-30, BR-31, BR-32, BR-33, BR-34, BR-42, ST-10, ST-14

### UC-10 Desativar e reativar a conta

- **Actor:** Usuário logado
- **Preconditions:** A conta está ativa (desativar) ou desativada (reativar).
- **Postconditions:** A conta está pausada ou restaurada.
- **Main flow:**
  1. O usuário desativa a conta.
  2. O sistema encerra as sessões, tira a página pública do ar e preserva os dados.
  3. Mais tarde, o usuário entra pelo login e confirma a reativação.
  4. O sistema restaura a conta.
- **Alternative flows:**
  - 3a. O usuário não confirma a reativação: a conta segue desativada.
- **Related:** BR-35, BR-36, BR-42, ST-11

### UC-11 Excluir a conta

- **Actor:** Usuário logado
- **Preconditions:** O usuário está logado.
- **Postconditions:** Conta em exclusão agendada, cancelada ou excluída.
- **Main flow:**
  1. O usuário abre a tela de exclusão e vê as alternativas (exportar, desativar, Minhas questões).
  2. O usuário confirma digitando o próprio e-mail.
  3. O sistema agenda a exclusão em 30 dias e envia e-mail com a data.
  4. Ao fim do prazo, o sistema apaga os dados pessoais, anonimiza o autor e envia o e-mail final.
- **Alternative flows:**
  - 3a. O usuário entra de novo antes do prazo: a exclusão é cancelada.
- **Exceptions:**
  - E1. E-mail digitado diferente: a exclusão não é agendada (AC-56).
  - E2. Questões em contestação: a exclusão segue (AC-61).
- **Related:** BR-37, BR-38, BR-39, BR-40, BR-42, ST-12

### UC-12 Exportar meus dados

- **Actor:** Usuário logado
- **Preconditions:** O usuário está logado e não pediu exportação nas últimas 24 horas.
- **Postconditions:** O usuário recebe link válido por 7 dias.
- **Main flow:**
  1. O usuário pede a exportação.
  2. O sistema gera o arquivo JSON.
  3. O sistema envia o link por e-mail.
  4. O usuário, logado, baixa o arquivo.
- **Exceptions:**
  - E1. Segundo pedido em 24 horas: recusado (AC-65).
  - E2. Link expirado ou usuário não logado: download negado (AC-64, AC-66).
- **Related:** BR-41, BR-42, ST-13

## Traceability

| BR | AC | UC | ST |
|---|---|---|---|
| BR-01 | AC-01 | UC-01 | ST-01 |
| BR-02 | AC-02 | UC-01 | ST-01 |
| BR-02 | AC-03 | UC-01 | ST-01 |
| BR-03 | AC-04 | UC-01 | ST-01 |
| BR-03 | AC-05 | UC-01 | ST-01 |
| BR-04 | AC-06 | UC-01 | ST-01 |
| BR-04 | AC-07 | UC-01 | ST-01 |
| BR-05 | AC-08 | UC-01 | ST-01 |
| BR-06 | AC-09 | UC-01 | ST-01 |
| BR-11 | AC-10 | UC-02 | ST-02 |
| BR-12 | AC-10 | UC-02 | ST-02 |
| BR-12 | AC-11 | UC-02 | ST-02 |
| BR-12 | AC-12 | UC-02 | ST-02 |
| BR-43 | AC-13 | UC-02 | ST-02 |
| BR-11 | AC-14 | UC-02 | ST-03 |
| BR-07 | AC-14 | UC-02 | ST-03 |
| BR-14 | AC-15 | UC-03 | ST-04 |
| BR-17 | AC-15 | UC-03 | ST-04 |
| BR-14 | AC-16 | UC-03 | ST-04 |
| BR-19 | AC-17 | UC-03 | ST-04 |
| BR-19 | AC-18 | UC-03 | ST-04 |
| BR-15 | AC-19 | UC-03 | ST-04 |
| BR-16 | AC-20 | UC-03 | ST-04 |
| BR-16 | AC-21 | UC-03 | ST-04 |
| BR-17 | AC-22 | UC-03 | ST-04 |
| BR-18 | AC-23 | UC-03 | ST-04 |
| BR-20 | AC-24 | UC-04 | ST-05 |
| BR-20 | AC-25 | UC-04 | ST-05 |
| BR-21 | AC-26 | UC-04 | ST-05 |
| BR-21 | AC-27 | UC-04 | ST-05 |
| BR-22 | AC-28 | UC-05 | ST-06 |
| BR-22 | AC-29 | UC-05 | ST-06 |
| BR-22 | AC-30 | UC-05 | ST-06 |
| BR-23 | AC-31 | UC-05 | ST-06 |
| BR-07 | AC-31 | UC-05 | ST-06 |
| BR-07 | AC-32 | UC-05 | ST-06 |
| BR-24 | AC-33 | UC-06 | ST-07 |
| BR-24 | AC-34 | UC-06 | ST-07 |
| BR-24 | AC-35 | UC-06 | ST-07 |
| BR-23 | AC-36 | UC-06 | ST-07 |
| BR-25 | AC-37 | UC-06 | ST-07 |
| BR-26 | AC-38 | UC-06 | ST-07 |
| BR-08 | AC-39 | UC-07 | ST-08 |
| BR-09 | AC-40 | UC-07 | ST-08 |
| BR-10 | AC-40 | UC-07 | ST-08 |
| BR-13 | AC-41 | UC-07 | ST-08 |
| BR-13 | AC-42 | UC-07 | ST-08 |
| BR-42 | AC-42 | - | ST-08 |
| BR-27 | AC-43 | UC-08 | ST-09 |
| BR-42 | AC-43 | UC-08 | ST-09 |
| BR-28 | AC-44 | UC-08 | ST-09 |
| BR-29 | AC-45 | UC-09 | ST-10 |
| BR-29 | AC-46 | UC-09 | ST-10 |
| BR-30 | AC-47 | UC-09 | ST-10 |
| BR-31 | AC-47 | UC-09 | ST-10 |
| BR-30 | AC-48 | UC-09 | ST-10 |
| BR-32 | AC-49 | UC-09 | ST-10 |
| BR-33 | AC-50 | UC-09 | ST-10 |
| BR-31 | AC-51 | UC-09 | ST-10 |
| BR-34 | AC-52 | UC-09 | ST-10 |
| BR-35 | AC-53 | UC-10 | ST-11 |
| BR-35 | AC-54 | UC-10 | ST-11 |
| BR-36 | AC-55 | UC-10 | ST-11 |
| BR-37 | AC-56 | UC-11 | ST-12 |
| BR-37 | AC-57 | UC-11 | ST-12 |
| BR-37 | AC-58 | UC-11 | ST-12 |
| BR-38 | AC-59 | UC-11 | ST-12 |
| BR-38 | AC-60 | UC-11 | ST-12 |
| BR-39 | AC-61 | UC-11 | ST-12 |
| BR-40 | AC-62 | UC-11 | ST-12 |
| BR-41 | AC-63 | UC-12 | ST-13 |
| BR-41 | AC-64 | UC-12 | ST-13 |
| BR-41 | AC-65 | UC-12 | ST-13 |
| BR-41 | AC-66 | UC-12 | ST-13 |
| BR-42 | AC-67 | UC-06, UC-09 | ST-14 |
| BR-42 | AC-68 | UC-06, UC-09 | ST-14 |
| BR-42 | AC-69 | UC-06, UC-09 | ST-14 |

## Open questions

| ID | Question | Related | Status |
|---|---|---|---|
| OQ-01 | O termo de exibição pública, o uso da CC BY-SA com pseudônimo, o prazo de guarda dos aceites e a retenção de comprovantes dependem de validação jurídica. O backend segue com texto provisório versionado? | BR-29, BR-22, BR-38 | answered. Resposta: seguir com texto provisório versionado. |
| OQ-02 | As listas de referência (cursos de Medicina do e-MEC, domínios por universidade, especialidades reconhecidas) ainda não existem. O backend entrega as tabelas e uma carga inicial de exemplo; a carga real é pendência de dados. | BR-05, BR-12, BR-19 | answered. Resposta: padrão (tabelas e carga inicial de exemplo). |
| OQ-03 | A tabela `questions` e o campo `author_badge_snapshot` pertencem ao módulo 03. Este backend entrega o cálculo do selo principal e a montagem da exibição do autor como consulta, sem alterar `questions`. Confirmar se a tabela já existe no repositório. | BR-10, BR-32, BR-34 | answered. Resposta: a tabela `questions` ainda não existe nas migrations; o backend não a cria e entrega só o cálculo do selo principal e a montagem da exibição do autor. |
| OQ-04 | A equipe se autentica por um papel `staff` na conta do login existente (default aceito). Falta definir como o papel é atribuído no piloto. | BR-24 | answered. Resposta: haverá uma conta única de equipe, criada por script de shell. |
| OQ-05 | O armazenamento privado de comprovantes entra como porta com implementação em disco local no desenvolvimento; o provedor real fica para depois (default aceito). | BR-22 | answered. Resposta: padrão (porta de armazenamento, disco local no desenvolvimento). |
| OQ-06 | Denúncia de breve histórico ofensivo e remoção pela curadoria (seção 12 da coleta) não tem regra própria nem cenário. Está fora deste escopo? | BR-04 | answered. Resposta: fora de escopo. |
| OQ-07 | "Questão em contestação", "comentários" e "avaliações" são do módulo 03; a exclusão aqui deve apenas preservá-los e anonimizar o autor, sem criar essas estruturas. Confirmar. | BR-38, BR-39 | answered. Resposta: padrão (apenas preservar e anonimizar). |
| OQ-08 | O prazo de 7 dias úteis (BR-26) é só um sinal de atraso na fila, sem consequência automática para o usuário. | BR-26 | answered. Resposta: padrão (apenas sinal de atraso). |
