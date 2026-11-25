# Módulo 02: perfil, selos e conta

2026-11-15 · rafael · v3: decisões D-11 a D-19 fechadas

Documentos-fonte: `produto-banco-questoes-residencia.md`, `workflow-jornada-novo-usuario.md` e `01-login-e-cadastro.md`.

## 1. Objetivo e limites

Este módulo define a área do usuário logado: o que ele informa no perfil, como esses dados são verificados, o que aparece publicamente, quais selos ele recebe e como desativa ou exclui a conta.

**Dentro do módulo:**

- Dados do perfil acadêmico.
- Exibição pública ou oculta do autor.
- Verificação de CRM, títulos e matrícula.
- Selos.
- Desativação e exclusão da conta, com as questões permanecendo no banco.
- Exportação dos dados pessoais (LGPD).
- O mínimo da fila manual de verificação, do lado da equipe.

**Fora do módulo:**

- Cadastro, login e sessões → módulo 01. Aqui só entra o link para a lista de dispositivos.
- Gestão das questões publicadas (criar, editar, excluir) → módulo 03.
- Overwatch e selo de revisões → fase futura.

## 2. Mudanças em relação aos documentos-fonte

Todas foram aceitas em D-11 e prevalecem sobre os documentos-fonte.

| # | Documento-fonte dizia | Decisão | Motivo |
|---|---|---|---|
| P-01 | Escada de 5 selos, com “peso de autoria” crescente | **Selos cumulativos e sem peso.** O usuário pode ter vários (ex.: Especialista + Mestre). O cartão da questão mostra o selo principal, e o perfil mostra todos | A ordem das questões é aleatória (RN-06), então o “peso” não tem função. Uma escada única também não comporta quem é especialista e mestre ao mesmo tempo |
| P-02 | Situação atual com 5 opções, incluindo “médico em preparação para residência” e “médico formado” | **4 opções:** estudante, médico, residente, especialista. “Em preparação para residência” vira uma marcação opcional | As duas opções de médico geram o mesmo selo. A marcação continua útil para o produto (ex.: mostrar editais no Pro) |
| P-03 | Estudante entra no selo só por preencher a formação | **Selo de estudante exige verificação:** e-mail institucional ou comprovante de matrícula | Sem isso, o selo de estudante vira autodeclaração e perde valor. O e-mail institucional resolve a maioria dos casos sem fila manual |
| P-04 | CRM conferido no Webservice do CFM | **No piloto, CRM e especialidade são verificados manualmente:** o usuário envia a carteira do CRM, e a fila confere na Busca por Médicos do portal do CFM, que é pública e gratuita | O webservice custa R$ 948 por ano e exige CNPJ. A consulta dele só confirma que o CRM existe, e não que quem se cadastra é aquele médico. A carteira resolve as duas coisas. O webservice volta a ser avaliado quando houver CNPJ e volume (D-12) |
| P-05 | “Termo assinado” para exibir os dados | **Aceite eletrônico versionado**, igual aos termos do módulo 01. Não há assinatura digital | Mesma prova jurídica com muito menos atrito. Confirmar com advogado |
| P-06 | Excluir a conta anonimiza o autor (a confirmar) | **Confirmado, com prazo de carência de 30 dias** e manutenção do selo que o autor tinha na publicação | A carência evita exclusão por engano. O selo preservado mantém a confiança na questão sem identificar ninguém |
| P-07 | Não existia | **Desativar a conta**, como pausa reversível | Atende quem quer sumir por um tempo sem perder o progresso |

## 3. Estrutura da área da conta

Menu da área logada:

1. **Perfil:** dados pessoais e acadêmicos.
2. **Selos e verificações:** selos ativos, verificações pendentes e envio de comprovantes.
3. **Privacidade e exibição:** modo público ou oculto e prévia de como o autor aparece.
4. **Dispositivos:** sessões ativas (módulo 01).
5. **Dados e conta:** exportar dados, desativar e excluir a conta.
6. **Minhas questões:** link para o módulo 03.

## 4. Dados do perfil

O perfil é opcional para estudar. Ele só é exigido para criar questões (RN-10). Os campos marcados como “para criar questão” definem o que é um **perfil completo**.

### 4.1 Identificação

