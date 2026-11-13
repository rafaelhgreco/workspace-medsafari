#!/usr/bin/env bash
# Fail-open RTK PreToolUse hook (project scope). If rtk is missing, do nothing so the original command runs.
command -v rtk >/dev/null 2>&1 || exit 0
exec rtk hook claude
