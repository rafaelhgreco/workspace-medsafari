#!/usr/bin/env python3
"""Create development symlinks in repos/ from a JSON config.

Config (default: scripts/dev-repos.json):

    {
      "repos": {
        "medsafari": "~/Documentos/medsafari"
      }
    }

Each key becomes repos/<key>, a symlink pointing at the given path.
Relative paths are resolved against the config file's directory; "~" and
environment variables are expanded.

Usage:
    python3 scripts/link_dev_repos.py [--config FILE] [--dry-run] [--force] [--remove]
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent
WORKSPACE = SCRIPTS_DIR.parent
REPOS_DIR = WORKSPACE / "repos"
DEFAULT_CONFIG = SCRIPTS_DIR / "dev-repos.json"
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def load_config(path: Path) -> dict[str, Path]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"error: config not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"error: invalid JSON in {path}: {exc}")

    repos = data.get("repos") if isinstance(data, dict) else None
    if not isinstance(repos, dict) or not repos:
        sys.exit(f'error: {path} must contain a non-empty "repos" object')

    resolved: dict[str, Path] = {}
    for name, raw in repos.items():
        if not NAME_RE.match(name):
            sys.exit(f"error: invalid repo name: {name!r}")
        if not isinstance(raw, str) or not raw.strip():
            sys.exit(f"error: path for {name!r} must be a non-empty string")
        target = Path(os.path.expandvars(os.path.expanduser(raw)))
        if not target.is_absolute():
            target = path.parent / target
        resolved[name] = Path(os.path.abspath(target))
    return resolved


def link_one(name: str, target: Path, *, dry_run: bool, force: bool) -> bool:
    link = REPOS_DIR / name
    prefix = "[dry-run] " if dry_run else ""

    if not target.is_dir():
        print(f"SKIP   {name}: source is not a directory: {target}")
        return False

    if link.is_symlink():
        if Path(os.path.realpath(link)) == target.resolve():
            print(f"OK     {name} -> {target} (already linked)")
            return True
        if not force:
            print(f"SKIP   {name}: symlink points to {os.readlink(link)} (use --force)")
            return False
        print(f"{prefix}RELINK {name} (was {os.readlink(link)})")
        if not dry_run:
            link.unlink()
    elif link.exists():
        print(f"SKIP   {name}: {link} exists and is not a symlink (not touching it)")
        return False

    print(f"{prefix}LINK   {name} -> {target}")
    if not dry_run:
        REPOS_DIR.mkdir(exist_ok=True)
        os.symlink(target, link, target_is_directory=True)
    return True


def remove_one(name: str, *, dry_run: bool) -> bool:
    link = REPOS_DIR / name
    prefix = "[dry-run] " if dry_run else ""
    if not link.is_symlink():
        print(f"SKIP   {name}: not a symlink in repos/")
        return False
    print(f"{prefix}UNLINK {name}")
    if not dry_run:
        link.unlink()
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG, help="JSON config file")
    parser.add_argument("--dry-run", action="store_true", help="show actions without changing anything")
    parser.add_argument("--force", action="store_true", help="replace symlinks that point elsewhere")
    parser.add_argument("--remove", action="store_true", help="remove the configured symlinks instead")
    args = parser.parse_args()

    repos = load_config(args.config.resolve())
    if args.remove:
        results = [remove_one(n, dry_run=args.dry_run) for n in repos]
    else:
        results = [link_one(n, t, dry_run=args.dry_run, force=args.force) for n, t in repos.items()]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
