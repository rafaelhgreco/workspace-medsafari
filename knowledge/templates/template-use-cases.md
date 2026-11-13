# Template: Use cases

Section of `01-functional-stories.md`. Composed by Tiger; see `template-composition.md`.

<!--
FILL-IN INSTRUCTIONS (Tiger removes all HTML comments from the output)
- Simplified Cockburn format. One block per use case, IDs sequential: UC-01, UC-02, ...
- main flow: numbered steps, actor and system alternating.
- alternative flows: reference the main flow step they branch from (e.g. "3a").
- exceptions: failure paths and what the system does.
- related: every BR-xx and ST-xx the use case touches (feeds the traceability matrix).
- Field labels in English; text in `output_language`.
-->

## Use cases

### UC-01 <use case title>

- **Actor:** <primary actor>
- **Preconditions:** <what must be true before>
- **Postconditions:** <what is true after success>
- **Main flow:**
  1. <step>
- **Alternative flows:**
  - 1a. <branch>
- **Exceptions:**
  - E1. <failure and system response>
- **Related:** BR-xx, ST-xx

### Minimal example

### UC-01 Cancel an appointment

- **Actor:** Patient
- **Preconditions:** The patient has a scheduled appointment.
- **Postconditions:** The appointment is canceled and the slot is released.
- **Main flow:**
  1. The patient selects the appointment.
  2. The patient confirms the cancellation.
  3. The system cancels it and releases the slot.
- **Alternative flows:**
  - 2a. The patient gives up; nothing changes.
- **Exceptions:**
  - E1. Less than 24 hours before the start: the system refuses the cancellation.
- **Related:** BR-01, ST-01
