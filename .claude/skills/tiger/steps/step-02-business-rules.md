# Step 02 - Business rules

Goal: list the business rules as `BR-xx`, using `knowledge/templates/template-work-rules.md`.

## 1. Load
- Read the template (its HTML comments are the fill-in rules) and, if present, the `## Quick rules` of `knowledge/guides/commons/` guides that mention business rules.

## 2. Draft the rules
- One row per rule, ids `BR-01`, `BR-02`, ... sequential.
- Rule: one declarative, testable sentence, no implementation detail.
- Rationale: the business reason.
- Source: `demand` (stated in the demand), `human answer` (from step-01), or `inferred`.
- Prefer fewer sharp rules over many vague ones; split a rule that mixes two conditions.
- Every `inferred` rule must also become an Open question in step-05.

## 3. Write the file (delegate to file-operator, or write directly)
Create `artifacts/active/<slug>/delivery/01-functional-stories.md` with:
1. `# <title>` (in `output_language`)
2. One context line: `Demand <id> · <date>.` plus a one-paragraph summary.
3. `## Business rules` and the table, with all HTML comments removed.

Headings, IDs and the `source` values stay in English; the cell text uses `output_language`.

## Done when
The file exists with the Business rules section and no `<!--`. Load `steps/step-03-stories.md`.
