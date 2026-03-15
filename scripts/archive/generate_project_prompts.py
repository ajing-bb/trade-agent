#!/usr/bin/env python3
"""Generate prompt pack YAML files from canonical project bibles."""

from __future__ import annotations

import argparse
import subprocess
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


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)


def resolve_archive_dir(target: str) -> Path:
    path = Path(target).resolve()
    archive_dir = path if path.name == "项目档案" else path / "项目档案"
    if not archive_dir.exists():
        raise FileNotFoundError(f"Archive directory does not exist: {archive_dir}")
    return archive_dir


def merge_items(
    generated_items: list[dict[str, Any]],
    existing_items: list[dict[str, Any]],
    *,
    only_ids: set[str] | None,
    skip_existing: bool,
) -> list[dict[str, Any]]:
    generated_by_id = {item["id"]: item for item in generated_items}
    existing_by_id = {item["id"]: item for item in existing_items}

    if only_ids:
        merged = [dict(item) for item in existing_items]
        for asset_id in only_ids:
            if asset_id not in generated_by_id:
                continue
            if skip_existing and asset_id in existing_by_id:
                continue
            replacement = generated_by_id[asset_id]
            for idx, item in enumerate(merged):
                if item["id"] == asset_id:
                    merged[idx] = replacement
                    break
            else:
                merged.append(replacement)
        return merged

    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in generated_items:
        asset_id = item["id"]
        if skip_existing and asset_id in existing_by_id:
            merged.append(existing_by_id[asset_id])
        else:
            merged.append(item)
        seen.add(asset_id)
    for item in existing_items:
        if item["id"] not in seen:
            merged.append(item)
    return merged


def base_dir_for_asset(asset_root: str | None, fallback_prefix: str, item_id: str) -> str:
    if asset_root:
        return asset_root
    return f"{fallback_prefix}/{item_id}"


def status_scope(items: list[dict[str, Any]]) -> list[str]:
    return [item["id"] for item in items if item.get("status") in {"planned", "prompted"}]


def style_fragments(style: dict[str, Any]) -> tuple[str, str]:
    line_quality = style.get("line_and_render", {}).get("line_quality", "")
    shadow_depth = style.get("line_and_render", {}).get("shadow_depth", "")
    core_format = str(style.get("core_format", "")).lower()

    if "3d" in core_format:
        portrait = "stylized 3D rendering, animated genre portrait"
        general = "stylized 3D rendering, controlled cinematic lighting, animated genre still"
    else:
        portrait = "clean comic linework, 2D Chinese manhua still"
        general = f"clean comic linework, {shadow_depth}, 2D Chinese manhua still".strip(", ")

    if line_quality and "comic linework" not in portrait and "3d" not in portrait:
        portrait = f"{line_quality}, {portrait}"
    return portrait, general


