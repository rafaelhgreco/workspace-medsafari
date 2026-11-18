# Módulo 01: cadastro, login e sessão

2026-11-15 · rafael · v2: decisões D-01 a D-10 fechadas

Documentos-fonte: `produto-banco-questoes-residencia.md` e `workflow-jornada-novo-usuario.md`.

## 1. Objetivo e limites

Este módulo define como um visitante vira usuário cadastrado, como ele entra de novo em outro navegador e como o progresso de estudo passa do navegador para o banco.

**Dentro do módulo:**

- Prática anônima com progresso no navegador.
- Cadastro por e-mail, com aceite de termos.
- Login sem senha (link ou código por e-mail).
- Sessão, logout e logout de todos os dispositivos.
- Migração e sincronização do progresso.
- Proteções contra abuso (limites de envio e de tentativas).

**Fora do módulo (documentos próprios):**

- Perfil acadêmico, CRM e títulos → módulo 02.
- Prática de questões e simulado → módulo 03.
- Exclusão de conta e direitos LGPD → módulo 07. Aqui só entram os pontos que tocam a sessão.

## 2. Mudanças em relação aos documentos-fonte

As mudanças abaixo fecham pontas que os documentos deixaram em aberto. Todas foram aceitas em D-01 e prevalecem sobre os documentos-fonte.

| # | Documento-fonte dizia | Decisão | Motivo |
|---|---|---|---|
| M-01 | O sistema envia a session ID por e-mail, para o usuário guardar | **Não enviar a session ID.** Ela deixa de existir como algo que o usuário vê. Internamente, há um `user_id` e uma sessão em cookie | Uma session ID no e-mail é uma senha permanente parada na caixa de entrada. O login por e-mail já resolve a recuperação, então guardar a ID não acrescenta nada e só aumenta o risco |
| M-02 | Login por link (proposta). Link, código ou ambos? | **Ambos no mesmo e-mail:** um link e um código de 6 dígitos | O link é mais prático no mesmo aparelho. O código resolve o caso comum de abrir o e-mail no celular e estudar no computador |
| M-03 | Vínculo de e-mail e login eram fluxos separados | **Um único fluxo:** “informe seu e-mail”. Se a conta não existe, ela é criada depois da confirmação | Simplifica telas e código, e não revela quem tem conta (RN-04) |
| M-04 | O progresso vai para o banco ao vincular? (a confirmar) | **Sim.** O progresso do navegador é enviado e somado ao da conta | Perder o que o visitante já estudou é o pior motivo para ele não se cadastrar |
| M-05 | Exceção: “perde a session ID e não tem acesso ao e-mail” | Passa a ser **“perdeu o acesso ao e-mail”**. Sem recuperação automática no piloto. O suporte trata | Sem session ID para perder, só sobra o e-mail como chave |

## 3. Dados pedidos no cadastro

O cadastro pede o mínimo. Tudo que é acadêmico fica para o perfil (módulo 02), e só é exigido de quem quer criar questões.

### 3.1 Informados pelo usuário

| Campo | Obrigatório | Regra |
|---|---|---|
| E-mail | Sim | Formato válido, até 254 caracteres. Normalizado: sem espaços nas pontas e em minúsculas. Pontos e `+` são mantidos como digitados |
| Aceite dos Termos de Uso | Sim | Caixa desmarcada por padrão. Grava a versão aceita |
| Ciência da Política de Privacidade | Sim | Mesmo tratamento. Pode ser a mesma caixa dos termos, com os dois links |
| Nome de exibição | Não | Opcional. Se vazio, o site usa “Você”. O nome completo e verificado fica no perfil |

### 3.2 Gerados pelo sistema

| Campo | Uso |
|---|---|
| `user_id` (UUID) | Identificador interno. Nunca aparece para o usuário nem vai por e-mail |
| `created_at`, `email_verified_at` | Auditoria |
| Versão e data/hora do aceite de cada termo | Prova do aceite (LGPD) |
| `device_id` (UUID gerado no navegador) | Liga o progresso anônimo à conta na migração |
| Sessões ativas | Ver seção 6 |

