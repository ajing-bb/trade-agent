#!/usr/bin/env python3
"""Run the repo-internal archive generation pipeline in one command."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def run(script: str, *args: str) -> None:
    scripts_dir = Path(__file__).resolve().parent
    script_path = scripts_dir / script
    subprocess.run([sys.executable, str(script_path), *args], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Sync prompt packs, queue, runbook, and rendered markdown for one episode."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument("--episode", default="ep001", help="Episode folder to sync. Defaults to ep001.")
    parser.add_argument("--batch-id", default="Batch-01", help="Batch label for generated runbook files.")
    parser.add_argument("--batch-size", type=int, default=5, help="Maximum number of asset ids in generated batch docs.")
    parser.add_argument("--only", nargs="+", help="Limit generation to listed asset ids where supported.")
    parser.add_argument("--skip-existing-prompts", action="store_true", help="Do not overwrite already existing prompt entries.")
    parser.add_argument("--dry-run", action="store_true", help="Run all generation steps in preview mode.")
    args = parser.parse_args()

    prompt_args = [args.project_or_archive_dir, "--episode", args.episode]
    queue_args = [args.project_or_archive_dir, "--episode", args.episode]
    runbook_args = [
        args.project_or_archive_dir,
        "--episode",
        args.episode,
        "--batch-id",
        args.batch_id,
        "--batch-size",
        str(args.batch_size),
    ]

    if args.only:
        prompt_args.extend(["--only", *args.only])
        runbook_args.extend(["--only", *args.only])
    if args.skip_existing_prompts:
        prompt_args.append("--skip-existing")
    if args.dry_run:
        prompt_args.append("--dry-run")
        queue_args.append("--dry-run")
        runbook_args.append("--dry-run")
    else:
        prompt_args.append("--render")
        queue_args.append("--render")

    run("generate_project_prompts.py", *prompt_args)
    run("generate_director_queue.py", *queue_args)
    run("generate_batch_runbook.py", *runbook_args)
    if not args.dry_run:
        run("check_asset_health.py", args.project_or_archive_dir)


if __name__ == "__main__":
    main()
