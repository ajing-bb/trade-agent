#!/usr/bin/env python3
"""Switch a project archive between reusable visual style presets."""

from __future__ import annotations

import argparse
import copy
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


PRESETS: dict[str, dict[str, Any]] = {
    "2d-manhua": {
        "aliases": {"2d", "manhua", "2d-manhua"},
        "display_name": "2D manhua",
        "realism_level": "semi-flat",
        "line_and_render": {
            "line_quality": "hard-clean with selective weight change",
            "shadow_depth": "2-step cel shade with restrained rim light",
            "skin_finish": "matte with slight warm highlight",
            "hair_finish": "grouped locks first, detail strands second",
            "fabric_finish": "medium folds, readable silhouette before texture",
            "metallic_finish": "limited bright edges, no mirror chrome",
        },
        "portrait_prompt_fragment": "clean comic linework, 2D Chinese manhua still",
        "general_prompt_fragment": "clean comic linework, 2-step cel shading, 2D Chinese manhua still",
    },
    "3d-scifi": {
        "aliases": {"3d-scifi", "scifi", "3d-kehuan", "3d-kehuan-style"},
        "display_name": "stylized 3D sci-fi",
        "realism_level": "stylized-semi-real",
        "line_and_render": {
            "line_quality": "minimal contour emphasis, form-first 3D rendering",
            "shadow_depth": "stylized volumetric shading with controlled bounce light",
            "skin_finish": "soft stylized 3D skin with restrained subsurface feel",
            "hair_finish": "sculpted strand masses with readable specular breakup",
            "fabric_finish": "material-driven folds with 3D form readability",
            "metallic_finish": "hard-surface specular control with clean sci-fi highlights",
        },
        "portrait_prompt_fragment": "stylized 3D rendering, animated sci-fi film portrait",
        "general_prompt_fragment": "stylized 3D rendering, controlled cinematic lighting, animated sci-fi film still",
    },
    "3d-xuanhuan": {
        "aliases": {"3d-xuanhuan", "xuanhuan", "3d-xuanhuan-style", "3d-fantasy"},
        "display_name": "stylized 3D xuanhuan",
        "realism_level": "stylized-semi-real",
        "line_and_render": {
            "line_quality": "minimal contour emphasis, form-first 3D rendering",
            "shadow_depth": "stylized volumetric shading with mystical light layering",
            "skin_finish": "soft stylized 3D skin with restrained glow",
            "hair_finish": "sculpted strand masses with flowing fantasy readability",
            "fabric_finish": "material-driven folds with layered fantasy silhouette",
            "metallic_finish": "ornamental specular highlights with controlled bloom",
        },
        "portrait_prompt_fragment": "stylized 3D rendering, animated xuanhuan film portrait",
        "general_prompt_fragment": "stylized 3D rendering, controlled cinematic lighting, animated xuanhuan fantasy film still",
    },
}


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
    if path.name == "项目档案":
        archive_dir = path
    else:
        archive_dir = path / "项目档案"
    if not archive_dir.exists():
        raise FileNotFoundError(f"Archive directory does not exist: {archive_dir}")
    return archive_dir


def normalize_preset(name: str) -> str:
    needle = name.strip().lower()
    for preset_name, preset in PRESETS.items():
        if needle == preset_name or needle in preset["aliases"]:
            return preset_name
    available = ", ".join(sorted(PRESETS))
    raise ValueError(f"Unknown preset: {name}. Available: {available}")


def deep_transform(obj: Any, transform: callable) -> Any:
    if isinstance(obj, dict):
        return {key: deep_transform(value, transform) for key, value in obj.items()}
    if isinstance(obj, list):
        return [deep_transform(value, transform) for value in obj]
    if isinstance(obj, str):
        return transform(obj)
    return obj


def prompt_replacements(target_preset: dict[str, Any]) -> list[tuple[str, str]]:
    replacements: list[tuple[str, str]] = []
    for preset in PRESETS.values():
        replacements.append((preset["general_prompt_fragment"], target_preset["general_prompt_fragment"]))
        replacements.append((preset["portrait_prompt_fragment"], target_preset["portrait_prompt_fragment"]))
    replacements.extend(
        [
            (
                "clean comic linework, 2-step cel shading, 2.5D Chinese webtoon animation still",
                target_preset["general_prompt_fragment"],
            ),
            (
                "clean comic linework, 2.5D Chinese webtoon animation still",
                target_preset["portrait_prompt_fragment"],
            ),
        ]
    )
    # Replace longer fragments first so we do not partially mutate a prompt twice.
    return sorted(set(replacements), key=lambda item: len(item[0]), reverse=True)