| Campo | Obrigatório para criar questão | Regra |
|---|---|---|
| Nome completo | Sim | Até 120 caracteres. Fica travado depois que um CRM é verificado, e só muda por nova verificação |
| Nome de exibição | Não | Vem do módulo 01. Usado na área logada, nunca nas questões |
| Breve histórico | Não | Até 500 caracteres, texto simples. Aparece só no modo público |
| Link do Lattes | Não | URL de `lattes.cnpq.br`. Ajuda na verificação de pós-graduação |

Não há foto no piloto. Foto exige moderação e é mais um dado pessoal a proteger.

### 4.2 Situação atual

| Campo | Obrigatório para criar questão | Regra |
|---|---|---|
| Situação | Sim | Uma de: estudante, médico, residente, especialista |
| Em preparação para residência | Não | Marcação sim ou não. Não gera selo |

### 4.3 Formação em Medicina

| Campo | Obrigatório para criar questão | Regra |
|---|---|---|
| Universidade | Sim | Escolhida de uma lista dos cursos de Medicina do e-MEC, com a opção “Instituição estrangeira” (texto livre) |
| Ano de ingresso | Não | Ano com 4 dígitos |
| Ano de conclusão | Sim para médicos | Para estudantes, é o ano previsto |

### 4.4 CRM (médicos)

| Campo | Regra |
|---|---|
| Número | Só dígitos |
| UF | Lista das 27 UFs |
| Inscrições adicionais | O usuário pode informar mais de um CRM, de UFs diferentes. Basta um verificado para o selo |

### 4.5 Residência (zero ou mais)

| Campo | Regra |
|---|---|
| Programa | Especialidade, de uma lista fixa das especialidades reconhecidas |
| Instituição | Texto livre no piloto |
| Ano de início e de conclusão | Conclusão prevista, se estiver em curso |
| Situação | Em curso ou concluída |

### 4.6 Pós-graduação stricto sensu (zero ou mais)

| Campo | Regra |
|---|---|
| Tipo | Mestrado ou doutorado |
| Área | Texto livre |
| Instituição | Texto livre |
| Ano de conclusão | Ano com 4 dígitos |
| Situação | Em curso ou concluída. Só a concluída gera selo |

## 5. Verificação

Cada item verificável tem um status: **não enviado**, **pendente**, **aprovado**, **recusado** (com motivo) ou **revogado** (com motivo).

### 5.1 Matriz de verificação

| Item | Como é verificado | Automático? | Selo |
|---|---|---|---|
| Matrícula em Medicina | Código enviado a um e-mail institucional da universidade escolhida | Sim | Estudante |
| Matrícula em Medicina (alternativa) | Comprovante de matrícula do semestre atual | Não, fila manual | Estudante |
| CRM | Carteira do CRM (física ou digital) conferida na Busca por Médicos do CFM: número, UF, nome e situação ativa | Não, fila manual | Médico |
| Especialidade com RQE | Conferida na mesma consulta da Busca por Médicos, que mostra as especialidades registradas | Não, fila manual | Especialista |
| Título de especialista sem RQE | Certificado de conclusão de residência ou título de sociedade | Não, fila manual | Especialista |
| Residência em curso | Declaração do programa ou da COREME, emitida há até 90 dias | Não, fila manual | Residente |
| Mestrado ou doutorado | Diploma ou ata de defesa, com o Lattes como apoio | Não, fila manual | Mestre ou Doutor |

### 5.2 Regras do CRM

No piloto, a verificação do CRM é manual. Fluxo:

1. O usuário informa número e UF e envia a carteira do CRM, física (foto da frente) ou digital (captura de tela do CRM Virtual).
2. O sistema confere se aquele CRM já está verificado em outra conta. Se estiver, o pedido entra na fila marcado como conflito.
3. Quem cuida da fila abre a Busca por Médicos do portal do CFM (`portal.cfm.org.br/busca-medicos`) e confere:
   - se número, UF e nome da carteira batem com o registro;
   - se o nome do perfil bate com o registro, sem considerar acentos e maiúsculas;
   - se a situação é **ativa**;
   - quais especialidades com RQE aparecem, para os selos de especialista.
4. A pessoa aprova ou recusa, com motivo, e registra o que viu: situação e especialidades com RQE.

Regras:

1. Só a situação **ativa** gera o selo. Inscrição cancelada, suspensa ou cassada é recusada, sem expor o motivo no perfil público.
2. Um CRM só pode estar verificado em uma conta. A segunda conta fica sem o selo até a análise do conflito.
3. A consulta é sempre feita, uma por vez, na tela pública do CFM. O projeto não copia, não raspa e não guarda a base de médicos. Guarda só o que conferiu sobre o próprio usuário.
4. No piloto não há reconsulta periódica. A curadoria reconfere quando houver denúncia ou, por amostragem, uma vez por ano. Se a situação deixou de ser ativa, o selo é revogado e o usuário recebe aviso.
5. A reconsulta automática mensal entra quando o webservice for contratado (D-12).

### 5.3 Regras do e-mail institucional

1. A lista de domínios aceitos é mantida pela equipe, por universidade (ex.: `usp.br` para a USP).
2. O usuário informa o e-mail, recebe um código de 6 dígitos e confirma. As regras de validade e de tentativas são as do módulo 01.
3. O e-mail institucional serve só para a verificação. Ele não vira login e não recebe outras mensagens.
4. O selo de estudante vale até o ano de conclusão previsto mais um ano. Depois, o usuário precisa verificar de novo ou passar a médico.

### 5.4 Comprovantes enviados

| Regra | Valor proposto |
|---|---|
| Formatos | PDF, JPG ou PNG |
| Tamanho | Até 5 MB por arquivo |
| Armazenamento | Privado. Só a fila manual acessa |
| Retenção | Apagado 90 dias depois da decisão. Fica guardado só o registro: tipo, decisão, data e quem decidiu |
| Recusa | Sempre com motivo, escolhido de uma lista (ilegível, documento vencido, nome diferente, documento não aceito, outro). O usuário pode reenviar |

### 5.5 Fila manual (lado da equipe)

O piloto precisa de uma tela simples para a equipe, com:

- Lista de pendências por ordem de chegada, com o tipo do item.
- Visualização do comprovante e dos dados do perfil lado a lado.
- Botões de aprovar ou recusar, com motivo.
- Registro de quem decidiu e quando.

Dono da fila no piloto e prazo de resposta: ver D-17.

Para pedidos de CRM, a tela também mostra o link direto para a Busca por Médicos e um aviso quando aquele CRM já está verificado em outra conta.

## 6. Selos

### 6.1 Lista

| Selo | Origem |
|---|---|
| Estudante de Medicina | Matrícula verificada |
| Médico | CRM ativo verificado |
| Residente | Residência em curso verificada |
| Especialista | RQE ou título verificado. Mostra a especialidade (ex.: “Especialista · Cardiologia”) |
| Mestre | Mestrado concluído verificado |
| Doutor | Doutorado concluído verificado |

Quem não tem nenhum item verificado fica **sem selo**. A questão dele é publicada normalmente (RN-05).

### 6.2 Selo principal

O cartão da questão mostra um selo só, escolhido nesta ordem: Doutor, Mestre, Especialista, Residente, Médico, Estudante. A ordem existe só para escolher o que cabe no cartão. Ela não muda a ordem das questões nem dá peso a nenhuma.

O perfil público mostra todos os selos ativos.

### 6.3 Selo na publicação

Cada questão guarda uma cópia do selo principal do autor na data da publicação. O cartão mostra o selo **atual**. Se o autor excluir a conta, passa a mostrar o selo guardado, com a indicação “na data da publicação”.

Se um selo for revogado por fraude, ele some também das cópias guardadas.

## 7. Privacidade e exibição

### 7.1 Modos

| Modo | O que aparece na questão | Página pública do autor |
|---|---|---|
| **Público** | Nome completo, selo principal, situação e universidade | Sim: nome, selos, situação, universidade, residências, pós-graduações, breve histórico, Lattes e número de questões publicadas |
| **Oculto** (padrão) | “Autor verificado” e o selo principal. Sem selo: “Autor da comunidade” | Não |

O modo oculto é o padrão. O modo público exige o aceite do termo de exibição pública (P-05).

### 7.2 Regras