### 3.3 O que **não** é pedido no cadastro

Senha, CPF, telefone, CRM, universidade, data de nascimento e declaração de idade. Cada dado a mais é um dado pessoal a proteger e um motivo a mais para o visitante desistir.

Não há restrição de idade (D-04). O site é aberto e educacional, e o público real tem 17 anos ou mais (estudantes de Medicina em diante). Pela LGPD, o consentimento dos pais só é exigido para crianças de até 12 anos, e a ANPD (Enunciado CD/ANPD nº 1/2023) admite as demais bases legais para adolescentes, desde que respeitado o melhor interesse deles. O advogado deve confirmar se o ECA Digital (Lei 15.211/2025) impõe alguma obrigação a um serviço com esse público.

## 4. Estados do usuário neste módulo

| Estado | Como entra | Onde fica o progresso |
|---|---|---|
| Visitante | Abre o site | Só no navegador (`localStorage`) |
| Aguardando confirmação | Informou o e-mail e o sistema enviou link e código | Ainda só no navegador |
| Cadastrado | Confirmou o e-mail e aceitou os termos | No banco, com cópia no navegador |

Os estados “Estudante”, “Médico verificado” e seguintes partem de “Cadastrado” e são tratados no módulo 02.

## 5. Fluxos

### 5.1 Prática anônima

1. Ao abrir o site pela primeira vez, o navegador gera um `device_id` e o guarda no `localStorage`.
2. Cada resposta é gravada localmente como uma **tentativa**, com um `attempt_id` gerado no navegador (ver seção 7).
3. Depois de um número de respostas (proposta: 10), o site mostra um aviso discreto: “seu progresso está só neste navegador. Informe seu e-mail para não perder”. O aviso não bloqueia o estudo.

### 5.2 Entrar ou criar conta (fluxo único)

1. O usuário clica em “Salvar progresso” ou “Entrar” e informa o e-mail.
2. O sistema responde sempre com a mesma mensagem: “Se este e-mail puder ser usado, enviamos um link e um código. Confira também o spam.” (RN-04).
3. O sistema envia um e-mail com:
   - um link de acesso, de uso único;
   - um código de 6 dígitos;
   - a validade dos dois (proposta: 15 minutos).
4. O usuário clica no link **ou** digita o código na tela que ficou aberta.
5. O sistema confere o token:
   - **Conta existente:** cria a sessão e vai para o passo 7.
   - **Conta nova:** mostra a tela de termos (seção 3.1). Ao aceitar, cria a conta, marca o e-mail como confirmado e cria a sessão.
6. Se o usuário fechar a tela de termos sem aceitar, a conta não é criada. O token já foi usado, então ele precisa pedir outro.
7. O navegador envia o progresso local para o banco (seção 7.2) e recebe de volta o progresso completo da conta.
8. O site confirma: “Pronto. Seu progresso está salvo na sua conta.”

**Por que os termos aparecem depois da confirmação, e não antes do envio:** se a tela de envio pedisse o aceite só para contas novas, ela revelaria quais e-mails já têm conta.

### 5.3 Entrar em outro navegador ou computador

É o mesmo fluxo da 5.2. No passo 7, o navegador novo pode já ter progresso anônimo. Nesse caso, os dois são somados, sem perda (seção 7.3).

### 5.4 Logout

- **Sair deste dispositivo:** encerra a sessão atual e apaga o progresso do `localStorage`. O progresso continua no banco.
- **Sair de todos os dispositivos:** encerra todas as sessões da conta. Fica na tela de conta.

Apagar o `localStorage` no logout evita que a próxima pessoa no mesmo computador (por exemplo, numa biblioteca) veja o progresso de quem saiu.

## 6. Sessão e tokens

Todos os valores são **propostas** para validar.

### 6.1 Token de acesso (link e código)