def build_character_prompt_pack(
    project_id: str, archive_dir: Path, style: dict[str, Any], bible: dict[str, Any], episode: str
) -> dict[str, Any]:
    portrait_style, general_style = style_fragments(style)
    characters = bible.get("characters", [])
    generated: list[dict[str, Any]] = []
    for item in characters:
        status = item.get("status", "planned")
        asset_root = base_dir_for_asset(item.get("asset_root"), "assets/角色", item["id"])
        record: dict[str, Any] = {
            "id": item["id"],
            "name": item.get("name", item["id"]),
            "status": status,
            "target_path": asset_root,
            "reference_assets": [
                f"{archive_dir.as_posix()}/series/style-bible.yaml",
                f"{archive_dir.as_posix()}/series/character-bible.yaml",
            ],
            "required_outputs": [],
            "visual_anchors": item.get("visual_anchors", []),
            "midjourney": {},
            "banana": {},
            "archive_updates": [
                f"{archive_dir.as_posix()}/episodes/{episode}/asset-manifest.yaml",
                f"{archive_dir.as_posix()}/series/character-bible.yaml",
                f"{archive_dir.as_posix()}/series/character-asset-prompt-pack.yaml",
            ],
        }
        face_anchors = ", ".join(item.get("face_anchors", []))
        visual_anchors = ", ".join(item.get("visual_anchors", []))
        costume_core = item.get("costume_core", "")
        material_texture = item.get("material_texture", "")
        color_anchors = ", ".join(item.get("color_anchors", []))
        body = item.get("body_silhouette", "")
        hair = item.get("hair_headwear", "")
        role = item.get("role", "")
        age_hint = "18 years old"
        if "中年" in body or "50" in role or "中年" in role:
            age_hint = "early 50s"

        face_prompt = (
            f"one East Asian {role or 'character'}, {age_hint}, {face_anchors}, {hair}, "
            f"{costume_core}, waist-up portrait, plain light gray background, {portrait_style}, "
            f"{material_texture}, {visual_anchors}, not photoreal --ar 3:4 --v 7 --raw"
        )

        if any(token in item["id"] for token in ("MENGJIANG", "LINQIANQIAN", "ZHANGHE")):
            record["required_outputs"].extend(["face_draft", "full_body_master"])
            body_prompt = (
                f"one East Asian {role or 'character'}, {age_hint}, same face and same hairstyle as the selected reference, "
                f"{visual_anchors}, {body}, {costume_core}, {material_texture}, colors {color_anchors}, "
                f"standing straight, solo character, full body, centered composition, plain light gray background, "
                f"{general_style}, not photoreal --ar 9:16 --v 7 --raw --oref [{item['id']}_FACE_DRAFT] --ow 250"
            )
            record["midjourney"]["face_draft"] = " ".join(face_prompt.split())
            record["midjourney"]["full_body_master"] = " ".join(body_prompt.split())
        else:
            record["required_outputs"].extend(["face_draft", "half_body_master"])
            body_prompt = (
                f"one East Asian {role or 'character'}, {age_hint}, same face and same hairstyle as the selected reference, "
                f"{visual_anchors}, {body}, {costume_core}, {material_texture}, colors {color_anchors}, "
                f"half body, centered composition, plain light gray background, {general_style}, "
                f"not photoreal --ar 4:5 --v 7 --raw --oref [{item['id']}_FACE_DRAFT] --ow 220"
            )
            record["midjourney"]["face_draft"] = " ".join(face_prompt.split())
            record["midjourney"]["half_body_master"] = " ".join(body_prompt.split())

        if costume_core:
            record["banana"]["uniform_fix"] = (
                f"保留{item.get('name', item['id'])}的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的"
                f"{costume_core}。保留人物身份和画风，不要改成通用模板。"
            )
        generated.append(record)

    return {
        "prompt_pack_id": "CHARACTER_ASSET_PROMPT_PACK_V1",
        "project_id": project_id,
        "scope": status_scope(generated),
        "rules": {
            "midjourney_role": "base_generation_only",
            "banana_role": "derive_turnaround_expression_angle_and_repair",
            "canonical_note": "generated_from_character_bible",
            "character_pipeline": "face_draft_then_full_body_then_banana_derived_pack",
        },
        "characters": generated,
    }


