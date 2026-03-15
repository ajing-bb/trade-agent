#!/usr/bin/env python3
"""Generate batch prompt and execution markdown from canonical prompt packs and queue."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def dump_text(path: Path, text: str) -> None:
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def resolve_archive_dir(target: str) -> Path:
    path = Path(target).resolve()
    archive_dir = path if path.name == "项目档案" else path / "项目档案"
    if not archive_dir.exists():
        raise FileNotFoundError(f"Archive directory does not exist: {archive_dir}")
    return archive_dir


def collect_prompt_items(series_dir: Path) -> dict[str, dict[str, Any]]:
    records: dict[str, dict[str, Any]] = {}
    for file_name, section_name in (
        ("character-asset-prompt-pack.yaml", "characters"),
        ("scene-asset-prompt-pack.yaml", "locations"),
        ("prop-vfx-asset-prompt-pack.yaml", "props"),
        ("prop-vfx-asset-prompt-pack.yaml", "vfx"),
    ):
        data = load_yaml(series_dir / file_name)
        for item in data.get(section_name, []):
            records[item["id"]] = item
    return records


def output_name(prompt_name: str) -> str:
    return f"{prompt_name.replace('_', '-')}-v001.png"


def batch_assets(prompt_items: dict[str, dict[str, Any]], queue: dict[str, Any], batch_size: int) -> list[dict[str, Any]]:
    usage = Counter()
    for shot in queue.get("queue", []):
        for asset_id in shot.get("blocked_by_assets", []):
            usage[asset_id] += 1
    candidates = [
        item for item in prompt_items.values() if item.get("status") in {"planned", "prompted"}
    ]
    candidates.sort(key=lambda item: (-usage[item["id"]], item["id"]))
    return candidates[:batch_size]


def generate_execution_md(batch_id: str, assets: list[dict[str, Any]], queue: dict[str, Any]) -> str:
    lines = [f"# {batch_id} Execution", "", "## Asset Order", ""]
    lines.append("| Order | Asset ID | Tool | Prompt Source | Recommended Output |")
    lines.append("| --- | --- | --- | --- | --- |")
    order = 1
    unlocks: dict[str, list[str]] = {item["id"]: [] for item in assets}
    selected_ids = set(unlocks)
    for shot in queue.get("queue", []):
        for asset_id in shot.get("blocked_by_assets", []):
            if asset_id in selected_ids:
                unlocks[asset_id].append(shot["shot_id"])
    for item in assets:
        for tool_name, prompt_map in (("Midjourney", item.get("midjourney", {})), ("Banana Pro", item.get("banana", {}))):
            for prompt_name in prompt_map:
                lines.append(
                    f"| {order} | `{item['id']}` | {tool_name} | `{item['id']} -> {prompt_name}` | "
                    f"`{item.get('target_path', 'missing')}/{output_name(prompt_name)}` |"
                )
                order += 1
    lines.extend(["", "## Unlock Map", "", "| Asset | Unblocks |", "| --- | --- |"])
    for item in assets:
        lines.append(f"| `{item['id']}` | {', '.join(unlocks[item['id']]) or '-'} |")
    return "\n".join(lines)


def generate_prompts_md(batch_id: str, assets: list[dict[str, Any]]) -> str:
    lines = [f"# {batch_id} Prompts", ""]
    for item in assets:
        lines.extend(["", f"## `{item['id']}`", ""])
        target_path = item.get("target_path", "missing")
        for tool_name, prompt_map in (("Midjourney", item.get("midjourney", {})), ("Banana Pro", item.get("banana", {}))):
            if not prompt_map:
                continue
            lines.extend([f"### {tool_name}", ""])
            for prompt_name, prompt in prompt_map.items():
                lines.extend(
                    [
                        f"#### `{prompt_name}`",
                        "",
                        f"建议输出：`{target_path}/{output_name(prompt_name)}`",
                        "",
                        "```text",
                        prompt,
                        "```",
                        "",
                    ]
                )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate batch execution/prompt markdown from canonical prompt packs and queue."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument("--episode", default="ep001", help="Episode folder to update. Defaults to ep001.")
    parser.add_argument("--batch-id", default="Batch-01", help="Batch label used in output filenames and headings.")
    parser.add_argument("--batch-size", type=int, default=5, help="Maximum number of asset ids to include.")
    parser.add_argument("--only", nargs="+", help="Only include the listed asset ids.")
    parser.add_argument("--dry-run", action="store_true", help="Preview output paths and selected assets without writing.")
    args = parser.parse_args()

    archive_dir = resolve_archive_dir(args.project_or_archive_dir)
    series_dir = archive_dir / "series"
    episode_dir = archive_dir / "episodes" / args.episode
    queue = load_yaml(episode_dir / "director-queue.yaml")
    prompt_items = collect_prompt_items(series_dir)
    assets = batch_assets(prompt_items, queue, args.batch_size)
    if args.only:
        selected = set(args.only)
        assets = [item for item in assets if item["id"] in selected]

    slug = args.batch_id.lower().replace(" ", "-")
    execution_path = episode_dir / f"{slug}-execution.md"
    prompts_path = episode_dir / f"{slug}-prompts.md"
    if args.dry_run:
        print(f"Dry run execution path: {execution_path}")
        print(f"Dry run prompts path: {prompts_path}")
        print("Selected assets:")
        for item in assets:
            print(f"- {item['id']}")
        return
    dump_text(execution_path, generate_execution_md(args.batch_id, assets, queue))
    dump_text(prompts_path, generate_prompts_md(args.batch_id, assets))
    print(f"Generated: {execution_path}")
    print(f"Generated: {prompts_path}")


if __name__ == "__main__":
    main()
