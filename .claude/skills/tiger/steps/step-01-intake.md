# Step 01 - Intake

Goal: understand the demand, close real gaps, then create the demand folder and `demand-context.json`.

## 1. Read the demand
- The input is the user's text, a file path, or a ticket reference. Read files with Read.
- If the demand is empty or unreadable, ask for it and stop.

## 2. Slug and id
- slug: kebab-case from the title, `[a-z0-9-]+`, at most 40 chars.
- id: the ticket id if the human gave one, otherwise `DEM-<YYYYMMDD>-<slug>`.
- Collision: if `artifacts/active/<slug>` or `artifacts/archive/<slug>` exists, ask: resume it or use another slug.

## 3. Gap analysis (reasoning, do not skip)
Check what the demand does NOT say about:
- actors and the goal of each;
- scope and explicit out-of-scope;
- business limits (amounts, time windows, quotas, permissions);
- error and edge cases the business cares about;
- notifications or side effects visible to the user;
- `demandType` (see below) and target repositories;
- UI inputs, only if the demand has a frontend part.

## 4. One grouped round of questions
- Maximum `[intake].max_questions` numbered questions, only for real gaps.
- Each question carries a proposed default so the human can answer "default".
- Include: `demandType` proposal, target repositories (list `repos/` with `ls repos/`), and for frontend or fullstack: ask the human to drop screenshots, Figma links or references into `design/`.
- Wait for the answers. Do not ask a second round unless an answer contradicts the demand.
- Keep answers as facts; later BR rows cite them as `human answer`.

## 5. demandType
| Value | Meaning |
|---|---|
| `backend` | Rust/Axum repo only |
| `frontend` | Angular repo only |
| `database` | schema/migrations only |
| `fullstack` | more than one of the above |

## 6. Create the demand (delegate to file-operator)
1. `mkdir -p artifacts/active/<slug>/delivery artifacts/active/<slug>/design`.
2. Write `artifacts/active/<slug>/demand-context.json`:
   - `id`, `slug`, `title`, `createdAt` (now), `demandType`;
   - `targetRepositories[]`: `{name, path: "repos/<name>", graphifyPath: "knowledge/repositories/<name>/graphify-out"}`;
   - `branches: []`, `approvals: []`, `verifyRetries: 0`;
   - `graphify: {requestedAt: null, repos: [], confirmedBy: null, confirmedAt: null}`;
   - `artifacts: {delivery: {}, design: []}` (list files already in `design/` as `design/<file>`);
   - `status: "tiger_in_progress"`;
   - `history`: `{from:null,to:"created",...}` then `{from:"created",to:"tiger_in_progress",by:"tiger",...}`.
3. Run `[validation].command` with the new file; it must print `valid`.
4. If a `repos/<name>` folder is missing, warn the human (they must clone it before /turtle); do not block.

## Done when
The file validates, status is `tiger_in_progress`, and the answers are in hand. Load `steps/step-02-business-rules.md`.