| Item | Valor proposto |
|---|---|
| Link | Token aleatório de 32 bytes, em URL. Guardado no banco só como hash (SHA-256) |
| Código | 6 dígitos numéricos. Guardado como hash, ligado ao mesmo pedido do link |
| Validade | 15 minutos |
| Uso | Único. Usar o link invalida o código, e vice-versa |
| Tentativas de código | 5 erros invalidam o pedido. O usuário pede um novo |
| Pedido novo | Invalida os pedidos anteriores ainda abertos do mesmo e-mail |

O link abre uma página que pede um clique em “Entrar” antes de consumir o token. Isso impede que leitores de e-mail corporativos, que abrem links sozinhos para checar segurança, gastem o token antes do usuário.

### 6.2 Sessão

| Item | Valor proposto |
|---|---|
| Transporte | Cookie `HttpOnly`, `Secure`, `SameSite=Lax` |
| Conteúdo | Identificador aleatório. No banco, só o hash |
| Duração | 30 dias, renovada a cada uso (validade deslizante) |
| Limite absoluto | 90 dias. Depois disso, novo login por e-mail |
| Dados guardados por sessão | Data de criação, último uso e um rótulo do navegador (ex.: “Chrome no Windows”) para a lista de dispositivos |

A sessão nunca vai para o `localStorage`, porque qualquer script na página consegue ler o `localStorage`.

### 6.3 Limites contra abuso

| Limite | Valor proposto |
|---|---|
| Envios por e-mail | 3 a cada 15 minutos, 10 por dia |
| Envios por IP | 20 por hora |
| Tentativas de código por IP | 30 por hora |
| Resposta ao estourar o limite | A mesma mensagem genérica de sempre, para não revelar nada. O e-mail simplesmente não é enviado |

## 7. Progresso: formato, migração e sincronização

### 7.1 Formato

O progresso é guardado como uma lista de tentativas, e não como “última resposta por questão”. Somar duas listas é simples e não perde dados.

```json
{
  "schema_version": 1,
  "device_id": "uuid",
  "attempts": [
    {
      "attempt_id": "uuid gerado no navegador",
      "question_id": "id da questão",
      "selected_option": "C",
      "is_correct": true,
      "answered_at": "2026-11-15T12:34:56Z"
    }
  ]
}
```

As marcações de concordância, “caiu na prova” e contestações são do módulo de avaliação (05) e não entram neste formato.

### 7.2 Migração no cadastro ou login

1. O navegador envia todas as tentativas locais.
2. O servidor grava cada uma ligada ao `user_id`. Uma tentativa com `attempt_id` já gravado é ignorada. Assim, enviar duas vezes não duplica nada.
3. O servidor devolve o progresso completo da conta, e o navegador substitui o `localStorage` por ele.
4. Se o envio falhar, o progresso local continua intacto e o navegador tenta de novo no próximo acesso.

### 7.3 Soma de progresso de dois lugares

Como cada tentativa tem seu próprio `attempt_id`, somar é unir as duas listas. Não há conflito a resolver. Estatísticas (acertos por domínio etc.) são sempre calculadas a partir da lista.

### 7.4 Estudo já logado

1. Cada resposta é gravada no `localStorage` e enviada ao servidor.
2. Se o envio falhar (rede caiu), a tentativa fica numa fila local e é reenviada depois.
3. O banco é a fonte de verdade (RN-02). Ao entrar, o navegador sempre baixa o progresso do servidor.

### 7.5 Navegador sem `localStorage`

O site funciona só com o servidor e avisa o usuário. Sem login e sem `localStorage`, o progresso dura só até fechar a aba, e o aviso diz isso.

## 8. E-mails deste módulo

O piloto envia um só e-mail transacional neste módulo. Ele substitui os três gatilhos do workflow (confirmação, login e session ID).

**Assunto:** `Seu acesso ao [nome do projeto]`

**Corpo (rascunho):**

> Use o botão abaixo para entrar:
>
> [Entrar]
>
> Ou digite este código na tela aberta: **483 920**
>
> O link e o código valem por 15 minutos e só funcionam uma vez.
>
> Se você não pediu este acesso, ignore este e-mail. Ninguém entra na sua conta sem ele.

**Regras:**

