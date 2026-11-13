# Step 03 - Epics, stories, tasks, acceptance criteria

Goal: append `## Epics and stories` to `delivery/01-functional-stories.md`, using `knowledge/templates/template-functional-history.md`.

## 1. Load
Read the template and the current `delivery/01-functional-stories.md`.

## 2. Structure
- Group related behavior into epics `EP-xx` (one epic is fine for a small demand).
- Each story `ST-xx`: "As a / I want / So that"; independently valuable and testable.
- Functional tasks `FT-xx` under each story: business behavior only, never technical work.
- Ids are sequential across the whole file (ST-01, ST-02 ...; FT-01 ...; AC-01 ...).

## 3. Acceptance criteria
- Gherkin, one scenario per observable behavior.
- Tag line above each scenario: `@AC-xx @BR-xx` (more than one BR tag allowed).
- Derive scenarios from the BRs: at least one happy path and, for every restrictive BR, one refusal/edge scenario.
- Keywords (Feature, Scenario, Given, When, Then, And) and tags in English; scenario text in `output_language`.

## 4. Coverage check (before writing)
- Every BR has at least one AC. If a BR has none, add a scenario or remove the BR.
- Every AC sits under exactly one story.

## 5. Write
Append to the file (file-operator or direct): `## Epics and stories`, with all HTML comments removed.

## Done when
Section appended, coverage check passes. Load `steps/step-04-use-cases.md`.
