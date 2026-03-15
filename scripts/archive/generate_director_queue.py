#!/usr/bin/env python3
"""Generate continuity shot_build_policy and director queue from breakdown + manifest."""

from __future__ import annotations

import argparse
import subprocess
import sys
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


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)


def resolve_archive_dir(target: str) -> Path:
    path = Path(target).resolve()
    archive_dir = path if path.name == "项目档案" else path / "项目档案"
    if not archive_dir.exists():
        raise FileNotFoundError(f"Archive directory does not exist: {archive_dir}")
    return archive_dir


def render_archive(archive_dir: Path) -> None:
    render_script = Path(__file__).with_name("render_project_archive.py")
    subprocess.run([sys.executable, str(render_script), str(archive_dir)], check=True)


def load_asset_lookup(manifest: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]]:
    by_id = {item["id"]: item for item in manifest.get("assets", [])}
    by_type: dict[str, list[dict[str, Any]]] = {}
    for item in manifest.get("assets", []):
        by_type.setdefault(item.get("type", ""), []).append(item)
    return by_id, by_type


def norm(text: str) -> str:
    return text.strip().lower().replace(" ", "")


def build_asset_name_catalog(archive_dir: Path, manifest: dict[str, Any]) -> dict[str, str]:
    catalog: dict[str, str] = {}
    for path, section in (
        (archive_dir / "series" / "character-bible.yaml", "characters"),
        (archive_dir / "series" / "scene-bible.yaml", "locations"),
        (archive_dir / "series" / "prop-vfx-bible.yaml", "props"),
        (archive_dir / "series" / "prop-vfx-bible.yaml", "vfx"),
    ):
        data = load_yaml(path)
        for item in data.get(section, []):
            item_id = item.get("id")
            name = item.get("name")
            if item_id and isinstance(name, str) and name:
                catalog[item_id] = name
    for item in manifest.get("assets", []):
        catalog.setdefault(item["id"], Path(item.get("path", "")).name)
    return catalog


def candidate_asset_ids(
    required_assets: list[str],
    shot_characters: list[str],
    manifest: dict[str, Any],
    asset_names: dict[str, str],
) -> list[str]:
    by_id, _ = load_asset_lookup(manifest)
    candidates: list[str] = []

    def maybe_add(raw_text: str) -> None:
        raw_norm = norm(raw_text)
        if not raw_norm:
            return
        for asset_id, asset_name in asset_names.items():
            if asset_id not in by_id or asset_id in candidates:
                continue
            name_norm = norm(asset_name)
            if raw_norm == name_norm or raw_norm in name_norm or name_norm in raw_norm:
                candidates.append(asset_id)
    for character in shot_characters:
        maybe_add(character)
    for raw in required_assets:
        maybe_add(raw)
    return candidates


def infer_build_method(shot: dict[str, Any], blocked_by_assets: list[str]) -> str:
    flags = set(shot.get("review_flags", []))
    dialogue = bool(shot.get("dialogue"))
    characters = shot.get("characters", [])
    if "strong_vfx" in flags:
        if any(asset_id.startswith("VFX_") for asset_id in blocked_by_assets):
            return "scene_plate + vfx_pass"
        return "scene_plate + effect_overlay"
    if any(asset_id.startswith("PROP_") for asset_id in blocked_by_assets) and not characters:
        return "prop_insert_close_up"
    if dialogue and len(characters) >= 2:
        return "dialogue_two_shot"
    if dialogue and len(characters) == 1:
        return "character_close_medium"
    if any(asset_id.startswith("CHAR_") for asset_id in blocked_by_assets) and any(asset_id.startswith("LOC_") for asset_id in blocked_by_assets):
        return "scene_master + character_composite"
    if any(asset_id.startswith("LOC_") for asset_id in blocked_by_assets):
        return "scene_master_first"
    return "manual_design"