- Sem conteúdo promocional.
- Sem dados do usuário além do código.
- Remetente fixo, com SPF, DKIM e DMARC configurados no domínio, para não cair no spam.

## 9. Exceções

| Situação | O que acontece | Quem resolve |
|---|---|---|
| E-mail não chega | O usuário pode pedir reenvio após 60 segundos, dentro dos limites da 6.3. A tela lembra de olhar o spam | Automático. Suporte, se persistir |
| Link expirado, já usado ou substituído | Página explica e oferece “Enviar novo acesso” | Automático |
| Código errado | Mostra quantas tentativas restam. Na 5ª, invalida o pedido | Automático |
| Link aberto em outro navegador | Funciona. A sessão é criada no navegador onde o link foi aberto, e o progresso daquele navegador é somado | Automático |
| Usuário fecha a tela de termos | Conta não é criada. Precisa pedir novo acesso | Automático |
| Perdeu o acesso ao e-mail | Sem recuperação automática no piloto | Suporte, processo a definir (D-07) |
| Envio de progresso falha | Progresso local é mantido e reenviado depois | Automático |
| Sessão expirada no meio do estudo | As respostas continuam sendo gravadas no navegador. O site pede novo login e sobe as respostas pendentes depois | Automático |
| Termos mudam de versão | No próximo acesso, o usuário vê a nova versão e precisa aceitar para continuar logado | Automático |
| E-mail já usado por outra conta | Não acontece: o e-mail é a chave única da conta | Automático |

## 10. Regras de negócio deste módulo

Os IDs continuam a numeração do workflow. As regras RN-01 e RN-03 são **substituídas** pelas versões abaixo.

| ID | Regra |
|---|---|
| RN-01 (nova) | A conta é criada quando o usuário confirma o e-mail e aceita os termos. Nenhum identificador de sessão é enviado por e-mail |
| RN-02 | Antes do cadastro, o progresso fica só no navegador. Depois, o banco é a fonte de verdade e o navegador guarda uma cópia |
| RN-03 (nova) | O login é feito por link ou código de 6 dígitos enviados ao e-mail, no mesmo fluxo do cadastro |
| RN-04 | A resposta ao pedido de acesso é sempre a mesma, exista ou não a conta |
| RN-19 | Um e-mail corresponde a uma única conta |
| RN-20 | Link e código são de uso único, valem 15 minutos e são guardados só como hash |
| RN-21 | Ao entrar, o progresso do navegador é somado ao da conta, sem perda e sem duplicação |
| RN-22 | A sessão fica em cookie `HttpOnly` e nunca no `localStorage` |
| RN-23 | Sair do dispositivo apaga o progresso local. Sair de todos encerra todas as sessões |
| RN-24 | O aceite de termos guarda a versão e a data. Uma versão nova exige novo aceite |
| RN-25 | O cadastro pede só o e-mail e os aceites, sem restrição de idade. Dados acadêmicos ficam no perfil |

## 11. Modelo de dados (rascunho)

Os nomes são sugestões para o desenvolvimento.

```
users
  id                  uuid, pk
  email               texto, único, normalizado
  display_name        texto, opcional
  email_verified_at   data/hora
  created_at          data/hora
  deleted_at          data/hora, opcional

login_requests
  id                  uuid, pk
  email               texto
  token_hash          texto
  code_hash           texto
  code_attempts       inteiro
  expires_at          data/hora
  used_at             data/hora, opcional
  requested_ip        texto
  created_at          data/hora

sessions
  id                  uuid, pk
  user_id             fk users
  token_hash          texto
  user_agent_label    texto
  created_at          data/hora
  last_used_at        data/hora
  expires_at          data/hora
  revoked_at          data/hora, opcional

terms_acceptances
  id                  uuid, pk
  user_id             fk users
  document            "termos" | "privacidade"
  version             texto
  accepted_at         data/hora
  ip                  texto

attempts
  attempt_id          uuid, pk (gerado no navegador)
  user_id             fk users
  question_id         fk questões
  selected_option     texto
  is_correct          booleano
  answered_at         data/hora
  device_id           uuid
  synced_at           data/hora
```

