#!/usr/bin/env python3
"""Check whether canonical asset paths still match the filesystem."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def resolve_archive(target: str) -> tuple[Path, Path]:
    path = Path(target).resolve()
    if path.name == "项目档案":
        return path.parent, path
    return path, path / "项目档案"


def resolve_record_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (Path.cwd() / path).resolve()


def suspicious_path(raw_path: str) -> bool:
    return any(part != part.strip() for part in Path(raw_path).parts) or "//" in raw_path


def add_finding(
    findings: list[dict[str, str]],
    severity: str,
    code: str,
    source: str,
    item_id: str,
    field: str,
    raw_path: str,
    message: str,
) -> None:
    findings.append(
        {
            "severity": severity,
            "code": code,
            "source": source,
            "item_id": item_id,
            "field": field,
            "path": raw_path,
            "message": message,
        }
    )


def check_path(
    findings: list[dict[str, str]],
    source: str,
    item_id: str,
    field: str,
    raw_path: str | None,
    status: str | None,
    expected_kind: str | None,
    missing_severity: str,
) -> None:
    if not raw_path:
        if status == "committed":
            add_finding(
                findings,
                "error",
                "missing_path_field",
                source,
                item_id,
                field,
                "",
                "status=committed but no path was recorded",
            )
        return

    if suspicious_path(raw_path):
        add_finding(
            findings,
            "warning",
            "suspicious_path",
            source,
            item_id,
            field,
            raw_path,
            "path contains leading/trailing spaces or duplicated separators",
        )

    resolved = resolve_record_path(raw_path)
    if not resolved.exists():
        add_finding(
            findings,
            missing_severity,
            "missing_path",
            source,
            item_id,
            field,
            raw_path,
            "path recorded in YAML does not exist on disk",
        )
        return

    if expected_kind == "dir" and not resolved.is_dir():
        add_finding(
            findings,
            "error",
            "expected_directory",
            source,
            item_id,
            field,
            raw_path,
            "expected a directory but found a file",
        )
    if expected_kind == "file" and not resolved.is_file():
        add_finding(
            findings,
            "error",
            "expected_file",
            source,
            item_id,
            field,
            raw_path,
            "expected a file but found a directory",
        )


def check_character_bible(archive_dir: Path, findings: list[dict[str, str]]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    path = archive_dir / "series" / "character-bible.yaml"
    if not path.exists():
        return mapping
    data = load_yaml(path)
    for item in data.get("characters", []):
        item_id = item.get("id", "")
        status = item.get("status")
        asset_root = item.get("asset_root")
        if status == "committed" and asset_root:
            mapping[item_id] = asset_root
        check_path(
            findings,
            "character-bible.yaml",
            item_id,
            "asset_root",
            asset_root,
            status,
            "dir",
            "error" if status == "committed" else "warning",
        )
        prompt_pack = item.get("prompt_pack")
        if prompt_pack:
            check_path(
                findings,
                "character-bible.yaml",
                item_id,
                "prompt_pack",
                prompt_pack,
                status,
                "file",
                "error",
            )
    return mapping


def first_path_field(item: dict[str, Any], field_names: tuple[str, ...]) -> tuple[str | None, str]:
    for field_name in field_names:
        raw_value = item.get(field_name)
        if isinstance(raw_value, str) and raw_value:
            return raw_value, field_name
    return None, ""


def check_scene_bible(archive_dir: Path, findings: list[dict[str, str]]) -> tuple[set[str], dict[str, str]]:
    committed_ids: set[str] = set()
    mapping: dict[str, str] = {}
    path = archive_dir / "series" / "scene-bible.yaml"
    if not path.exists():
        return committed_ids, mapping
    data = load_yaml(path)
    for item in data.get("locations", []):
        item_id = item.get("id", "")
        status = item.get("status")
        if status == "committed":
            committed_ids.add(item_id)
        asset_path, _ = first_path_field(item, ("asset_root", "path", "master_path", "master_shot_path"))
        if status == "committed" and asset_path:
            mapping[item_id] = asset_path
        prompt_pack = item.get("prompt_pack")
        if prompt_pack:
            check_path(
                findings,
                "scene-bible.yaml",
                item_id,
                "prompt_pack",
                prompt_pack,
                status,
                "file",
                "error",
            )
    return committed_ids, mapping


def check_prop_vfx_bible(
    archive_dir: Path, findings: list[dict[str, str]]
) -> tuple[dict[str, set[str]], dict[str, dict[str, str]]]:
    committed_ids = {"prop": set(), "vfx": set()}
    mappings = {"prop": {}, "vfx": {}}
    path = archive_dir / "series" / "prop-vfx-bible.yaml"
    if not path.exists():
        return committed_ids, mappings
    data = load_yaml(path)
    for section_name, manifest_type in (("props", "prop"), ("vfx", "vfx")):
        for item in data.get(section_name, []):
            item_id = item.get("id", "")
            status = item.get("status")
            if status == "committed":
                committed_ids[manifest_type].add(item_id)
            asset_path, _ = first_path_field(item, ("asset_root", "path", "master_path", "master_plate_path"))
            if status == "committed" and asset_path:
                mappings[manifest_type][item_id] = asset_path
            prompt_pack = item.get("prompt_pack")
            if prompt_pack:
                check_path(
                    findings,
                    "prop-vfx-bible.yaml",
                    item_id,
                    "prompt_pack",
                    prompt_pack,
                    status,
                    "file",
                    "error",
                )
    return committed_ids, mappings


def check_asset_manifest(
    archive_dir: Path, findings: list[dict[str, str]]
) -> tuple[dict[str, set[str]], dict[str, dict[str, str]]]:
    committed_ids = {"character": set(), "scene": set(), "prop": set(), "vfx": set()}
    mappings = {"character": {}, "scene": {}, "prop": {}, "vfx": {}}
    episodes_dir = archive_dir / "episodes"
    for episode_dir in sorted(episodes_dir.glob("ep*")):
        path = episode_dir / "asset-manifest.yaml"
        if not path.exists():
            continue
        data = load_yaml(path)
        for item in data.get("assets", []):
            item_id = item.get("id", "")
            status = item.get("status")
            raw_path = item.get("path")
            item_type = item.get("type")
            if item_type in committed_ids and status == "committed":
                committed_ids[item_type].add(item_id)
                if raw_path:
                    mappings[item_type][item_id] = raw_path
            expected_kind = "dir" if item_type in {"character", "scene", "prop", "vfx"} else "file"
            check_path(
                findings,
                f"{episode_dir.name}/asset-manifest.yaml",
                item_id,
                "path",
                raw_path,
                status,
                expected_kind,
                "error" if status == "committed" else "warning",
            )
    return committed_ids, mappings


def check_prompt_pack_item_paths(
    findings: list[dict[str, str]], source: str, item_id: str, status: str | None, item: dict[str, Any]
) -> None:
    if "target_path" in item:
        check_path(
            findings,
            source,
            item_id,
            "target_path",
            item.get("target_path"),
            status,
            "dir",
            "warning",
        )
    for field in ("reference_assets", "archive_updates"):
        for raw_path in item.get(field, []):
            check_path(
                findings,
                source,
                item_id,
                field,
                raw_path,
                status,
                None if field == "reference_assets" else "file",
                "error" if field == "reference_assets" else "warning",
            )


def check_character_prompt_pack(archive_dir: Path, findings: list[dict[str, str]]) -> None:
    path = archive_dir / "series" / "character-asset-prompt-pack.yaml"
    if not path.exists():
        return
    data = load_yaml(path)
    for item in data.get("characters", []):
        check_prompt_pack_item_paths(
            findings,
            "character-asset-prompt-pack.yaml",
            item.get("id", ""),
            item.get("status"),
            item,
        )


def check_scene_prompt_pack(archive_dir: Path, findings: list[dict[str, str]]) -> None:
    path = archive_dir / "series" / "scene-asset-prompt-pack.yaml"
    if not path.exists():
        return
    data = load_yaml(path)
    for item in data.get("locations", []):
        check_prompt_pack_item_paths(
            findings,
            "scene-asset-prompt-pack.yaml",
            item.get("id", ""),
            item.get("status"),
            item,
        )


def check_prop_vfx_prompt_pack(archive_dir: Path, findings: list[dict[str, str]]) -> None:
    path = archive_dir / "series" / "prop-vfx-asset-prompt-pack.yaml"
    if not path.exists():
        return
    data = load_yaml(path)
    for section_name in ("props", "vfx"):
        for item in data.get(section_name, []):
            check_prompt_pack_item_paths(
                findings,
                "prop-vfx-asset-prompt-pack.yaml",
                item.get("id", ""),
                item.get("status"),
                item,
            )


def load_episode_breakdown_index(
    episode_dir: Path, findings: list[dict[str, str]]
) -> tuple[set[str], set[str]]:
    path = episode_dir / "breakdown.yaml"
    scene_ids: set[str] = set()
    shot_ids: set[str] = set()
    if not path.exists():
        return scene_ids, shot_ids
    data = load_yaml(path)
    for item in data.get("scenes", []):
        scene_id = item.get("id", "")
        if not scene_id:
            continue
        if scene_id in scene_ids:
            add_finding(
                findings,
                "error",
                "duplicate_breakdown_scene",
                f"{episode_dir.name}/breakdown.yaml",
                scene_id,
                "id",
                scene_id,
                "scene id is duplicated in breakdown",
            )
            continue
        scene_ids.add(scene_id)
    for item in data.get("shots", []):
        shot_id = item.get("id", "")
        if not shot_id:
            continue
        if shot_id in shot_ids:
            add_finding(
                findings,
                "error",
                "duplicate_breakdown_shot",
                f"{episode_dir.name}/breakdown.yaml",
                shot_id,
                "id",
                shot_id,
                "shot id is duplicated in breakdown",
            )
            continue
        shot_ids.add(shot_id)
    return scene_ids, shot_ids


def load_episode_asset_index(
    episode_dir: Path, findings: list[dict[str, str]]
) -> dict[str, dict[str, str]]:
    path = episode_dir / "asset-manifest.yaml"
    index: dict[str, dict[str, str]] = {}
    if not path.exists():
        return index
    data = load_yaml(path)
    for item in data.get("assets", []):
        item_id = item.get("id", "")
        if not item_id:
            continue
        if item_id in index:
            add_finding(
                findings,
                "error",
                "duplicate_asset_manifest_id",
                f"{episode_dir.name}/asset-manifest.yaml",
                item_id,
                "id",
                item_id,
                "asset id is duplicated in asset-manifest",
            )
            continue
        index[item_id] = {
            "type": str(item.get("type", "")),
            "status": str(item.get("status", "")),
        }
    return index


def validate_continuity_plan(
    episode_dir: Path,
    shot_ids: set[str],
    asset_index: dict[str, dict[str, str]],
    findings: list[dict[str, str]],
) -> set[str]:
    path = episode_dir / "continuity-plan.yaml"
    policy_shots: set[str] = set()
    if not path.exists():
        return policy_shots
    data = load_yaml(path)
    for item in data.get("shot_build_policy", []):
        shot_id = item.get("shot_id", "")
        if not shot_id:
            continue
        if shot_id in policy_shots:
            add_finding(
                findings,
                "error",
                "duplicate_continuity_policy_shot",
                f"{episode_dir.name}/continuity-plan.yaml",
                shot_id,
                "shot_id",
                shot_id,
                "shot_build_policy references the same shot more than once",
            )
            continue
        policy_shots.add(shot_id)
        if shot_id not in shot_ids:
            add_finding(
                findings,
                "error",
                "missing_breakdown_shot",
                f"{episode_dir.name}/continuity-plan.yaml",
                shot_id,
                "shot_id",
                shot_id,
                "shot_build_policy references a shot id missing from breakdown",
            )
    for field_name, expected_status in (
        ("canonical_character_assets", "committed"),
        ("pending_character_assets", "pending"),
    ):
        for asset_id in data.get(field_name, []):
            asset = asset_index.get(asset_id)
            if not asset:
                add_finding(
                    findings,
                    "error",
                    f"missing_{field_name}_asset",
                    f"{episode_dir.name}/continuity-plan.yaml",
                    asset_id,
                    field_name,
                    asset_id,
                    f"{field_name} references an asset id missing from asset-manifest",
                )
                continue
            if asset["type"] != "character":
                add_finding(
                    findings,
                    "error",
                    f"invalid_{field_name}_type",
                    f"{episode_dir.name}/continuity-plan.yaml",
                    asset_id,
                    field_name,
                    asset_id,
                    f"{field_name} must only reference character assets",
                )
                continue
            if field_name == "canonical_character_assets" and asset["status"] != expected_status:
                add_finding(
                    findings,
                    "error",
                    "invalid_canonical_character_asset",
                    f"{episode_dir.name}/continuity-plan.yaml",
                    asset_id,
                    field_name,
                    asset_id,
                    "canonical_character_assets must reference committed character assets",
                )
            if field_name == "pending_character_assets" and asset["status"] == "committed":
                add_finding(
                    findings,
                    "error",
                    "invalid_pending_character_asset",
                    f"{episode_dir.name}/continuity-plan.yaml",
                    asset_id,
                    field_name,
                    asset_id,
                    "pending_character_assets must not reference committed character assets",
                )
    return policy_shots


def validate_director_queue(
    episode_dir: Path,
    shot_ids: set[str],
    asset_index: dict[str, dict[str, str]],
    continuity_shots: set[str],
    findings: list[dict[str, str]],
) -> set[str]:
    path = episode_dir / "director-queue.yaml"
    queue_shots: set[str] = set()
    if not path.exists():
        return queue_shots
    data = load_yaml(path)
    allowed_statuses = set(data.get("queue_rules", {}).keys()) or {"blocked", "ready", "in_progress", "done"}
    for item in data.get("queue", []):
        shot_id = item.get("shot_id", "")
        if not shot_id:
            continue
        if shot_id in queue_shots:
            add_finding(
                findings,
                "error",
                "duplicate_director_queue_shot",
                f"{episode_dir.name}/director-queue.yaml",
                shot_id,
                "shot_id",
                shot_id,
                "director queue references the same shot more than once",
            )
            continue
        queue_shots.add(shot_id)
        if shot_id not in shot_ids:
            add_finding(
                findings,
                "error",
                "missing_breakdown_shot",
                f"{episode_dir.name}/director-queue.yaml",
                shot_id,
                "shot_id",
                shot_id,
                "director queue references a shot id missing from breakdown",
            )
        queue_status = item.get("queue_status", "")
        if queue_status not in allowed_statuses:
            add_finding(
                findings,
                "error",
                "invalid_queue_status",
                f"{episode_dir.name}/director-queue.yaml",
                shot_id,
                "queue_status",
                queue_status,
                "queue_status is not defined in queue_rules",
            )
        blocked_by_assets = item.get("blocked_by_assets", [])
        if queue_status == "blocked" and not blocked_by_assets:
            add_finding(
                findings,
                "warning",
                "blocked_without_assets",
                f"{episode_dir.name}/director-queue.yaml",
                shot_id,
                "blocked_by_assets",
                "",
                "blocked queue item has no blocking assets recorded",
            )
        for asset_id in blocked_by_assets:
            asset = asset_index.get(asset_id)
            if not asset:
                add_finding(
                    findings,
                    "error",
                    "missing_blocking_asset",
                    f"{episode_dir.name}/director-queue.yaml",
                    shot_id,
                    "blocked_by_assets",
                    asset_id,
                    "blocked_by_assets references an asset id missing from asset-manifest",
                )
                continue
            if queue_status in {"ready", "in_progress", "done"} and asset["status"] != "committed":
                add_finding(
                    findings,
                    "error",
                    "uncommitted_blocking_asset",
                    f"{episode_dir.name}/director-queue.yaml",
                    shot_id,
                    "blocked_by_assets",
                    asset_id,
                    "active queue item still references a non-committed blocking asset",
                )
        if shot_id not in continuity_shots:
            add_finding(
                findings,
                "warning",
                "missing_continuity_policy",
                f"{episode_dir.name}/director-queue.yaml",
                shot_id,
                "shot_id",
                shot_id,
                "director queue shot has no matching continuity shot_build_policy entry",
            )
    return queue_shots


def check_episode_semantics(archive_dir: Path, findings: list[dict[str, str]]) -> None:
    episodes_dir = archive_dir / "episodes"
    for episode_dir in sorted(episodes_dir.glob("ep*")):
        _, shot_ids = load_episode_breakdown_index(episode_dir, findings)
        asset_index = load_episode_asset_index(episode_dir, findings)
        continuity_shots = validate_continuity_plan(episode_dir, shot_ids, asset_index, findings)
        queue_shots = validate_director_queue(episode_dir, shot_ids, asset_index, continuity_shots, findings)
        for shot_id in sorted(continuity_shots - queue_shots):
            add_finding(
                findings,
                "warning",
                "missing_director_queue_shot",
                f"{episode_dir.name}/continuity-plan.yaml",
                shot_id,
                "shot_id",
                shot_id,
                "continuity shot_build_policy has no matching director queue entry",
            )


def check_cross_consistency(
    findings: list[dict[str, str]],
    item_type: str,
    manifest_ids: set[str],
    manifest_paths: dict[str, str],
    bible_ids: set[str],
    bible_paths: dict[str, str],
    bible_field: str,
) -> None:
    for item_id in sorted(manifest_ids | bible_ids):
        manifest_present = item_id in manifest_ids
        bible_present = item_id in bible_ids
        manifest_path = manifest_paths.get(item_id, "")
        bible_path = bible_paths.get(item_id, "")
        if manifest_present and not bible_present:
            add_finding(
                findings,
                "error",
                f"missing_{item_type}_bible_entry",
                "cross-check",
                item_id,
                bible_field,
                manifest_path,
                f"committed {item_type} exists in asset-manifest but not in matching bible",
            )
            continue
        if bible_present and not manifest_present:
            add_finding(
                findings,
                "error",
                f"missing_asset_manifest_{item_type}_entry",
                "cross-check",
                item_id,
                "path",
                bible_path,
                f"committed {item_type} exists in matching bible but not in asset-manifest",
            )
            continue
        if manifest_path and bible_path:
            if resolve_record_path(manifest_path) != resolve_record_path(bible_path):
                add_finding(
                    findings,
                    "error",
                    f"{item_type}_path_mismatch",
                    "cross-check",
                    item_id,
                    "path",
                    manifest_path,
                    f"asset-manifest path and matching bible {bible_field} do not match",
                )


def print_human(findings: list[dict[str, str]], project_root: Path, archive_dir: Path) -> None:
    print(f"Project root: {project_root}")
    print(f"Archive dir: {archive_dir}")
    if not findings:
        print("OK: no asset health issues found.")
        return
    for finding in findings:
        print(
            f"[{finding['severity'].upper()}] {finding['source']} {finding['item_id']} "
            f"{finding['field']} -> {finding['message']} ({finding['path']})"
        )
    errors = sum(1 for finding in findings if finding["severity"] == "error")
    warnings = sum(1 for finding in findings if finding["severity"] == "warning")
    infos = sum(1 for finding in findings if finding["severity"] == "info")
    print(f"Summary: {errors} error(s), {warnings} warning(s), {infos} info message(s).")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether canonical asset paths in YAML still match the filesystem."
    )
    parser.add_argument("target", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root, archive_dir = resolve_archive(args.target)
    findings: list[dict[str, str]] = []

    if not archive_dir.exists():
        add_finding(
            findings,
            "info",
            "fresh_start",
            "archive",
            "",
            "",
            "",
            "fresh start: no canonical archive exists yet",
        )
        if args.json:
            print(
                json.dumps(
                    {
                        "project_root": str(project_root),
                        "archive_dir": str(archive_dir),
                        "findings": findings,
                    },
                    ensure_ascii=False,
                    indent=2,
                )
            )
        else:
            print_human(findings, project_root, archive_dir)
        sys.exit(0)

    bible_characters = check_character_bible(archive_dir, findings)
    scene_ids, scene_paths = check_scene_bible(archive_dir, findings)
    prop_vfx_ids, prop_vfx_paths = check_prop_vfx_bible(archive_dir, findings)
    manifest_ids, manifest_paths = check_asset_manifest(archive_dir, findings)
    check_character_prompt_pack(archive_dir, findings)
    check_scene_prompt_pack(archive_dir, findings)
    check_prop_vfx_prompt_pack(archive_dir, findings)
    check_episode_semantics(archive_dir, findings)
    check_cross_consistency(
        findings,
        "character",
        manifest_ids["character"],
        manifest_paths["character"],
        set(bible_characters),
        bible_characters,
        "asset_root",
    )
    check_cross_consistency(
        findings,
        "scene",
        manifest_ids["scene"],
        manifest_paths["scene"],
        scene_ids,
        scene_paths,
        "asset_root",
    )
    check_cross_consistency(
        findings,
        "prop",
        manifest_ids["prop"],
        manifest_paths["prop"],
        prop_vfx_ids["prop"],
        prop_vfx_paths["prop"],
        "asset_root",
    )
    check_cross_consistency(
        findings,
        "vfx",
        manifest_ids["vfx"],
        manifest_paths["vfx"],
        prop_vfx_ids["vfx"],
        prop_vfx_paths["vfx"],
        "asset_root",
    )

    if args.json:
        print(
            json.dumps(
                {
                    "project_root": str(project_root),
                    "archive_dir": str(archive_dir),
                    "findings": findings,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print_human(findings, project_root, archive_dir)

    has_errors = any(finding["severity"] == "error" for finding in findings)
    sys.exit(1 if has_errors else 0)


if __name__ == "__main__":
    main()
