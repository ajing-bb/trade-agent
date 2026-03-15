#!/usr/bin/env python3
"""Render project archive Markdown views from canonical YAML sources."""

from __future__ import annotations

import argparse
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


def escape_cell(value: Any) -> str:
    if value is None:
        return "`missing`"
    text = str(value).replace("|", "\\|")
    return text


def format_status(status: str, kind: str) -> str:
    status_map = {
        "character": {
            "committed": "已落盘",
            "prompted": "已出 prompt，待落盘",
            "planned": "待设计",
        },
        "scene": {
            "committed": "已落盘",
            "prompted": "已出 prompt，待落盘",
            "planned": "待设计",
        },
        "prop_vfx": {
            "committed": "已落盘",
            "prompted": "已出 prompt，待落盘",
            "planned": "待设计",
        },
    }
    return status_map.get(kind, {}).get(status, status)


def generated_header(title: str, source_name: str) -> list[str]:
    return [
        f"# {title}",
        "",
        f"> Generated from `{source_name}`. Do not edit this Markdown manually.",
        "",
    ]


def render_bullets(items: list[str]) -> list[str]:
    lines: list[str] = []
    for item in items:
        lines.append(f"- {item}")
    return lines


def render_code_block(text: str) -> list[str]:
    return ["```text", text, "```"]