1. O usuário vê uma prévia de como aparece em cada modo antes de escolher.
2. Trocar o modo vale na hora para todas as questões dele, inclusive as antigas, porque o nome é montado na exibição e não gravado na questão.
3. O número do CRM nunca aparece publicamente, em nenhum modo.
4. Ao ocultar, as cópias das questões feitas fora do site antes da troca continuam com o nome antigo. O termo de exibição pública avisa isso.
5. A licença CC BY-SA 4.0 permite ao autor pedir que a atribuição seja feita por pseudônimo ou retirada. O modo oculto se apoia nisso. Confirmar com advogado.

## 8. Desativar a conta

Pausa reversível.

**Ao desativar:**

1. Todas as sessões são encerradas.
2. A página pública do autor sai do ar, e as questões passam a mostrar o autor como no modo oculto.
3. As questões continuam no banco e no simulado.
4. Progresso, perfil, selos e verificações ficam guardados.
5. Os e-mails transacionais param, exceto os ligados à própria conta (ex.: aviso de reativação).

**Para reativar:** basta entrar de novo pelo login do módulo 01. O site pergunta se ele quer reativar, e tudo volta como estava.

Não há prazo máximo de desativação no piloto.

## 9. Excluir a conta

### 9.1 Fluxo

1. O usuário escolhe “Excluir conta”. A tela explica o que é apagado e o que fica (9.2).
2. Ele confirma digitando o próprio e-mail.
3. A conta entra em **exclusão agendada** por 30 dias, com o mesmo efeito da desativação.
4. Ele recebe um e-mail com a data da exclusão e a forma de cancelar: entrar de novo no site.
5. Ao fim dos 30 dias, a exclusão é executada e um último e-mail confirma.

### 9.2 O que é apagado e o que fica

| Dado | Destino |
|---|---|
| E-mail, nome, perfil, breve histórico, Lattes | Apagados |
| CRM, e-mail institucional e registros de verificação | Apagados |
| Comprovantes ainda guardados | Apagados |
| Progresso de estudo (tentativas) | Apagado |
| Sessões e registros de login | Apagados |
| Aceites de termos | Guardados pelo prazo legal, sem ligação com dados que identifiquem a pessoa. Confirmar o prazo com advogado |
| Questões publicadas | **Ficam no banco e no simulado**, sob CC BY-SA, com autor “Autor da comunidade” e o selo da publicação (6.3) |
| Comentários e contestações | Ficam, com autor anônimo |
| Avaliações (concordância, “caiu na prova”) | Ficam nas estatísticas da questão, sem ligação com a pessoa |

### 9.3 Antes de excluir

A tela de exclusão oferece:

- **Exportar meus dados** (seção 10).
- **Desativar em vez de excluir.**
- Link para **Minhas questões**, para quem quiser retirar alguma antes (regras no módulo 03).

## 10. Exportar meus dados

Atende o direito de acesso e portabilidade da LGPD.

1. O usuário pede a exportação em “Dados e conta”.
2. O sistema gera um arquivo JSON com: dados da conta, perfil, selos, histórico de verificações (sem os comprovantes), aceites de termos, progresso completo, questões publicadas, comentários e contestações.
3. O link de download vai por e-mail, vale 7 dias e exige estar logado.
4. Limite de um pedido a cada 24 horas.

## 11. Notificações deste módulo

| Gatilho | Canal |
|---|---|
| Código de verificação do e-mail institucional | E-mail institucional |
| Comprovante ou carteira do CRM recebidos | Site |
| Verificação aprovada ou recusada, com motivo | E-mail e site |
| Selo revogado, com motivo | E-mail e site |
| Selo de estudante perto de vencer (30 dias antes) | E-mail e site |
| Modo de exibição alterado | Site |
| Conta desativada | E-mail |
| Exclusão agendada, com data e forma de cancelar | E-mail |
| Exclusão concluída | E-mail |
| Exportação pronta | E-mail |

## 12. Exceções