def infer_priority_score(shot: dict[str, Any], blocked_by_assets: list[str]) -> int:
    score = 0
    if "high_difficulty" not in shot.get("review_flags", []):
        score += 3
    if shot.get("difficulty") == "low":
        score += 2
    if "strong_vfx" in shot.get("review_flags", []):
        score -= 2
    if "many_characters" in shot.get("review_flags", []):
        score -= 2
    if "lip_sync_high" in shot.get("review_flags", []):
        score -= 1
    if any(asset_id.startswith("CHAR_") for asset_id in blocked_by_assets):
        score += 2
    if any(asset_id.startswith("LOC_") for asset_id in blocked_by_assets):
        score += 1
    return score


def primary_refs_for_shot(shot: dict[str, Any], blocked_by_assets: list[str]) -> list[str]:
    refs: list[str] = []
    for asset_id in blocked_by_assets:
        if asset_id.startswith("CHAR_"):
            refs.append(f"{asset_id} face/full body master")
        elif asset_id.startswith("LOC_"):
            refs.append(f"{asset_id} scene master")
        elif asset_id.startswith("PROP_") or asset_id.startswith("CARD_"):
            refs.append(f"{asset_id} master")
        elif asset_id.startswith("VFX_"):
            refs.append(f"{asset_id} keyframe")
    return refs or ["manual canonical design"]


def next_action_for_shot(queue_status: str, shot: dict[str, Any], blocked_by_assets: list[str]) -> str:
    if queue_status == "ready":
        return f"按 {infer_build_method(shot, blocked_by_assets)} 先做首帧/静帧，再决定是否进入视频段。"
    if blocked_by_assets:
        return f"先补齐 {', '.join(blocked_by_assets)}，再执行该镜头。"
    return "人工确认缺失的 canonical 资产绑定。"


def fallback_for_shot(shot: dict[str, Any]) -> str:
    flags = set(shot.get("review_flags", []))
    if "strong_vfx" in flags:
        return "先做无特效稳定 plate，后续分层补特效。"
    if "many_characters" in flags:
        return "先缩小景别或拆成单人/双人镜头，再回补群像。"
    if shot.get("dialogue"):
        return "先做静帧对白 keyframe，不直接上长对白视频。"
    return "先做更稳的中景版本，再回补复杂机位。"


def generate_queue_and_policy(archive_dir: Path, episode: str) -> tuple[dict[str, Any], dict[str, Any]]:
    episode_dir = archive_dir / "episodes" / episode
    breakdown = load_yaml(episode_dir / "breakdown.yaml")
    continuity = load_yaml(episode_dir / "continuity-plan.yaml")
    director_queue = load_yaml(episode_dir / "director-queue.yaml")
    manifest = load_yaml(episode_dir / "asset-manifest.yaml")
    manifest_by_id, _ = load_asset_lookup(manifest)
    asset_names = build_asset_name_catalog(archive_dir, manifest)

    policies: list[dict[str, str]] = []
    queue: list[dict[str, Any]] = []
    skipped_count = 0

    shots = breakdown.get("shots", [])
    ranked = []
    for shot in shots:
        blocked_by_assets = [
            asset_id
            for asset_id in candidate_asset_ids(
                shot.get("required_assets", []),
                shot.get("characters", []),
                manifest,
                asset_names,
            )
            if asset_id in manifest_by_id
        ]
        score = infer_priority_score(shot, blocked_by_assets)
        ranked.append((score, shot, blocked_by_assets))

    ranked.sort(key=lambda item: (-item[0], item[1]["id"]))

    for _, shot, blocked_by_assets in ranked:
        if not blocked_by_assets:
            skipped_count += 1
            continue
        build_method = infer_build_method(shot, blocked_by_assets)
        policies.append(
            {
                "shot_id": shot["id"],
                "build_method": build_method,
                "why": shot.get("action_core") or shot.get("beat") or shot.get("camera_intent", ""),
            }
        )

        queue_status = "ready" if all(manifest_by_id[a]["status"] == "committed" for a in blocked_by_assets) else "blocked"
        queue.append(
            {
                "shot_id": shot["id"],
                "purpose": shot.get("beat") or shot.get("action_core") or shot.get("camera_intent", ""),
                "blocked_by_assets": blocked_by_assets,
                "primary_refs": primary_refs_for_shot(shot, blocked_by_assets),
                "execution_mode": build_method,
                "queue_status": queue_status,
                "next_action": next_action_for_shot(queue_status, shot, blocked_by_assets),
                "fallback": fallback_for_shot(shot),
            }
        )

    continuity["shot_build_policy"] = policies
    director_queue["queue"] = queue
    director_queue["status_notes"] = [
        note for note in director_queue.get("status_notes", []) if "自动生成" not in note
    ]
    director_queue["status_notes"].append(
        "本轮 queue 由 generate-director-queue.py 根据 breakdown / manifest / continuity 自动生成。"
    )
    if skipped_count:
        director_queue["status_notes"].append(
            f"有 {skipped_count} 条镜头因当前 manifest 中缺少可绑定资产而未进入 queue，仍需先补 canonical 资产或清单。"
        )
    return continuity, director_queue


