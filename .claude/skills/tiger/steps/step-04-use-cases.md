# Step 04 - Use cases

Goal: append `## Use cases` (simplified Cockburn), using `knowledge/templates/template-use-cases.md`.

## 1. Load
Read the template and the current `delivery/01-functional-stories.md`.

## 2. Write the use cases
- One `UC-xx` per significant actor goal; at least one per epic.
- Fields: Actor, Preconditions, Postconditions, Main flow (numbered), Alternative flows (`2a.` style, referencing the main step), Exceptions (`E1.`), Related.
- `Related` lists every `BR-xx` and `ST-xx` the use case touches; each exception should map to a refusal/edge AC from step-03 (add the AC there if it is missing and note it).
- Keep flows at business level: no screens, endpoints or tables.

## 3. Append
Append `## Use cases` to the file (file-operator or direct), with all HTML comments removed.

## Done when
Section appended and every UC `Related` id exists. Load `steps/step-05-compose-handoff.md`.
