#!/usr/bin/env python3
"""Batch-ingest generated asset files and mark matching assets as committed."""

from __future__ import annotations

import argparse
from pathlib import Path

from _asset_ops import apply_asset_status, load_yaml, render_and_check, resolve_archive_dir


IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
STRICT_KEYWORDS = ("final", "master", "select")


def candidate_images(asset_root: Path) -> list[Path]:
    return sorted(
        path
        for path in asset_root.iterdir()
        if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
    )


def select_image(paths: list[Path]) -> tuple[str, Path | None]:
    if not paths:
        return "empty_dir", None
    if len(paths) == 1:
        return "selected", paths[0]
    strict_matches = [
        path for path in paths if any(keyword in path.stem.lower() for keyword in STRICT_KEYWORDS)
    ]
    if len(strict_matches) == 1:
        return "selected", strict_matches[0]
    return "ambiguous", None


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scan asset directories and batch-mark eligible assets as committed."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument("--episode", default="ep001", help="Episode folder to update. Defaults to ep001.")
    parser.add_argument("--only", nargs="+", help="Only ingest the listed asset ids.")
    parser.add_argument("--dry-run", action="store_true", help="Preview ingest results without writing YAML.")
    args = parser.parse_args()

    archive_dir = resolve_archive_dir(args.project_or_archive_dir)
    repo_root = archive_dir.parent.parent.parent
    manifest_path = archive_dir / "episodes" / args.episode / "asset-manifest.yaml"
    manifest = load_yaml(manifest_path)

    committed: list[tuple[str, Path, str]] = []
    skipped: list[tuple[str, str, str]] = []
    changed_paths: set[Path] = set()

    only_ids = set(args.only or [])
    for item in manifest.get("assets", []):
        item_type = item.get("type")
        if item_type not in {"character", "scene", "prop", "vfx"}:
            continue
        if only_ids and item["id"] not in only_ids:
            continue
        if item.get("status") == "committed":
            continue
        raw_path = item.get("path")
        if not raw_path:
            skipped.append((item["id"], "missing_path", ""))
            continue

        asset_root = Path(raw_path)
        if not asset_root.is_absolute():
            asset_root = (repo_root / asset_root).resolve()
        if not asset_root.exists():
            skipped.append((item["id"], "missing_dir", raw_path))
            continue
        if not asset_root.is_dir():
            skipped.append((item["id"], "not_dir", raw_path))
            continue

        state, selected = select_image(candidate_images(asset_root))
        if state != "selected" or selected is None:
            skipped.append((item["id"], state, raw_path))
            continue

        committed.append((item["id"], selected, raw_path))
        if not args.dry_run:
            for changed in apply_asset_status(
                archive_dir,
                item["id"],
                "committed",
                raw_path=raw_path,
                episode=args.episode,
                render=False,
            ):
                changed_paths.add(changed)

    if committed and not args.dry_run:
        render_and_check(archive_dir)

    mode = "Dry run" if args.dry_run else "Committed"
    print(f"{mode}: {len(committed)} asset(s)")
    for asset_id, selected, raw_path in committed:
        print(f"- {asset_id}: {selected} -> {raw_path}")

    if skipped:
        print("Skipped:")
        for asset_id, reason, raw_path in skipped:
            suffix = f" ({raw_path})" if raw_path else ""
            print(f"- {asset_id}: {reason}{suffix}")

    if changed_paths:
        print("Changed:")
        for path in sorted(changed_paths):
            print(f"- {path}")


if __name__ == "__main__":
    main()