| Situação | O que acontece | Quem resolve |
|---|---|---|
| CRM não encontrado na Busca por Médicos | Recusado com motivo. O usuário pode corrigir número ou UF e reenviar | Fila manual |
| Nome do perfil diferente do registro do CRM | Recusado com motivo “nome diferente”. O usuário corrige o nome e reenvia | Fila manual |
| Carteira ilegível ou de outra pessoa | Recusada com motivo | Fila manual |
| CRM com situação não ativa | Recusado. O motivo não aparece publicamente | Fila manual |
| CRM já verificado em outra conta | Segunda conta sem selo até a análise do conflito | Fila manual |
| Busca por Médicos fora do ar | O pedido fica pendente até a consulta voltar | Fila manual |
| Domínio do e-mail institucional não está na lista | Oferece o envio de comprovante e um pedido de inclusão do domínio | Fila manual |
| Usuário quer mudar o nome depois do CRM verificado | Precisa de nova verificação | Fila manual |
| Comprovante suspeito de falsificação | Recusado. Se confirmado, todos os selos do usuário são revogados e a conta é suspensa | Fila manual |
| Usuário cancela a exclusão no prazo | Conta volta ao normal | Automático |
| Usuário tenta excluir com questões em contestação | A exclusão segue. As contestações continuam abertas para a curadoria | Automático |
| Breve histórico com conteúdo ofensivo ou propaganda | Pode ser denunciado. A curadoria remove o texto | Curadoria |

## 13. Regras de negócio deste módulo

A numeração continua a do módulo 01.

| ID | Regra |
|---|---|
| RN-26 | Perfil completo = nome completo, situação e universidade. Médicos também informam o ano de conclusão |
| RN-27 | Selos são cumulativos e não dão peso nem ordem às questões |
| RN-28 | O cartão da questão mostra só o selo principal, pela ordem da seção 6.2 |
| RN-29 | Todo selo depende de um item verificado. Sem item verificado, o usuário fica sem selo |
| RN-30 | No piloto, o CRM é verificado manualmente: carteira do CRM conferida na Busca por Médicos do CFM. Só gera selo com situação ativa e só pode estar verificado em uma conta |
| RN-38 | O projeto não copia, não raspa e não guarda a base de médicos do CFM. Guarda só o que conferiu sobre o próprio usuário |
| RN-31 | O nome completo fica travado depois da verificação do CRM |
| RN-32 | O modo oculto é o padrão. O modo público exige o aceite do termo de exibição |
| RN-33 | O número do CRM nunca é exibido publicamente |
| RN-34 | O nome do autor é montado na exibição. Trocar o modo afeta todas as questões na hora |
| RN-35 | Comprovantes são apagados 90 dias depois da decisão. Fica só o registro da decisão |
| RN-36 | Desativar é reversível pelo login e mantém tudo guardado |
| RN-37 | Excluir tem carência de 30 dias. Depois, os dados pessoais são apagados e as questões ficam, com autor anônimo e o selo da publicação |
| RN-17 (nova) | Substituída pela RN-37 |

## 14. Modelo de dados (rascunho)

Complementa as tabelas do módulo 01.

```
users  (acréscimos)
  status              "ativa" | "desativada" | "exclusao_agendada" | "suspensa"
  deletion_due_at     data/hora, opcional

profiles
  user_id             fk users, pk
  full_name           texto
  full_name_locked    booleano
  bio                 texto, até 500
  lattes_url          texto
  situation           "estudante" | "medico" | "residente" | "especialista"
  preparing_residency booleano
  university_id       fk universities, opcional
  foreign_university  texto, opcional
  admission_year      inteiro
  graduation_year     inteiro
  display_mode        "publico" | "oculto"
  updated_at          data/hora

universities
  id, nome, uf, codigo_emec
  email_domains       lista de texto

crm_registrations
  id, user_id, number, uf
  checked_status      situação vista na conferência (ex.: "ativa")
  checked_specialties especialidades com RQE vistas na conferência
  check_source        "manual" (piloto) | "webservice" (futuro)
  checked_by          fk equipe, opcional
  verified_at, last_checked_at

residencies
  id, user_id, specialty_id, institution
  start_year, end_year, status

postgraduates
  id, user_id, type, area, institution, year, status

verifications
  id, user_id
  item_type           "matricula" | "crm" | "especialista" | "residencia" | "pos"
  item_id             referência ao item verificado
  method              "carteira_crm" | "email_institucional" | "comprovante" | "webservice_cfm" (futuro)
  status              "pendente" | "aprovado" | "recusado" | "revogado"
  reason              texto, opcional
  file_key            chave do arquivo, opcional
  file_delete_at      data/hora
  decided_by          fk equipe, opcional
  decided_at          data/hora

badges
  id, user_id
  type                "estudante" | "medico" | "residente" | "especialista" | "mestre" | "doutor"
  detail              ex.: especialidade
  verification_id     fk verifications
  valid_until         data/hora, opcional
  revoked_at          data/hora, opcional

questions  (acréscimo, detalhado no módulo 03)
  author_badge_snapshot  selo principal na data da publicação
```