def render_character_bible(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Character Bible", yaml_path.name)
    lines.extend(
        [
            "| ID | 角色 | 叙事角色 | 当前状态 | 视觉锚点 | 资产根路径 |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for character in data["characters"]:
        anchors = "、".join(character.get("visual_anchors", []))
        asset_root = character.get("asset_root")
        asset_text = f"`{asset_root}/`" if asset_root else "`missing`"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(character['id'])}`",
                    escape_cell(character["name"]),
                    escape_cell(character["role"]),
                    escape_cell(format_status(character["status"], "character")),
                    escape_cell(anchors),
                    asset_text,
                ]
            )
            + " |"
        )
    lines.extend(["", "## 当前角色资产说明", ""])
    lines.extend(render_bullets(data.get("notes", [])))
    dump_text(md_path, "\n".join(lines))


def render_series_bible(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Series Bible", yaml_path.name)
    lines.extend(
        [
            "## 项目摘要",
            "",
            "| 字段 | 值 |",
            "| --- | --- |",
            f"| 项目 ID | `{escape_cell(data.get('project_id', ''))}` |",
            f"| 项目名 | {escape_cell(data.get('title', ''))} |",
            f"| 当前导入范围 | {escape_cell(data.get('current_ingested_range', ''))} |",
            f"| 作品形态 | {escape_cell(data.get('story_form', ''))} |",
            f"| 主叙事钩子 | {escape_cell(data.get('story_hook', ''))} |",
            "",
            "## 世界观硬规则",
            "",
        ]
    )
    for idx, rule in enumerate(data.get("world_rules", []), start=1):
        lines.append(f"{idx}. {rule}")
    lines.extend(["", "## 审美与制作规则", ""])
    for idx, rule in enumerate(data.get("production_rules", []), start=1):
        lines.append(f"{idx}. {rule}")
    lines.extend(["", "## Canonical 使用规则", ""])
    for idx, rule in enumerate(data.get("canonical_rules", []), start=1):
        lines.append(f"{idx}. {rule}")
    lines.extend(["", "## 稳定 ID 规则", ""])
    stable = data.get("stable_id_prefixes", {})
    labels = {
        "character": "角色",
        "location": "场景",
        "prop": "道具",
        "vfx": "特效",
        "shot": "镜头",
    }
    for key in ("character", "location", "prop", "vfx", "shot"):
        if key in stable:
            lines.append(f"- {labels[key]}：`{escape_cell(stable[key])}`")
    notes = data.get("current_import_notes", [])
    if notes:
        lines.extend(["", "## 当前导入说明", ""])
        lines.extend(render_bullets(notes))
    dump_text(md_path, "\n".join(lines))


def render_style_bible(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Style Bible", yaml_path.name)
    lines.extend(
        [
            "## Style Summary",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Project Style Name | {escape_cell(data.get('style_name', ''))} |",
            f"| Core Format | {escape_cell(data.get('core_format', ''))} |",
            f"| Overall Density | {escape_cell(data.get('overall_density', ''))} |",
            f"| Realism Level | {escape_cell(data.get('realism_level', ''))} |",
            f"| Reference Warning | {escape_cell('、'.join(data.get('reference_warning', [])))} |",
            "",
            "## Line and Render Rules",
            "",
            "| Category | Rule |",
            "| --- | --- |",
        ]
    )
    for key, value in data.get("line_and_render", {}).items():
        lines.append(f"| {escape_cell(key.replace('_', ' ').title())} | {escape_cell(value)} |")
    lines.extend(["", "## Color and Light Rules", "", "| Category | Rule |", "| --- | --- |"])
    cal = data.get("color_and_light", {})
    for key, value in cal.items():
        if isinstance(value, list):
            rendered = "、".join(value)
        elif isinstance(value, dict):
            rendered = "、".join(f"{k}: {v}" for k, v in value.items())
        else:
            rendered = str(value)
        lines.append(f"| {escape_cell(key.replace('_', ' ').title())} | {escape_cell(rendered)} |")
    lines.extend(["", "## World Design Rules", "", "| Category | Rule |", "| --- | --- |"])
    for key, value in data.get("world_design", {}).items():
        lines.append(f"| {escape_cell(key.replace('_', ' ').title())} | {escape_cell(value)} |")
    lines.extend(["", "## Camera and Composition Rules", "", "| Category | Rule |", "| --- | --- |"])
    for key, value in data.get("camera_rules", {}).items():
        lines.append(f"| {escape_cell(key.replace('_', ' ').title())} | {escape_cell(value)} |")
    lines.extend(["", "## Failure Boundaries", ""])
    lines.extend(render_bullets(data.get("failure_boundaries", [])))
    dump_text(md_path, "\n".join(lines))


def render_scene_bible(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Scene Bible", yaml_path.name)
    lines.extend(
        [
            "| ID | 场景 | 功能 | 核心锚点 | 当前状态 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for location in data["locations"]:
        time_label = "日" if location.get("time") == "day" else "夜"
        anchors = "、".join(location.get("anchors", []))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(location['id'])}`",
                    f"{escape_cell(location['name'])} / {time_label}",
                    escape_cell(location["function"]),
                    escape_cell(anchors),
                    escape_cell(format_status(location["status"], "scene")),
                ]
            )
            + " |"
        )
    lines.extend(["", "## 场景规则", ""])
    for idx, rule in enumerate(data.get("rules", []), start=1):
        lines.append(f"{idx}. {rule}")
    dump_text(md_path, "\n".join(lines))


