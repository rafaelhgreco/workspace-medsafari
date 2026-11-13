# Template: Composition of 01-functional-stories.md

Tiger composes ONE file, `delivery/01-functional-stories.md`, from the three section templates. Remove all HTML comments from the output.

<!--
Rules
- Section order is fixed (below). Do not add sections.
- IDs (BR/EP/ST/FT/AC/UC), tags and these headings stay in English; body text uses `output_language`.
- Open questions: anything marked `inferred` in business rules, plus every gap the human has not answered.
-->

## Section order

1. `# <Story title>` plus one-paragraph context (status line: demand id, date)
2. `## Business rules` (from `template-work-rules.md`)
3. `## Epics and stories` (from `template-functional-history.md`)
4. `## Use cases` (from `template-use-cases.md`)
5. `## Traceability`
6. `## Open questions`

## Traceability

Matrix with one row per acceptance criterion. Rules: every BR appears in at least one row; every AC appears exactly once; UC may be empty (`-`) when no use case covers the row.

| BR | AC | UC | ST |
|---|---|---|---|
| BR-01 | AC-01 | UC-01 | ST-01 |

## Open questions

| ID | Question | Related | Status |
|---|---|---|---|
| OQ-01 | <question> | BR-xx | open / answered |

Use `- None.` when there are no open questions.
