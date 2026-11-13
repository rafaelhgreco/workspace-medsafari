# Step 05 - Compose, validate, hand off

Goal: finish `delivery/01-functional-stories.md`, prove traceability, request the human review.

## 1. Load
Read `knowledge/templates/template-composition.md` and the whole current file.

## 2. Add the closing sections
- `## Traceability`: one row per AC `| BR | AC | UC | ST |`. UC = the use case whose `Related` lists both that BR and that ST, else `-`.
- `## Open questions`: one `OQ-xx` row for every `inferred` BR and every gap the human has not answered; `- None.` if empty.
- Section order must be: title+context, Business rules, Epics and stories, Use cases, Traceability, Open questions.

## 3. Validate (delegate commands to file-operator, judge the results yourself)
- `grep -n "<!--" <file>` returns nothing.
- Every BR appears in at least one Traceability row.
- Every AC appears exactly once and is linked to one ST.
- Every id cited (BR, AC, ST, UC) is defined in the file; each scenario tag pair matches its Traceability row.
- Fix every violation before continuing.

## 4. Update the demand
- Set `artifacts.delivery.functionalStories = "delivery/01-functional-stories.md"` (and refresh `artifacts.design` from `ls design/`).
- Transition `tiger_in_progress -> tiger_review` with a `history[]` entry (`by: "tiger"`).
- Run `[validation].command`.

## 5. Request review (human gate)
Show a short summary: counts of BR, EP, ST, FT, AC, UC, the open questions, and the file path. Ask: approve or request changes.
- Changes: edit the affected section, redo step-05 validation, ask again; keep the status `tiger_review`.
- Explicit approval: append `{stage:"tiger_review", approver, date}` to `approvals[]`, validate, then tell the human to run `/turtle <slug>`.
- Never record an approval the human did not give.