## 15. Critérios de aceite

```gherkin
Funcionalidade: Perfil, selos e conta

  Cenário: CRM aprovado pela fila manual
    Dado um usuário com nome "Ana Souza" no perfil
    E ele enviou número, UF e a carteira do CRM
    Quando a curadoria aprova a verificação, registrando situação "ativa"
    Então ele recebe o selo "Médico"
    E o nome completo fica travado

  Cenário: Especialidade registrada na conferência
    Dado que a curadoria aprova um CRM
    E registra a especialidade "Cardiologia" com RQE
    Então o usuário recebe também o selo "Especialista · Cardiologia"

  Cenário: CRM já verificado em outra conta
    Dado que o CRM 12345/SP já está verificado na conta A
    Quando a conta B envia o mesmo CRM
    Então o pedido entra na fila marcado como conflito
    E a conta B fica sem o selo até a análise

  Cenário: Selo principal no cartão
    Dado um autor com os selos "Especialista · Cardiologia" e "Mestre"
    Quando uma questão dele é exibida
    Então o cartão mostra "Mestre"
    E a página pública mostra os dois selos

  Cenário: Troca para o modo oculto
    Dado um autor em modo público com 10 questões publicadas
    Quando ele muda para o modo oculto
    Então as 10 questões passam a mostrar "Autor verificado" e o selo principal
    E a página pública dele sai do ar

  Cenário: Exclusão com questões publicadas
    Dado um autor com 5 questões publicadas e selo "Residente"
    Quando ele pede a exclusão e passam 30 dias
    Então o e-mail, o perfil e o progresso são apagados
    E as 5 questões continuam no simulado
    E mostram "Autor da comunidade" e "Residente na data da publicação"

  Cenário: Cancelar a exclusão
    Dado uma conta em exclusão agendada há 10 dias
    Quando o usuário entra de novo
    Então a exclusão é cancelada
    E a conta volta ao normal

  Cenário: CRM deixa de estar ativo
    Dado um usuário com selo "Médico"
    Quando a curadoria reconfere o CRM e registra situação "cancelada"
    Então o selo é revogado
    E o usuário recebe um aviso
```

## 16. Decisões tomadas

Fechadas em 2026-11-15, todas conforme a recomendação.

| ID | Tema | Decisão |
|---|---|---|
| D-11 | Mudanças P-01 a P-07 | Aceitas |
| D-12 | Webservice do CFM | **Decidido:** fora do piloto. Ele custa R$ 948 por ano, exige CNPJ e é gratuito só para entidades públicas. Volta à pauta quando o projeto tiver CNPJ e volume que justifique. Opcional: pedir isenção por e-mail ao CFM (`webservice@portalmedico.org.br`) |
| D-13 | Modo padrão de exibição | Oculto |
| D-14 | Documentos aceitos | Lista da seção 5.1, revisada com os primeiros casos reais |
| D-15 | Prazos | Comprovantes apagados em 90 dias, carência de exclusão de 30 dias, selo de estudante válido até a conclusão prevista mais um ano |
| D-16 | Pós-graduação fora da área da saúde | Não gera selo. Só mestrado e doutorado em área da saúde |
| D-17 | Fila manual no piloto | Dono: Rafael. Prazo de resposta: 7 dias úteis |
| D-18 | Fraude confirmada | Conta suspensa, selos revogados e questões enviadas para revisão da curadoria |
| D-19 | Edição de questões de quem excluiu a conta | Só pela curadoria, para corrigir erro. Detalhe no módulo 03 |

## 17. Pendências antes de desenvolver

As decisões estão fechadas. Faltam duas ações práticas, e nenhuma impede o código de começar:

1. **Advogado:** termo de exibição pública, uso da CC BY-SA com pseudônimo, prazo de guarda dos aceites e retenção de comprovantes.
2. **Listas de referência:** cursos de Medicina do e-MEC, domínios de e-mail por universidade e especialidades reconhecidas.
