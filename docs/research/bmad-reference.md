# BMAD-METHOD reference (technical patterns only)

Analyzed: https://github.com/bmad-code-org/BMAD-METHOD, commit `e435a22574fe55722841086e5566420178b98df3` (2026-11-12, main, v7 preview; stable line is v6.12). Used ONLY as a pattern reference. Nothing from BMAD is installed or vendored.

## a) How an agent is defined
- An agent is a skill: a folder `skills/<module>/<skill>/` with `SKILL.md` (frontmatter `name` + `description`), `customize.toml`, optional `references/` and `scripts/`.
- `SKILL.md` body: Overview (persona), Conventions (`{skill-root}`, `{project-root}`), On Activation (resolve customization, prepend steps, adopt persona, load persistent facts, load config, greet).
- `customize.toml` `[agent]` keys: `name, title, icon, role, identity, communication_style, principles[], persistent_facts[], activation_steps_prepend/append[]`, and `[[agent.menu]]` entries (`code`, `description`, `skill`). Workflows use a `[workflow]` table instead.
- Overrides merge in order: skill defaults, team (`_bmad/custom/<skill>.toml`), personal (`<skill>.user.toml`). Scalars override, tables deep-merge, arrays append, arrays of tables keyed by `code`/`id` replace-or-append.
- The module manifest is `bmod.toml` (`[bmod]`: `code, version, update_source, skills, required_skills`; member skills carry `[skill]`). Confirmed name: `bmod.toml`.

## b) Workflows
- Workflows are skills too. Heavy logic lives in `references/*.md`, with helper `scripts/*.py`.
- Human checkpoints are expressed as instructions inside the skill (ask, wait), not as a separate engine.

## c) Lazy loading
- `SKILL.md` stays short; reference files are read just-in-time by the step that needs them (for example review lenses load their own reference only when that lens runs).
- `persistent_facts` support `file:` globs for standing context, loaded on activation only.

## d) Model routing
- No per-agent model routing found. Only advisory hints: `subagent_models` (ordered preference) in `bmad-deep-recon`, and "prefer faster cheaper models" for party-mode subagents.
- Our routing is therefore our own: `.claude/agents/*.md` with `model:` frontmatter.

## e) Skills worth adapting (recommendation only, phase 2)
| BMAD skill | Why | Cost |
|---|---|---|
| `bmad-review` (adversarial lens) | High value for tech-spec and story review | Low: lenses load on demand |
| `bmad-shard-pro` | Splitting large documents so agents load slices | Low |
| `bmad-build` flow (ticket-first, test-first) | Matches Termite PLAN to CODE TDD | Medium |

## Patterns adopted
- Agent = `SKILL.md` + `customize.toml`; persona and paths in TOML, logic in markdown.
- Just-in-time `references/` loading; `file:` globs for knowledge by `demandType`.
- Structural merge rules for overrides (not needed yet, kept as option).

## Patterns discarded
- Installer, `_bmad/` runtime tree, `uv` Python resolver scripts: too heavy; our `customize.toml` is read directly.
- `bmod.toml` manifest: we are a single repo, not a distributable module.
- Persona roleplay menus and party mode: low value per token for our three-agent flow.