def build_scene_prompt_pack(
    project_id: str, archive_dir: Path, style: dict[str, Any], bible: dict[str, Any], episode: str
) -> dict[str, Any]:
    _, general_style = style_fragments(style)
    generated: list[dict[str, Any]] = []
    for item in bible.get("locations", []):
        anchors = ", ".join(item.get("anchors", []))
        camera = ", ".join(item.get("camera_seeds", []))
        signature_assets = ", ".join(item.get("signature_assets", []))
        environment_type = item.get("environment_type", "")
        time_weather = ", ".join(filter(None, [item.get("time", ""), item.get("weather", "")]))
        target_path = base_dir_for_asset(item.get("asset_root"), "assets/场景", item["id"])
        master_label = item["id"].replace("LOC_", "")
        record = {
            "id": item["id"],
            "status": item.get("status", "planned"),
            "target_path": target_path,
            "reference_assets": [
                f"{archive_dir.as_posix()}/series/style-bible.yaml",
                f"{archive_dir.as_posix()}/series/scene-bible.yaml",
            ],
            "required_outputs": ["scene_master", "reverse_seed"] if item.get("reverse_shot_needed") else ["scene_master"],
            "midjourney": {
                "scene_master": " ".join(
                    (
                        f"{item.get('name', item['id'])}, {item.get('function', '')}, {environment_type}, "
                        f"{anchors}, {signature_assets}, {time_weather}, {general_style}, readable wide composition, "
                        f"camera coverage seeds: {camera}, not photoreal --ar 16:9 --v 7 --raw"
                    ).split()
                )
            },
            "banana": {},
            "archive_updates": [
                f"{archive_dir.as_posix()}/episodes/{episode}/asset-manifest.yaml",
                f"{archive_dir.as_posix()}/series/scene-bible.yaml",
                f"{archive_dir.as_posix()}/series/scene-asset-prompt-pack.yaml",
            ],
        }
        if item.get("reverse_shot_needed"):
            record["midjourney"]["reverse_seed"] = " ".join(
                (
                    f"same {item.get('name', item['id'])}, reverse-side view of the same space, preserve {anchors}, "
                    f"preserve layout logic, same {time_weather}, {general_style} --ar 16:9 --v 7 --raw "
                    f"--oref [{master_label}_MASTER] --ow 200"
                ).split()
            )
        record["banana"]["layout_cleanup"] = (
            f"保留{item.get('name', item['id'])}的空间布局、透视、锚点和光照不变，只清理错误结构与不稳定细节，"
            "使它成为后续镜头可复用的稳定母图。"
        )
        generated.append(record)

    return {
        "prompt_pack_id": "SCENE_ASSET_PROMPT_PACK_V1",
        "project_id": project_id,
        "rules": {
            "midjourney_role": "scene_master_only",
            "banana_role": "derive_reverse_angle_variant_and_repair",
            "scene_pipeline": "scene_master_then_banana_derived_views",
        },
        "locations": generated,
    }


def build_prop_vfx_prompt_pack(
    project_id: str, archive_dir: Path, style: dict[str, Any], bible: dict[str, Any], episode: str
) -> dict[str, Any]:
    _, general_style = style_fragments(style)
    prop_items: list[dict[str, Any]] = []
    for item in bible.get("props", []):
        anchors = ", ".join(item.get("visual_anchors", []))
        target_path = base_dir_for_asset(item.get("asset_root"), "assets/道具", item["id"])
        prompt_key = "master_card" if not item["id"].startswith("PROP_") else "master_view"
        aspect = "2:3" if prompt_key == "master_card" else "1:1"
        prop_items.append(
            {
                "id": item["id"],
                "status": item.get("status", "planned"),
                "target_path": target_path,
                "reference_assets": [
                    f"{archive_dir.as_posix()}/series/style-bible.yaml",
                    f"{archive_dir.as_posix()}/series/prop-vfx-bible.yaml",
                ],
                "archive_updates": [
                    f"{archive_dir.as_posix()}/episodes/{episode}/asset-manifest.yaml",
                    f"{archive_dir.as_posix()}/series/prop-vfx-bible.yaml",
                    f"{archive_dir.as_posix()}/series/prop-vfx-asset-prompt-pack.yaml",
                ],
                "midjourney": {
                    prompt_key: " ".join(
                        (
                            f"one {item.get('name', item['id'])}, {item.get('function', '')}, {anchors}, "
                            f"{general_style}, clean background, readable silhouette, not photoreal "
                            f"--ar {aspect} --v 7 --raw"
                        ).split()
                    )
                },
                "banana": {
                    "cleanup": f"保留{item.get('name', item['id'])}的主体轮廓和识别符号不变，只清理边框、结构与细节，使其更稳定。"
                },
            }
        )

    vfx_items: list[dict[str, Any]] = []
    for item in bible.get("vfx", []):
        target_path = base_dir_for_asset(item.get("asset_root"), "assets/VFX", item["id"])
        vfx_items.append(
            {
                "id": item["id"],
                "status": item.get("status", "planned"),
                "target_path": target_path,
                "reference_assets": [
                    f"{archive_dir.as_posix()}/series/style-bible.yaml",
                    f"{archive_dir.as_posix()}/series/prop-vfx-bible.yaml",
                ],
                "archive_updates": [
                    f"{archive_dir.as_posix()}/episodes/{episode}/asset-manifest.yaml",
                    f"{archive_dir.as_posix()}/series/prop-vfx-bible.yaml",
                    f"{archive_dir.as_posix()}/series/prop-vfx-asset-prompt-pack.yaml",
                ],
                "midjourney": {
                    "keyframe": " ".join(
                        (
                            f"{item.get('name', item['id'])}, {item.get('function', '')}, {general_style}, "
                            "clear effect silhouette, clean large-scale energy read, not photoreal --ar 16:9 --v 7 --raw"
                        ).split()
                    )
                },
                "banana": {
                    "refine": f"保留{item.get('name', item['id'])}的核心颜色和能量逻辑不变，只调整边缘、层次和识别度，使其更稳定。"
                },
            }
        )

    return {
        "prompt_pack_id": "PROP_VFX_ASSET_PROMPT_PACK_V1",
        "project_id": project_id,
        "rules": {
            "midjourney_role": "asset_master_only",
            "banana_role": "derive_variant_and_repair",
        },
        "props": prop_items,
        "vfx": vfx_items,
    }


