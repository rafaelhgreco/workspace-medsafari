# Cancelamento de agendamento (exemplo)

Demanda EXAMPLE-001 · 2026-11-13. Fixture de exemplo composta pelos templates do Tiger.

## Business rules

| ID | Rule | Rationale | Source |
|---|---|---|---|
| BR-01 | Um agendamento só pode ser cancelado até 24 horas antes do início. | Evitar horários que não podem ser reocupados. | demand |
| BR-02 | Ao cancelar, o horário volta a ficar disponível imediatamente. | Permitir novo agendamento por outros pacientes. | human answer |
| BR-03 | O paciente recebe uma confirmação do cancelamento. | Dar certeza de que o cancelamento foi registrado. | inferred |

## Epics and stories

### EP-01 Gestão de agendamentos

Permitir que o paciente gerencie seus próprios agendamentos.

#### ST-01 Cancelar um agendamento

- As a paciente
- I want cancelar meu agendamento
- So that o horário fique disponível para outras pessoas

**Functional tasks**
- FT-01 Permitir o cancelamento até 24 horas antes do início.
- FT-02 Recusar o cancelamento fora da janela permitida.
- FT-03 Liberar o horário ao cancelar.

**Acceptance criteria**

```gherkin
@AC-01 @BR-01
Scenario: Cancelar dentro da janela permitida
  Given um agendamento que começa em 48 horas
  When o paciente cancela o agendamento
  Then o agendamento é cancelado

@AC-02 @BR-01
Scenario: Recusar cancelamento fora da janela
  Given um agendamento que começa em 2 horas
  When o paciente tenta cancelar o agendamento
  Then o cancelamento é recusado com uma mensagem explicativa

@AC-03 @BR-02
Scenario: Liberar o horário
  Given um agendamento cancelado
  When outro paciente consulta os horários disponíveis
  Then o horário cancelado aparece como disponível
```

#### ST-02 Receber confirmação do cancelamento

- As a paciente
- I want receber uma confirmação do cancelamento
- So that eu tenha certeza de que ele foi registrado

**Functional tasks**
- FT-04 Enviar a confirmação ao paciente após o cancelamento.

**Acceptance criteria**

```gherkin
@AC-04 @BR-03
Scenario: Confirmar o cancelamento
  Given um agendamento cancelado com sucesso
  When o cancelamento é registrado
  Then o paciente recebe uma confirmação
```

## Use cases

### UC-01 Cancelar um agendamento

- **Actor:** Paciente
- **Preconditions:** O paciente possui um agendamento marcado.
- **Postconditions:** O agendamento está cancelado, o horário liberado e a confirmação enviada.
- **Main flow:**
  1. O paciente seleciona o agendamento.
  2. O paciente confirma o cancelamento.
  3. O sistema cancela o agendamento e libera o horário.
  4. O sistema envia a confirmação ao paciente.
- **Alternative flows:**
  - 2a. O paciente desiste; nada é alterado.
- **Exceptions:**
  - E1. Faltam menos de 24 horas para o início: o sistema recusa o cancelamento e explica o motivo.
- **Related:** BR-01, BR-02, BR-03, ST-01, ST-02

## Traceability

| BR | AC | UC | ST |
|---|---|---|---|
| BR-01 | AC-01 | UC-01 | ST-01 |
| BR-01 | AC-02 | UC-01 | ST-01 |
| BR-02 | AC-03 | UC-01 | ST-01 |
| BR-03 | AC-04 | UC-01 | ST-02 |

## Open questions

| ID | Question | Related | Status |
|---|---|---|---|
| OQ-01 | A confirmação deve ser enviada por e-mail, SMS ou ambos? (BR-03 foi inferida) | BR-03 | open |