def render_prop_vfx_bible(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Prop and VFX Bible", yaml_path.name)
    lines.extend(
        [
            "| ID | 类型 | 名称 | 功能 | 当前状态 |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for item in data.get("props", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['id'])}`",
                    "Prop" if item["id"].startswith("PROP_") else "Card",
                    escape_cell(item["name"]),
                    escape_cell(item.get("function", "")),
                    escape_cell(format_status(item["status"], "prop_vfx")),
                ]
            )
            + " |"
        )
    for item in data.get("vfx", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['id'])}`",
                    "VFX",
                    escape_cell(item["name"]),
                    escape_cell(item.get("function", "")),
                    escape_cell(format_status(item["status"], "prop_vfx")),
                ]
            )
            + " |"
        )
    lines.extend(["", "## VFX 分流规则", ""])
    for idx, rule in enumerate(data.get("rules", []), start=1):
        lines.append(f"{idx}. {rule}")
    dump_text(md_path, "\n".join(lines))


def render_asset_manifest(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    type_labels = {
        "script": "剧本",
        "character": "角色",
        "scene": "场景",
        "prop": "道具",
        "vfx": "VFX",
    }
    episode_label = yaml_path.parent.name.upper()
    lines = generated_header(f"{episode_label} Asset Manifest", yaml_path.name)
    lines.extend(
        [
            "## Source Assets",
            "",
            "| 类型 | ID | 状态 | 路径 |",
            "| --- | --- | --- | --- |",
        ]
    )
    for asset in data["assets"]:
        path = asset.get("path")
        path_text = f"`{path}`" if path else "`missing`"
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(type_labels.get(asset["type"], asset["type"])),
                    f"`{escape_cell(asset['id'])}`",
                    escape_cell(asset["status"]),
                    path_text,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Notes", ""])
    lines.extend(render_bullets(data.get("notes", [])))
    dump_text(md_path, "\n".join(lines))


def render_director_queue(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    episode_label = yaml_path.parent.name.upper()
    lines = generated_header(f"{episode_label} Director Queue", yaml_path.name)
    lines.extend(["## Queue Rules", ""])
    for key in ("blocked", "ready", "in_progress", "done"):
        value = data.get("queue_rules", {}).get(key)
        if value:
            lines.append(f"- `{key}`：{value}")
    lines.extend(
        [
            "",
            "| Shot ID | Purpose | Asset Gate | Primary Refs | Execution Mode | Queue Status | Next Action | Fallback |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in data["queue"]:
        gate = "、".join(f"`{asset}`" for asset in item.get("blocked_by_assets", []))
        if gate:
            gate = f"{gate} 未落盘"
        refs = "、".join(escape_cell(ref) for ref in item.get("primary_refs", []))
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['shot_id'])}`",
                    escape_cell(item["purpose"]),
                    escape_cell(gate),
                    escape_cell(refs),
                    f"`{escape_cell(item['execution_mode'])}`",
                    f"`{escape_cell(item['queue_status'])}`",
                    escape_cell(item.get("next_action", "")),
                    escape_cell(item.get("fallback", "")),
                ]
            )
            + " |"
        )
    status_notes = data.get("status_notes", [])
    if status_notes:
        lines.extend(["", "## Status Notes", ""])
        lines.extend(render_bullets(status_notes))
    dump_text(md_path, "\n".join(lines))