def render_archive(archive_dir: Path) -> None:
    render_script = Path(__file__).with_name("render_project_archive.py")
    subprocess.run([sys.executable, str(render_script), str(archive_dir)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate project prompt pack YAML files from canonical bibles."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument(
        "--episode",
        default="ep001",
        help="Episode folder used in archive_updates. Defaults to ep001.",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        help="Only regenerate the listed asset ids and leave other entries unchanged.",
    )
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Do not overwrite already existing prompt entries for targeted asset ids.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview which prompt pack files would change without writing.",
    )
    parser.add_argument(
        "--render",
        action="store_true",
        help="Render Markdown files after rewriting prompt pack YAML files.",
    )
    args = parser.parse_args()

    archive_dir = resolve_archive_dir(args.project_or_archive_dir)
    series_dir = archive_dir / "series"
    series_bible = load_yaml(series_dir / "series-bible.yaml")
    style_bible = load_yaml(series_dir / "style-bible.yaml")
    character_bible = load_yaml(series_dir / "character-bible.yaml")
    scene_bible = load_yaml(series_dir / "scene-bible.yaml")
    prop_vfx_bible = load_yaml(series_dir / "prop-vfx-bible.yaml")

    project_id = str(series_bible.get("project_id", "PROJECT"))
    only_ids = set(args.only or [])

    generated_character = build_character_prompt_pack(project_id, archive_dir, style_bible, character_bible, args.episode)
    generated_scene = build_scene_prompt_pack(project_id, archive_dir, style_bible, scene_bible, args.episode)
    generated_prop_vfx = build_prop_vfx_prompt_pack(project_id, archive_dir, style_bible, prop_vfx_bible, args.episode)

    target_files = [
        ("characters", series_dir / "character-asset-prompt-pack.yaml", generated_character),
        ("locations", series_dir / "scene-asset-prompt-pack.yaml", generated_scene),
        ("props_vfx", series_dir / "prop-vfx-asset-prompt-pack.yaml", generated_prop_vfx),
    ]

    changed: list[Path] = []
    for section_name, path, generated in target_files:
        existing = load_yaml(path) if path.exists() else {}
        merged = dict(generated)
        if section_name == "characters":
            merged["characters"] = merge_items(
                generated["characters"],
                existing.get("characters", []),
                only_ids=only_ids,
                skip_existing=args.skip_existing,
            )
            merged["scope"] = status_scope(merged["characters"])
        elif section_name == "locations":
            merged["locations"] = merge_items(
                generated["locations"],
                existing.get("locations", []),
                only_ids=only_ids,
                skip_existing=args.skip_existing,
            )
        else:
            merged["props"] = merge_items(
                generated["props"],
                existing.get("props", []),
                only_ids=only_ids,
                skip_existing=args.skip_existing,
            )
            merged["vfx"] = merge_items(
                generated["vfx"],
                existing.get("vfx", []),
                only_ids=only_ids,
                skip_existing=args.skip_existing,
            )
        if merged != existing:
            changed.append(path)
            if not args.dry_run:
                dump_yaml(path, merged)

    if args.render and not args.dry_run:
        render_archive(archive_dir)

    mode = "Dry run" if args.dry_run else "Generated"
    print(f"{mode} prompt packs under: {series_dir}")
    if changed:
        for path in changed:
            print(f"- {path}")
    else:
        print("No prompt pack files required changes.")


if __name__ == "__main__":
    main()
