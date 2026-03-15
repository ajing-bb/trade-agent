#!/usr/bin/env python3
"""Shared asset-status helpers for project archive scripts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


VALID_STATUSES = {"planned", "prompted", "committed"}


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


def episode_dir(archive_dir: Path, episode: str) -> Path:
    resolved = archive_dir / "episodes" / episode
    if not resolved.exists():
        raise FileNotFoundError(f"Episode directory does not exist: {resolved}")
    return resolved


def load_asset_manifest(path: Path, asset_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    data = load_yaml(path)
    for item in data.get("assets", []):
        if item.get("id") == asset_id:
            return data, item
    raise KeyError(f"Asset id not found in manifest: {asset_id}")


def bible_path_and_section(asset_type: str, series_dir: Path) -> tuple[Path, str]:
    if asset_type == "character":
        return series_dir / "character-bible.yaml", "characters"
    if asset_type == "scene":
        return series_dir / "scene-bible.yaml", "locations"
    if asset_type == "prop":
        return series_dir / "prop-vfx-bible.yaml", "props"
    if asset_type == "vfx":
        return series_dir / "prop-vfx-bible.yaml", "vfx"
    raise ValueError(f"Unsupported asset type: {asset_type}")


def update_bible_record(path: Path, section: str, asset_id: str, status: str, raw_path: str | None) -> bool:
    data = load_yaml(path)
    changed = False
    for item in data.get(section, []):
        if item.get("id") != asset_id:
            continue
        if item.get("status") != status:
            item["status"] = status
            changed = True
        if raw_path and item.get("asset_root") != raw_path:
            item["asset_root"] = raw_path
            changed = True
        break
    if changed:
        dump_yaml(path, data)
    return changed


def update_prompt_pack_status(path: Path, asset_id: str, status: str, raw_path: str | None) -> bool:
    data = load_yaml(path)
    changed = False

    def update_items(items: list[dict[str, Any]]) -> None:
        nonlocal changed
        for item in items:
            if item.get("id") != asset_id:
                continue
            if item.get("status") != status:
                item["status"] = status
                changed = True
            if raw_path and item.get("target_path") != raw_path:
                item["target_path"] = raw_path
                changed = True

    update_items(data.get("characters", []))
    update_items(data.get("locations", []))
    update_items(data.get("props", []))
    update_items(data.get("vfx", []))
    if changed:
        dump_yaml(path, data)
    return changed


def update_continuity_plan(path: Path, asset_id: str, asset_type: str, status: str) -> bool:
    if asset_type != "character":
        return False
    data = load_yaml(path)
    canonical = list(data.get("canonical_character_assets", []))
    pending = list(data.get("pending_character_assets", []))
    if status == "committed":
        if asset_id not in canonical:
            canonical.append(asset_id)
        pending = [item for item in pending if item != asset_id]
    else:
        if asset_id not in pending:
            pending.append(asset_id)
        canonical = [item for item in canonical if item != asset_id]
    changed = canonical != data.get("canonical_character_assets", []) or pending != data.get("pending_character_assets", [])
    if changed:
        data["canonical_character_assets"] = canonical
        data["pending_character_assets"] = pending
        dump_yaml(path, data)
    return changed


def committed_asset_index(manifest_data: dict[str, Any]) -> set[str]:
    return {item["id"] for item in manifest_data.get("assets", []) if item.get("status") == "committed"}


def update_director_queue(path: Path, committed_assets: set[str]) -> bool:
    data = load_yaml(path)
    changed = False
    for item in data.get("queue", []):
        blocked = item.get("blocked_by_assets", [])
        if not blocked:
            continue
        desired_status = "ready" if all(asset_id in committed_assets for asset_id in blocked) else "blocked"
        if item.get("queue_status") != desired_status:
            item["queue_status"] = desired_status
            changed = True
    if changed:
        dump_yaml(path, data)
    return changed


def render_and_check(archive_dir: Path) -> None:
    scripts_dir = Path(__file__).resolve().parent
    render_script = scripts_dir / "render_project_archive.py"
    health_script = scripts_dir / "check_asset_health.py"
    subprocess.run([sys.executable, str(render_script), str(archive_dir)], check=True)
    subprocess.run([sys.executable, str(health_script), str(archive_dir.parent)], check=True)


def apply_asset_status(
    archive_dir: Path,
    asset_id: str,
    status: str,
    *,
    raw_path: str | None = None,
    episode: str = "ep001",
    render: bool = True,
) -> list[Path]:
    if status not in VALID_STATUSES:
        raise ValueError(f"Unsupported status: {status}")

    series_dir = archive_dir / "series"
    ep_dir = episode_dir(archive_dir, episode)
    manifest_path = ep_dir / "asset-manifest.yaml"
    manifest_data, manifest_item = load_asset_manifest(manifest_path, asset_id)
    asset_type = manifest_item.get("type")
    effective_path = raw_path or manifest_item.get("path")

    if status == "committed" and not effective_path:
        raise ValueError("--path is required when committing an asset with no recorded path.")

    changed_files: list[Path] = []
    manifest_changed = False
    if manifest_item.get("status") != status:
        manifest_item["status"] = status
        manifest_changed = True
    if effective_path and manifest_item.get("path") != effective_path:
        manifest_item["path"] = effective_path
        manifest_changed = True
    if manifest_changed:
        dump_yaml(manifest_path, manifest_data)
        changed_files.append(manifest_path)

    bible_path, section = bible_path_and_section(asset_type, series_dir)
    if update_bible_record(bible_path, section, asset_id, status, effective_path):
        changed_files.append(bible_path)

    for prompt_pack_name in (
        "character-asset-prompt-pack.yaml",
        "scene-asset-prompt-pack.yaml",
        "prop-vfx-asset-prompt-pack.yaml",
    ):
        prompt_pack_path = series_dir / prompt_pack_name
        if prompt_pack_path.exists() and update_prompt_pack_status(prompt_pack_path, asset_id, status, effective_path):
            changed_files.append(prompt_pack_path)

    continuity_path = ep_dir / "continuity-plan.yaml"
    if continuity_path.exists() and update_continuity_plan(continuity_path, asset_id, asset_type, status):
        changed_files.append(continuity_path)

    refreshed_manifest = load_yaml(manifest_path)
    committed_assets = committed_asset_index(refreshed_manifest)
    director_queue_path = ep_dir / "director-queue.yaml"
    if director_queue_path.exists() and update_director_queue(director_queue_path, committed_assets):
        changed_files.append(director_queue_path)

    if render:
        render_and_check(archive_dir)

    return changed_files
