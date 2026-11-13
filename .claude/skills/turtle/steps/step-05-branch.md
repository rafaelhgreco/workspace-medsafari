# Step 05 - Create branches and hand off

Goal: create `<type>/<slug>` in each affected repository, record it, and move to Termite. Runs only after `approvals[]` contains `stage: "turtle_review"`.

## 1. Preconditions
- Status `turtle_review` and the `turtle_review` approval present. Otherwise stop.
- Branch name `<type>/<slug>` comes from the spec header; check it against `[branch].pattern`. Invalid -> stop and fix the spec.
- Affected repositories: those named in the Work decomposition table (subset of `targetRepositories`).

## 2. For each affected repo (delegate to file-operator, one repo at a time, report raw output)
1. `git -C repos/<name> status --porcelain` must be empty; otherwise STOP and report.
2. Default branch: `git -C repos/<name> symbolic-ref --short refs/remotes/origin/HEAD` (strip `origin/`); fallback `main`, then `master`.
3. `git -C repos/<name> fetch origin`, `checkout <default>`, `pull --ff-only`.
4. If `<type>/<slug>` already exists locally or on origin: STOP and ask the human.
5. `git -C repos/<name> checkout -b <type>/<slug>`.
6. Stop on the first failing command; never force anything.

## 3. Record
- Append to `branches[]` for each repo: `{repo, name, type, createdBy: "turtle", createdAt}`.
- Transition `turtle_review -> termite_plan` (history, `by: "turtle"`).
- Run `[validation].command`.

## 4. Handoff
Report the repos and branches created and tell the human to run `/termite <slug>`.