def replace_prompt_fragments(text: str, replacements: list[tuple[str, str]]) -> str:
    result = text
    for old, new in replacements:
        result = result.replace(old, new)
    return result


def update_style_bible(path: Path, preset: dict[str, Any]) -> bool:
    data = load_yaml(path)
    updated = copy.deepcopy(data)
    updated["core_format"] = preset["display_name"]
    updated["realism_level"] = preset["realism_level"]
    line_and_render = dict(updated.get("line_and_render", {}))
    line_and_render.update(preset["line_and_render"])
    updated["line_and_render"] = line_and_render
    if updated != data:
        dump_yaml(path, updated)
        return True
    return False


def update_prompt_pack_yaml(path: Path, replacements: list[tuple[str, str]]) -> bool:
    data = load_yaml(path)
    updated = deep_transform(data, lambda value: replace_prompt_fragments(value, replacements))
    if updated != data:
        dump_yaml(path, updated)
        return True
    return False


def update_execution_docs(archive_dir: Path, replacements: list[tuple[str, str]]) -> list[Path]:
    changed: list[Path] = []
    for path in sorted(archive_dir.rglob("batch-*.md")):
        original = path.read_text(encoding="utf-8")
        updated = replace_prompt_fragments(original, replacements)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            changed.append(path)
    return changed


def render_archive(archive_dir: Path) -> None:
    render_script = Path(__file__).with_name("render_project_archive.py")
    subprocess.run([sys.executable, str(render_script), str(archive_dir)], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Switch a project archive between reusable 2D/3D style presets."
    )
    parser.add_argument("project_or_archive_dir", help="Path to assets/<项目名> or assets/<项目名>/项目档案")
    parser.add_argument(
        "--preset",
        required=True,
        help="Preset name. Examples: 2d-manhua, 3d-scifi, 3d-xuanhuan",
    )
    parser.add_argument(
        "--skip-execution-docs",
        action="store_true",
        help="Do not rewrite batch/runbook Markdown files such as batch-01-prompts.md.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview which files would change without writing anything.",
    )
    args = parser.parse_args()

    archive_dir = resolve_archive_dir(args.project_or_archive_dir)
    preset_name = normalize_preset(args.preset)
    preset = PRESETS[preset_name]
    replacements = prompt_replacements(preset)

    yaml_targets = [
        archive_dir / "series" / "style-bible.yaml",
        archive_dir / "series" / "character-asset-prompt-pack.yaml",
        archive_dir / "series" / "scene-asset-prompt-pack.yaml",
        archive_dir / "series" / "prop-vfx-asset-prompt-pack.yaml",
    ]

    would_change: list[Path] = []
    if args.dry_run:
        for path in yaml_targets:
            if not path.exists():
                continue
            if path.name == "style-bible.yaml":
                data = load_yaml(path)
                preview = copy.deepcopy(data)
                preview["core_format"] = preset["display_name"]
                preview["realism_level"] = preset["realism_level"]
                line_and_render = dict(preview.get("line_and_render", {}))
                line_and_render.update(preset["line_and_render"])
                preview["line_and_render"] = line_and_render
            else:
                preview = deep_transform(load_yaml(path), lambda value: replace_prompt_fragments(value, replacements))
            if preview != load_yaml(path):
                would_change.append(path)
        if not args.skip_execution_docs:
            for path in sorted(archive_dir.rglob("batch-*.md")):
                original = path.read_text(encoding="utf-8")
                updated = replace_prompt_fragments(original, replacements)
                if updated != original:
                    would_change.append(path)
        print(f"Preset: {preset_name}")
        if would_change:
            print("Would update:")
            for path in would_change:
                print(f"- {path}")
        else:
            print("No changes needed.")
        return

    changed: list[Path] = []
    if (archive_dir / "series" / "style-bible.yaml").exists() and update_style_bible(
        archive_dir / "series" / "style-bible.yaml", preset
    ):
        changed.append(archive_dir / "series" / "style-bible.yaml")

    for path in yaml_targets[1:]:
        if path.exists() and update_prompt_pack_yaml(path, replacements):
            changed.append(path)

    if not args.skip_execution_docs:
        changed.extend(update_execution_docs(archive_dir, replacements))

    render_archive(archive_dir)

    print(f"Switched style preset to: {preset_name}")
    if changed:
        print("Updated:")
        for path in changed:
            print(f"- {path}")
    else:
        print("No canonical files required changes.")


if __name__ == "__main__":
    main()
