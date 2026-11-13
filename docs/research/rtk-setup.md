# RTK (Rust Token Killer) setup

Project: https://github.com/rtk-ai/rtk. Never `cargo install rtk` from crates.io (that is "Rust Type Kit", a different package).

- Installed version: 1.2.0 (winget `rtk-ai.rtk`, 2026-11-13).
- Install on a new machine: Windows `winget install rtk-ai.rtk`; macOS/Linux `brew install rtk`; or `cargo install --git https://github.com/rtk-ai/rtk`. Restart the shell so PATH updates.
- Verify: `rtk --version` and `rtk gain` (must print a savings dashboard, not "command not found").
- Project integration: `.claude/hooks/rtk-rewrite.sh` is a fail-open wrapper around the native `rtk hook claude` command, registered as PreToolUse (matcher `Bash`) in `.claude/settings.json`. If `rtk` is not installed, the script exits 0 silently and the original command runs.
- Do not run `rtk init -g`: it writes `~/.claude/RTK.md` and `~/.claude/CLAUDE.md`, even with `--no-patch`. We keep everything project-scoped.
- Limitation: Read, Grep and Glob tools do not pass through the hook. Prefer shell (`ls`, `grep`, `git`) for bulk reads and listings.
