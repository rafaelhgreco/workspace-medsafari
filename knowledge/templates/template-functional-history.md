# Template: Epics, stories and functional tasks

Section of `01-functional-stories.md`. Composed by Tiger; see `template-composition.md`.

<!--
FILL-IN INSTRUCTIONS (Tiger removes all HTML comments from the output)
- Hierarchy: Epic EP-xx -> Story ST-xx -> Functional task FT-xx. IDs are sequential across the whole file.
- Story: "As a <actor>, I want <capability>, So that <benefit>".
- Functional tasks describe business behavior only (no technical tasks).
- Acceptance criteria: Gherkin. Each scenario has an ID tag `@AC-xx` and at least one `@BR-xx` tag naming the business rule it verifies. Every BR must be covered by at least one scenario.
- Keep keywords (Feature, Scenario, Given, When, Then, And) and tags in English; scenario text in `output_language`.
-->

## Epics and stories

### EP-01 <epic title>

<epic summary>

#### ST-01 <story title>

- As a <actor>
- I want <capability>
- So that <benefit>

**Functional tasks**
- FT-01 <functional task>

**Acceptance criteria**

```gherkin
@AC-01 @BR-01
Scenario: <scenario title>
  Given <context>
  When <action>
  Then <outcome>
```

### Minimal example

#### ST-01 Cancel an appointment

- As a patient
- I want to cancel my appointment
- So that the slot becomes available to others

**Functional tasks**
- FT-01 Allow cancellation up to 24 hours before the start.

```gherkin
@AC-01 @BR-01
Scenario: Cancel within the allowed window
  Given an appointment starting in 48 hours
  When the patient cancels it
  Then the appointment is canceled
```