Retenção proposta: `login_requests` apagados após 30 dias. Sessões revogadas ou expiradas apagadas após 90 dias. IPs guardados só para segurança, com o prazo definido na Política de Privacidade.

## 12. Critérios de aceite

```gherkin
Funcionalidade: Cadastro e login por e-mail

  Cenário: Visitante cria conta e mantém o progresso
    Dado que um visitante respondeu 12 questões sem login
    Quando ele informa um e-mail sem conta
    E abre o link recebido
    E aceita os termos
    Então a conta é criada com o e-mail confirmado
    E as 12 tentativas aparecem no progresso da conta

  Cenário: Resposta igual para e-mail com e sem conta
    Quando alguém pede acesso para um e-mail cadastrado
    E depois para um e-mail não cadastrado
    Então as duas respostas na tela são idênticas

  Cenário: Login por código em outro aparelho
    Dado que o usuário pediu acesso no computador
    Quando ele lê o e-mail no celular
    E digita o código de 6 dígitos no computador
    Então a sessão é criada no computador

  Cenário: Token usado uma vez
    Dado que o usuário entrou com o link
    Quando ele abre o mesmo link de novo
    Então o site informa que o link já foi usado
    E oferece enviar um novo acesso

  Cenário: Soma de progresso sem duplicar
    Dado que a conta tem 30 tentativas no banco
    E um navegador novo tem 5 tentativas anônimas
    Quando o usuário entra nesse navegador
    Então a conta passa a ter 35 tentativas
    E reenviar as mesmas 5 não altera o total

  Cenário: Limite de envios
    Dado que o e-mail recebeu 3 acessos nos últimos 15 minutos
    Quando um 4º acesso é pedido
    Então a tela mostra a mesma mensagem genérica
    E nenhum e-mail é enviado

  Cenário: Logout em computador compartilhado
    Dado que o usuário está logado
    Quando ele escolhe "Sair deste dispositivo"
    Então a sessão é encerrada
    E o progresso local é apagado
```

## 13. Decisões tomadas

Fechadas em 2026-11-15.

| ID | Tema | Decisão |
|---|---|---|
| D-01 | Mudanças M-01 a M-05 | Aceitas: sem session ID por e-mail, link + código, fluxo único e migração do progresso |
| D-02 | Validades e limites | Valores da seção 6, ajustados depois com dados do piloto |
| D-03 | Nome de exibição | Opcional no cadastro |
| D-04 | Restrição de idade | **Nenhuma.** Não há declaração de 18 anos ou mais. O site é aberto e educacional. Ver seção 3.3 |
| D-05 | Base legal da LGPD para e-mail e progresso | A definir com o advogado, junto com os termos |
| D-06 | Provedor de e-mail transacional | A escolher antes do desenvolvimento. Critérios: custo baixo no volume do piloto, boa entrega no Brasil e API simples |
| D-07 | Usuário que perdeu o acesso ao e-mail | No piloto, atendimento caso a caso pelo canal de contato. Sem troca automática de e-mail |
| D-08 | Troca de e-mail da conta | Fora do piloto. Quando entrar, exige confirmação no e-mail antigo e no novo |
| D-09 | Aviso “salve seu progresso” | Aparece depois de 10 respostas |
| D-10 | Login social (Google, Apple) | Fora do piloto. Reavaliar com dados de abandono no cadastro |

## 14. Pendências antes de desenvolver

As decisões estão fechadas. Faltam três ações práticas:

1. **Advogado:** base legal da LGPD (D-05), textos dos termos e checagem do ECA Digital (seção 3.3).
2. **Provedor de e-mail** escolhido (D-06), com o domínio de envio configurado (SPF, DKIM e DMARC).
3. **Primeira versão dos Termos de Uso e da Política de Privacidade**, mesmo provisória, para ter uma versão a gravar no aceite.

O código pode começar antes delas. Os pontos que dependem dessas ações são o texto da tela de termos, que entra por configuração, e o envio real de e-mails, que pode usar um provedor de teste no desenvolvimento.
