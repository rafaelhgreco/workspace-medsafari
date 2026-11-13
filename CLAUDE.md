# Agentic repository

Purpose: Tiger (product) -> Turtle (architect) -> Termite (developer) workflow for feature delivery. All agent/skill/schema/guide files are in English; human-facing deliverables follow `output_language` in `customize.toml` (default pt-BR).

## Map
- `.claude/agents/` model-routing subagents; `.claude/skills/{tiger,turtle,termite}` the three agents (invoked as `/tiger`, `/turtle`, `/termite`); `.claude/hooks/` RTK hook
- `repos/<name>/` independent code repos (git-ignored)
- `artifacts/active/<story>/{delivery,design,demand-context.json}`; `artifacts/archive/`
- `knowledge/guides/{commons,backend,database,frontend}`, `knowledge/templates`, `knowledge/repositories/<repo>/graphify-out`
- `schemas/demand-context.schema.json`; `docs/`; `skills-lock.md`

## Flow and gates
Tiger -> human review -> Turtle (+ branches) -> human review -> Termite (PLAN -> CODE TDD -> VERIFY) -> manual graphify request -> done.
Human approval is mandatory between agents. Termite also pauses after PLAN and after VERIFY (approvals `termite_plan`, `termite_verify`). Status machine is in the schema: created, tiger_in_progress, tiger_review, turtle_in_progress, turtle_review, termite_plan, termite_code, termite_verify, awaiting_graphify, done, archived.

## Model routing
- Manual work (create, move, rename, edit files, scaffolding, verification commands, git ops): `file-operator` (haiku).
- Reasoning (investigation, analysis, architecture, review): `deep-thinker` (sonnet). Project default model is sonnet.
- Use aliases only, never fixed model IDs.

## Branches and commits
- Turtle creates `<type>/<slug>` in every affected repo; type in feat|fix|refactor|chore|docs|test|perf|build|ci, slug `[a-z0-9-]+`.
- Termite commits follow Conventional Commits.

## Graphify (manual)
At the end of VERIFY, Termite asks the human to run graphify on the changed repos and moves the demand to `done` only after confirmation.

## Shell
Shell commands pass through the RTK hook; see docs/research/rtk-setup.md. Prefer shell for bulk reads.

## Knowledge (lazy loading)
Load `knowledge/guides/commons/` always, plus guides for the demand's `demandType` (backend|frontend|database|fullstack) only.

## Naming
Deliverables in `delivery/`: `01-functional-stories.md`, `02-tech-spec.md`, `03-implementation-plan.md`, `04-verification-report.md`. After `done`, move `artifacts/active/<story>/` to `artifacts/archive/<story>/`.
