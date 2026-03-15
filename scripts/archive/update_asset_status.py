#!/usr/bin/env python3
"""Update one asset status across manifest, bibles, continuity plan, and director queue."""

from __future__ import annotations

import argparse

from _asset_ops import VALID_STATUSES, apply_asset_status, resolve_archive_dir


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Update one asset status across manifest, bibles, continuity plan, and director queue."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument("asset_id", help="Stable asset id such as CHAR_MENGJIANG or LOC_PUBLIC_DRAW_POOL_NIGHT")
    parser.add_argument("--status", required=True, choices=sorted(VALID_STATUSES))
    parser.add_argument("--path", help="Asset root path to record. Required when changing path.")
    parser.add_argument("--episode", default="ep001", help="Episode folder to update. Defaults to ep001.")
    parser.add_argument("--skip-render", action="store_true", help="Skip render/check after writing YAML.")
    args = parser.parse_args()

    archive_dir = resolve_archive_dir(args.project_or_archive_dir)
    changed_files = apply_asset_status(
        archive_dir,
        args.asset_id,
        args.status,
        raw_path=args.path,
        episode=args.episode,
        render=not args.skip_render,
    )

    print(f"Updated asset: {args.asset_id} -> {args.status}")
    if changed_files:
        print("Changed:")
        for path in changed_files:
            print(f"- {path}")
    else:
        print("No file changes were necessary.")


if __name__ == "__main__":
    main()
