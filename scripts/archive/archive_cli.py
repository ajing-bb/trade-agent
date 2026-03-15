#!/usr/bin/env python3
"""Unified CLI entrypoint for project archive workflows."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


ARCHIVE_COMMANDS: dict[str, tuple[str, str]] = {
    "init": ("init_project_archive.py", "Initialize 项目档案 from a source DOCX."),
    "reset": ("reset_project_creation.py", "Reset project archive/assets back to a clean state."),
    "render": ("render_project_archive.py", "Render Markdown views from canonical YAML."),
    "check": ("check_asset_health.py", "Check canonical archive health and cross-file consistency."),
    "style": ("switch_project_style.py", "Switch project style presets such as 2d/3d."),
    "prompts": ("generate_project_prompts.py", "Generate prompt pack YAML from canonical bibles."),
    "queue": ("generate_director_queue.py", "Generate continuity shot_build_policy and director queue."),
    "runbook": ("generate_batch_runbook.py", "Generate batch execution/prompt markdown files."),
    "status": ("update_asset_status.py", "Update one asset status across manifest, bibles, and queue."),
    "ingest": ("ingest_generated_assets.py", "Batch-ingest generated files and mark assets as committed."),
    "sync": ("sync_project_archive.py", "Run the full repo-internal archive sync pipeline."),
}


def script_path(script_name: str) -> Path:
    return Path(__file__).resolve().parent / script_name


def forward_to_script(command: str, forwarded_args: list[str]) -> int:
    script_name, _ = ARCHIVE_COMMANDS[command]
    completed = subprocess.run([sys.executable, str(script_path(script_name)), *forwarded_args], check=False)
    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Unified CLI for project archive workflows under scripts/."
    )
    subparsers = parser.add_subparsers(dest="command")
    for command, (_, help_text) in ARCHIVE_COMMANDS.items():
        subparser = subparsers.add_parser(command, add_help=False, help=help_text, description=help_text)
        subparser.add_argument("args", nargs=argparse.REMAINDER)
    return parser


def main(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if argv and argv[0] in ARCHIVE_COMMANDS and any(flag in {"-h", "--help"} for flag in argv[1:]):
        return forward_to_script(argv[0], argv[1:])

    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.command:
        parser.print_help()
        return 0

    forwarded_args = list(args.args)
    return forward_to_script(args.command, forwarded_args)


if __name__ == "__main__":
    raise SystemExit(main())
