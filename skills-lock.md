# skills-lock

Human-readable registry. The `skills` CLI also maintains `skills-lock.json` (machine-readable hashes); do not edit it by hand.

| Skill | Origin | Version / commit | Date | Reason |
|---|---|---|---|---|
| writing-plans | https://github.com/obra/superpowers (vendored) | 22f0b463e7a5e579904dd6211a520321035526f7 (v7.0.2) | 2026-11-13 | Plan writing for Termite PLAN. Default output `docs/superpowers/plans/YYYY-MM-DD-<feature>.md` (to redirect to `artifacts/active/<story>/delivery/` in phase 2) |
| test-driven-development | same | same | 2026-11-13 | Termite CODE (TDD) |
| verification-before-completion | same | same | 2026-11-13 | Termite VERIFY |
| design-taste-frontend | `npx skills add Leonxlnx/taste-skill` | see skills-lock.json (hash b10eab0a...) | 2026-11-13 | Frontend design quality. Note: about 39 MB of assets |
| web-design-guidelines | `npx skills add vercel-labs/agent-skills@web-design-guidelines` | see skills-lock.json (hash 4f68ae07...) | 2026-11-13 | UI review against Web Interface Guidelines |

Superpowers license: `.claude/skills/SUPERPOWERS-LICENSE`.
Known soft dependencies NOT vendored (referenced by name in the vendored skills): `superpowers:subagent-driven-development`, `superpowers:executing-plans`, `superpowers:using-git-worktrees`, `superpowers:writing-skills`.

## Tooling

| Tool | Origin | Version | Date | Reason |
|---|---|---|---|---|
| rtk | https://github.com/rtk-ai/rtk (winget `rtk-ai.rtk`) | 1.2.0 | 2026-11-13 | Compress shell command output; project-scoped hook. See docs/research/rtk-setup.md |