def render_breakdown(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    episode_label = yaml_path.parent.name.upper()
    lines = generated_header(f"{episode_label} Breakdown", yaml_path.name)
    manual_review_summary = data.get("manual_review_summary", [])
    lines.extend(
        [
            "## Project Summary",
            "",
            "| Field | Value |",
            "| --- | --- |",
            f"| Project Type | {escape_cell(data.get('project_type', ''))} |",
            f"| Target Style | {escape_cell(data.get('target_style', ''))} |",
            f"| Core Theme | {escape_cell(data.get('core_theme', ''))} |",
            f"| Core Continuity Risks | {escape_cell('、'.join(data.get('core_continuity_risks', [])))} |",
            f"| Manual Review Count | {escape_cell(len(manual_review_summary))} |",
        ]
    )
    if manual_review_summary:
        lines.extend(
            [
                "",
                "## Manual Review Summary",
                "",
                "| Scope | Target | Review Flags |",
                "| --- | --- | --- |",
            ]
        )
        for item in manual_review_summary:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{escape_cell(item.get('scope', ''))}`",
                        escape_cell(item.get("target_id", "")),
                        escape_cell("、".join(item.get("review_flags", [])) or "-"),
                    ]
                )
                + " |"
            )
    lines.extend(
        [
            "",
            "## Scene List",
            "",
            "| Scene ID | 单元 | 时间/地点 | 目的 | 角色 | 关键资产 | Review Flags |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for scene in data.get("scenes", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(scene['id'])}`",
                    escape_cell(scene.get("unit", "")),
                    escape_cell(scene.get("time_location", "")),
                    escape_cell(scene.get("purpose", "")),
                    escape_cell("、".join(scene.get("characters", []))),
                    escape_cell("、".join(scene.get("key_assets", []))),
                    escape_cell("、".join(scene.get("review_flags", [])) or "-"),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Shot List",
            "",
            "| Shot ID | Scene ID | Characters | Beat | Action Core | Camera Intent | Dialogue | Emotion | Difficulty | Required Assets | Review Flags |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for shot in data.get("shots", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(shot['id'])}`",
                    f"`{escape_cell(shot.get('scene_id', ''))}`",
                    escape_cell("、".join(shot.get("characters", []))),
                    escape_cell(shot.get("beat", "")),
                    escape_cell(shot.get("action_core", "")),
                    escape_cell(shot.get("camera_intent", "")),
                    escape_cell(shot.get("dialogue", "")),
                    escape_cell(shot.get("emotion", "")),
                    escape_cell(shot.get("difficulty", "")),
                    escape_cell("、".join(shot.get("required_assets", []))),
                    escape_cell("、".join(shot.get("review_flags", [])) or "-"),
                ]
            )
            + " |"
        )
    character_map = data.get("character_mention_map", [])
    if character_map:
        lines.extend(
            [
                "",
                "## Character Mention Map",
                "",
                "| Character | First Scene | Recurring Scenes | Dialogue Density | Asset Priority | Review Flags |",
                "| --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in character_map:
            lines.append(
                "| "
                + " | ".join(
                    [
                        escape_cell(item.get("character", "")),
                        f"`{escape_cell(item.get('first_scene', ''))}`",
                        escape_cell("、".join(item.get("recurring_scenes", []))),
                        escape_cell(item.get("dialogue_density", "")),
                        escape_cell(item.get("asset_priority", "")),
                        escape_cell("、".join(item.get("review_flags", [])) or "-"),
                    ]
                )
                + " |"
            )
    dialogue_notes = data.get("dialogue_and_emotion_notes", [])
    if dialogue_notes:
        lines.extend(
            [
                "",
                "## Dialogue and Emotion Notes",
                "",
                "| Shot ID | Speaker | Raw Tag | Delivery Mode | Dialogue Purpose | Emotion | Lip-Sync Sensitivity |",
                "| --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for item in dialogue_notes:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{escape_cell(item.get('shot_id', ''))}`",
                        escape_cell(item.get("speaker", "")),
                        escape_cell(item.get("raw_speaker_tag", "")),
                        f"`{escape_cell(item.get('delivery_mode', ''))}`",
                        escape_cell(item.get("dialogue_purpose", "")),
                        escape_cell(item.get("emotion", "")),
                        escape_cell(item.get("lip_sync_sensitivity", "")),
                    ]
                )
                + " |"
            )
    dump_text(md_path, "\n".join(lines))


def render_continuity_plan(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    episode_label = yaml_path.parent.name.upper()
    lines = generated_header(f"{episode_label} Continuity Plan", yaml_path.name)
    locks = data.get("high_priority_locks", [])
    if locks:
        lines.extend(["## 高优先级锁定项", ""])
        for idx, item in enumerate(locks, start=1):
            lines.append(f"{idx}. {item}")
        lines.append("")
    lines.extend(
        [
            "## Shot Build Policy",
            "",
            "| Shot ID | Build Method | Why |",
            "| --- | --- | --- |",
        ]
    )
    for item in data.get("shot_build_policy", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{escape_cell(item['shot_id'])}`",
                    f"`{escape_cell(item.get('build_method', ''))}`",
                    escape_cell(item.get("why", "")),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Continuity Risks",
            "",
            "| 风险 | 说明 | 对策 |",
            "| --- | --- | --- |",
        ]
    )
    for risk in data.get("risks", []):
        lines.append(
            "| "
            + " | ".join(
                [
                    escape_cell(risk.get("name", "")),
                    escape_cell(risk.get("description", "")),
                    escape_cell(risk.get("mitigation", "")),
                ]
            )
            + " |"
        )
    dump_text(md_path, "\n".join(lines))


def render_script_normalized(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    episode_label = yaml_path.parent.name.upper()
    lines = generated_header(f"{episode_label} Script Normalized", yaml_path.name)
    lines.extend(["## Source", ""])
    source_notes = data.get("source_notes", [])
    if source_notes:
        lines.extend(render_bullets(source_notes))
    else:
        lines.append(f"- 原文件：`{data.get('source_file', '')}`")
    for section in data.get("sections", []):
        lines.extend(["", f"## {section.get('title', section['id'])}", ""])
        time_location = section.get("time_location")
        if time_location:
            lines.append(time_location)
        for beat in section.get("beats", []):
            lines.append(beat)
    dump_text(md_path, "\n".join(lines))


def render_character_prompt_pack(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Character Asset Prompt Pack", yaml_path.name)
    lines.extend(["## Rules", ""])
    for key, value in data.get("rules", {}).items():
        lines.append(f"- `{key}`: {value}")
    scope = data.get("scope", [])
    if scope:
        lines.extend(["", "## Scope", ""])
        lines.extend(render_bullets([f"`{item}`" for item in scope]))
    for item in data.get("characters", []):
        lines.extend(["", f"## `{item['id']}`｜{item['name']}", ""])
        lines.extend(["### Summary", ""])
        lines.append(f"- `status`: {item.get('status', '')}")
        lines.append(f"- `target_path`: `{item.get('target_path', 'missing')}`")
        if item.get("reference_assets"):
            lines.append(
                "- `reference_assets`: "
                + "、".join(f"`{asset}`" for asset in item["reference_assets"])
            )
        if item.get("required_outputs"):
            lines.append(
                "- `required_outputs`: "
                + "、".join(f"`{output}`" for output in item["required_outputs"])
            )
        if item.get("visual_anchors"):
            lines.append("- `visual_anchors`: " + "、".join(item["visual_anchors"]))
        midjourney = item.get("midjourney", {})
        if midjourney:
            lines.extend(["", "### Midjourney", ""])
            for name, prompt in midjourney.items():
                lines.extend([f"#### {name}", ""])
                lines.extend(render_code_block(prompt))
                lines.append("")
            if lines[-1] == "":
                lines.pop()
        banana = item.get("banana", {})
        if banana:
            lines.extend(["", "### Banana Pro", ""])
            for name, prompt in banana.items():
                lines.extend([f"#### {name}", ""])
                lines.extend(render_code_block(prompt))
                lines.append("")
            if lines[-1] == "":
                lines.pop()
        archive_updates = item.get("archive_updates", [])
        if archive_updates:
            lines.extend(["", "### Archive Updates", ""])
            lines.extend(render_bullets([f"`{path}`" for path in archive_updates]))
    dump_text(md_path, "\n".join(lines))


def render_scene_prompt_pack(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Scene Asset Prompt Pack", yaml_path.name)
    lines.extend(["## Rules", ""])
    for key, value in data.get("rules", {}).items():
        lines.append(f"- `{key}`: {value}")
    for item in data.get("locations", []):
        lines.extend(["", f"## `{item['id']}`", ""])
        lines.extend(["### Summary", ""])
        lines.append(f"- `status`: {item.get('status', '')}")
        if item.get("required_outputs"):
            lines.append(
                "- `required_outputs`: "
                + "、".join(f"`{output}`" for output in item["required_outputs"])
            )
        midjourney = item.get("midjourney", {})
        if midjourney:
            lines.extend(["", "### Midjourney", ""])
            for name, prompt in midjourney.items():
                lines.extend([f"#### {name}", ""])
                lines.extend(render_code_block(prompt))
                lines.append("")
            if lines[-1] == "":
                lines.pop()
        banana = item.get("banana", {})
        if banana:
            lines.extend(["", "### Banana Pro", ""])
            for name, prompt in banana.items():
                lines.extend([f"#### {name}", ""])
                lines.extend(render_code_block(prompt))
                lines.append("")
            if lines[-1] == "":
                lines.pop()
    dump_text(md_path, "\n".join(lines))


def render_prop_vfx_prompt_pack(yaml_path: Path, md_path: Path) -> None:
    data = load_yaml(yaml_path)
    lines = generated_header("Prop and VFX Asset Prompt Pack", yaml_path.name)
    lines.extend(["## Rules", ""])
    for key, value in data.get("rules", {}).items():
        lines.append(f"- `{key}`: {value}")
    for section_name, items in (("Props", data.get("props", [])), ("VFX", data.get("vfx", []))):
        if not items:
            continue
        lines.extend(["", f"## {section_name}", ""])
        for item in items:
            lines.extend(["", f"### `{item['id']}`", ""])
            lines.append(f"- `status`: {item.get('status', '')}")
            midjourney = item.get("midjourney", {})
            if midjourney:
                lines.extend(["", "#### Midjourney", ""])
                for name, prompt in midjourney.items():
                    lines.extend([f"##### {name}", ""])
                    lines.extend(render_code_block(prompt))
                    lines.append("")
                if lines[-1] == "":
                    lines.pop()
            banana = item.get("banana", {})
            if banana:
                lines.extend(["", "#### Banana Pro", ""])
                for name, prompt in banana.items():
                    lines.extend([f"##### {name}", ""])
                    lines.extend(render_code_block(prompt))
                    lines.append("")
                if lines[-1] == "":
                    lines.pop()
    dump_text(md_path, "\n".join(lines))


def render_project_archive(project_dir: Path) -> None:
    series_dir = project_dir / "series"
    series_bible_yaml = series_dir / "series-bible.yaml"
    if series_bible_yaml.exists():
        render_series_bible(series_bible_yaml, series_dir / "series-bible.md")
    style_bible_yaml = series_dir / "style-bible.yaml"
    if style_bible_yaml.exists():
        render_style_bible(style_bible_yaml, series_dir / "style-bible.md")
    render_character_bible(series_dir / "character-bible.yaml", series_dir / "character-bible.md")
    render_scene_bible(series_dir / "scene-bible.yaml", series_dir / "scene-bible.md")
    render_prop_vfx_bible(series_dir / "prop-vfx-bible.yaml", series_dir / "prop-vfx-bible.md")
    character_prompt_pack_yaml = series_dir / "character-asset-prompt-pack.yaml"
    if character_prompt_pack_yaml.exists():
        render_character_prompt_pack(
            character_prompt_pack_yaml, series_dir / "character-asset-prompt-pack.md"
        )
    scene_prompt_pack_yaml = series_dir / "scene-asset-prompt-pack.yaml"
    if scene_prompt_pack_yaml.exists():
        render_scene_prompt_pack(scene_prompt_pack_yaml, series_dir / "scene-asset-prompt-pack.md")
    prop_prompt_pack_yaml = series_dir / "prop-vfx-asset-prompt-pack.yaml"
    if prop_prompt_pack_yaml.exists():
        render_prop_vfx_prompt_pack(
            prop_prompt_pack_yaml, series_dir / "prop-vfx-asset-prompt-pack.md"
        )
    episodes_dir = project_dir / "episodes"
    for episode_dir in sorted(episodes_dir.glob("ep*")):
        breakdown_yaml = episode_dir / "breakdown.yaml"
        continuity_yaml = episode_dir / "continuity-plan.yaml"
        script_yaml = episode_dir / "script-normalized.yaml"
        asset_yaml = episode_dir / "asset-manifest.yaml"
        director_yaml = episode_dir / "director-queue.yaml"
        if breakdown_yaml.exists():
            render_breakdown(breakdown_yaml, episode_dir / "breakdown.md")
        if continuity_yaml.exists():
            render_continuity_plan(continuity_yaml, episode_dir / "continuity-plan.md")
        if script_yaml.exists():
            render_script_normalized(script_yaml, episode_dir / "script-normalized.md")
        if asset_yaml.exists():
            render_asset_manifest(asset_yaml, episode_dir / "asset-manifest.md")
        if director_yaml.exists():
            render_director_queue(director_yaml, episode_dir / "director-queue.md")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Render project archive Markdown files from canonical YAML files."
    )
    parser.add_argument("project_archive_dir", help="Path to assets/<项目名>/项目档案")
    args = parser.parse_args()
    render_project_archive(Path(args.project_archive_dir))


if __name__ == "__main__":
    main()