def merge_shot_items(
    existing_items: list[dict[str, Any]],
    generated_items: list[dict[str, Any]],
    *,
    only_shot_ids: set[str] | None,
    key: str,
) -> list[dict[str, Any]]:
    if not only_shot_ids:
        return generated_items
    generated_by_id = {item[key]: item for item in generated_items}
    merged = [dict(item) for item in existing_items]
    for shot_id in only_shot_ids:
        replacement = generated_by_id.get(shot_id)
        if not replacement:
            continue
        for idx, item in enumerate(merged):
            if item.get(key) == shot_id:
                merged[idx] = replacement
                break
        else:
            merged.append(replacement)
    return merged


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate continuity shot_build_policy and director queue from breakdown + manifest."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument("--episode", default="ep001", help="Episode folder to update. Defaults to ep001.")
    parser.add_argument("--only-shot-id", nargs="+", help="Only regenerate the listed shot ids.")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing YAML.")
    parser.add_argument("--render", action="store_true", help="Render Markdown after writing YAML.")
    args = parser.parse_args()

    archive_dir = resolve_archive_dir(args.project_or_archive_dir)
    episode_dir = archive_dir / "episodes" / args.episode
    continuity, director_queue = generate_queue_and_policy(archive_dir, args.episode)
    only_shot_ids = set(args.only_shot_id or [])
    continuity_path = episode_dir / "continuity-plan.yaml"
    director_queue_path = episode_dir / "director-queue.yaml"
    existing_continuity = load_yaml(continuity_path)
    existing_queue = load_yaml(director_queue_path)

    continuity["shot_build_policy"] = merge_shot_items(
        existing_continuity.get("shot_build_policy", []),
        continuity.get("shot_build_policy", []),
        only_shot_ids=only_shot_ids,
        key="shot_id",
    )
    director_queue["queue"] = merge_shot_items(
        existing_queue.get("queue", []),
        director_queue.get("queue", []),
        only_shot_ids=only_shot_ids,
        key="shot_id",
    )

    changed: list[Path] = []
    if continuity != existing_continuity:
        changed.append(continuity_path)
        if not args.dry_run:
            dump_yaml(continuity_path, continuity)
    if director_queue != existing_queue:
        changed.append(director_queue_path)
        if not args.dry_run:
            dump_yaml(director_queue_path, director_queue)
    if args.render and not args.dry_run:
        render_archive(archive_dir)
    mode = "Dry run" if args.dry_run else "Generated"
    print(f"{mode} director queue for: {episode_dir}")
    if changed:
        for path in changed:
            print(f"- {path}")
    else:
        print("No queue files required changes.")

if __name__ == "__main__":
    main()
