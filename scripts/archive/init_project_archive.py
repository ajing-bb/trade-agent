#!/usr/bin/env python3
"""Initialize an AI manhua project archive from a source DOCX."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import yaml


WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
SCENE_SLUG_RE = re.compile(r"^(?P<slug>\d{2}-\d+)\s+(?P<time_location>.+)$")
ACTION_PREFIXES = ("△", "▲", "▽", "▼", "◆", "■", "●", "○", "※")
VISUAL_CUT_KEYWORDS = ("镜头切换", "镜头定格", "下一刻", "忽然", "轰", "光柱", "异象", "火光", "天空")
EMOTION_KEYWORDS = (
    "震惊",
    "惊喜",
    "愤怒",
    "紧张",
    "坚定",
    "冷笑",
    "轻蔑",
    "惊诧",
    "疲惫",
    "疑惑",
    "压迫",
    "失落",
)
CAMERA_KEYWORDS = (
    "镜头",
    "特写",
    "近景",
    "中景",
    "远景",
    "全景",
    "俯拍",
    "仰拍",
    "平视",
    "推近",
    "拉远",
    "跟拍",
    "转场",
    "CUT TO",
    "DISSOLVE",
    "FADE IN",
    "FADE OUT",
    "SMASH CUT",
    "MONTAGE",
)
REACTION_KEYWORDS = ("震惊", "惊喜", "惊诧", "愣住", "冷笑", "轻蔑", "疲惫", "皱眉", "眼神", "大笑")
VFX_KEYWORDS = ("异象", "光柱", "火光", "火轮", "红绫", "长枪", "金色", "赤红", "法相", "火焰", "巨震")
AUDIO_CUE_KEYWORDS = ("音效", "SFX", "BGM", "音乐", "配乐", "广播", "电话铃", "提示音", "机械音")
MEMORY_CUE_KEYWORDS = ("闪回", "回忆", "梦境", "幻想", "记忆片段", "幻觉")
TITLE_CARD_KEYWORDS = ("黑屏", "字幕", "字卡", "屏幕文字", "标题卡", "片名卡")
TRANSITION_KEYWORDS = (
    "CUT TO",
    "DISSOLVE",
    "FADE IN",
    "FADE OUT",
    "SMASH CUT",
    "MONTAGE",
    "转场",
    "切至",
    "切到",
    "淡入",
    "淡出",
    "蒙太奇",
)
MESSAGE_CUE_KEYWORDS = ("手机", "短信", "微信", "消息", "弹窗", "群聊", "通知", "聊天记录")
SKILL_CUE_KEYWORDS = ("技能", "招式", "法术", "术式", "绝技", "必杀", "剑招", "拳法", "阵法", "施展", "发动")
GENERIC_EXTRA_RE = re.compile(r"^(学生|跟班)\d+$")
ASSET_KEYWORDS = (
    "抽卡池",
    "卡片",
    "雕像",
    "翅膀",
    "天空",
    "光柱",
    "火轮",
    "长枪",
    "红绫",
    "办公室",
    "食堂",
    "操场",
    "宿舍",
)
DELIVERY_MODE_LABELS = {
    "spoken": "spoken",
    "os": "os",
    "vo": "vo",
    "narration": "narration",
    "offscreen": "offscreen",
    "broadcast": "broadcast",
    "phone": "phone",
    "system": "system",
    "sfx": "sfx",
    "bgm": "bgm",
    "caption": "caption",
    "message": "message",
}
DELIVERY_MARKERS = {
    "OS": "os",
    "VO": "vo",
    "旁白": "narration",
    "画外音": "offscreen",
    "画外旁白": "offscreen",
    "广播": "broadcast",
    "广播音": "broadcast",
    "广播声": "broadcast",
    "耳麦": "broadcast",
    "耳机里": "broadcast",
    "电话": "phone",
    "电话音": "phone",
    "来电": "phone",
    "手机来电": "phone",
    "通话": "phone",
    "系统": "system",
    "系统音": "system",
    "系统提示": "system",
    "提示音": "system",
    "系统播报": "system",
    "SFX": "sfx",
    "音效": "sfx",
    "音效声": "sfx",
    "BGM": "bgm",
    "音乐": "bgm",
    "配乐": "bgm",
    "字幕": "caption",
    "字卡": "caption",
    "屏幕文字": "caption",
    "画面字幕": "caption",
    "手机消息": "message",
    "消息提示": "message",
    "短信提示": "message",
    "聊天记录": "message",
    "弹窗提示": "message",
    "通知": "message",
    "内心独白": "os",
    "内心": "os",
    "心声": "os",
}


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"Expected mapping in {path}")
    return data


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, allow_unicode=True, sort_keys=False)


def best_effort_relative(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def discover_source_script(project_root: Path, override: str | None) -> Path:
    if override:
        path = Path(override).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Source script does not exist: {path}")
        return path
    matches = sorted((project_root / "剧本").glob("*.docx"))
    if len(matches) == 1:
        return matches[0].resolve()
    if not matches:
        raise FileNotFoundError("No .docx file found under 剧本/. Pass --source-script explicitly.")
    raise ValueError("Multiple .docx files found under 剧本/. Pass --source-script explicitly.")


def extract_docx_paragraphs(docx_path: Path) -> list[str]:
    with zipfile.ZipFile(docx_path) as archive:
        xml = archive.read("word/document.xml")
    root = ElementTree.fromstring(xml)
    paragraphs: list[str] = []
    for paragraph in root.findall(".//w:p", WORD_NAMESPACE):
        texts = [node.text or "" for node in paragraph.findall(".//w:t", WORD_NAMESPACE)]
        content = "".join(texts).replace("\u3000", " ").strip()
        if content:
            paragraphs.append(content)
    return paragraphs


def normalize_unit_id(heading: str, section_index: int) -> str:
    heading = heading.strip()
    if heading.startswith("开场"):
        return "opening"
    if heading.startswith("序章"):
        return "prologue"
    match = re.match(r"^第([0-9]+)集", heading)
    if match:
        return f"episode_{int(match.group(1))}"
    match = re.match(r"(?i)^episode\s*([0-9]+)", heading)
    if match:
        return f"episode_{int(match.group(1))}"
    return f"section_{section_index}"


def split_into_sections(paragraphs: list[str]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    heading_pattern = re.compile(r"^(开场|序章|第[0-9]+集|Episode\s*[0-9]+)", re.IGNORECASE)

    for paragraph in paragraphs:
        if heading_pattern.match(paragraph):
            current = {
                "id": normalize_unit_id(paragraph, len(sections) + 1),
                "title": paragraph,
                "time_location": "",
                "location": "",
                "summary": "",
                "beats": [],
            }
            sections.append(current)
            continue
        if current is None:
            current = {
                "id": "section_1",
                "title": "Imported Script",
                "time_location": "",
                "location": "",
                "summary": "",
                "beats": [],
            }
            sections.append(current)
        current["beats"].append(paragraph)
    return sections


def script_normalized_data(source_label: str, sections: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "source_file": source_label,
        "covered_units": [section["id"] for section in sections],
        "source_notes": [f"原文件：{source_label}", "由 init-project-archive.py 初次导入。"],
        "sections": sections,
    }


def scene_id(episode_id: str, index: int) -> str:
    return f"{episode_id.upper()}-S{index:02d}"


def normalize_delivery_marker(token: str) -> str | None:
    token = token.strip()
    if not token:
        return None
    upper = token.upper()
    if upper in DELIVERY_MARKERS:
        return DELIVERY_MARKERS[upper]
    return DELIVERY_MARKERS.get(token)


def parse_dialogue_entry(line: str) -> dict[str, Any] | None:
    stripped = line.strip()
    if "：" not in stripped and ":" not in stripped:
        return None
    separator = "：" if "：" in stripped else ":"
    raw_label, dialogue = stripped.split(separator, 1)
    raw_label = raw_label.strip()
    dialogue = dialogue.strip()
    if not raw_label or not dialogue:
        return None

    paren_tokens = [token.strip() for token in re.findall(r"[（(]([^）)]+)[）)]", raw_label) if token.strip()]
    label_without_paren = re.sub(r"[（(][^）)]+[）)]", "", raw_label).strip()

    delivery_mode = "spoken"
    extra_hints: list[str] = []
    for token in paren_tokens:
        normalized = normalize_delivery_marker(token)
        if normalized:
            delivery_mode = normalized
        else:
            extra_hints.append(token)

    speaker = label_without_paren
    normalized = normalize_delivery_marker(label_without_paren)
    if normalized:
        delivery_mode = normalized
        speaker = ""
    else:
        for marker, mode in sorted(DELIVERY_MARKERS.items(), key=lambda item: len(item[0]), reverse=True):
            if label_without_paren.upper().endswith(marker.upper()) and len(label_without_paren) > len(marker):
                speaker = label_without_paren[: -len(marker)].strip()
                delivery_mode = mode
                break

    speaker = speaker.strip()
    if speaker in {"VO", "旁白", "画外音"}:
        speaker = ""
    return {
        "raw_speaker_tag": raw_label,
        "speaker": speaker,
        "delivery_mode": delivery_mode,
        "dialogue": dialogue,
        "hint": " / ".join(extra_hints),
    }


def speaker_from_dialogue(line: str) -> str | None:
    entry = parse_dialogue_entry(line)
    if not entry:
        return None
    return entry["speaker"] or None


def infer_emotion(text: str) -> str:
    for keyword in EMOTION_KEYWORDS:
        if keyword in text:
            return keyword
    return ""


def infer_camera_intent(lines: list[str], has_dialogue: bool) -> str:
    joined = " ".join(lines)
    if "镜头定格" in joined:
        return "freeze / reveal"
    if "镜头切换" in joined:
        return "cut"
    if "仰" in joined and "看" in joined:
        return "low-angle reveal"
    if has_dialogue:
        return "dialogue coverage"
    if any(token in joined for token in ("黑压压", "到处都是", "整片天空", "整个城市")):
        return "wide reveal"
    return "story beat coverage"


def infer_difficulty(lines: list[str], characters: list[str]) -> str:
    joined = " ".join(lines)
    if len(characters) > 2 or any(keyword in joined for keyword in ("异象", "光柱", "火光", "巨震", "法相")):
        return "high"
    if len(characters) == 2 or any(keyword in joined for keyword in ("卡片", "抽卡池", "雕像", "风云人物")):
        return "medium"
    return "low"


def infer_lip_sync_sensitivity(dialogue: str) -> str:
    length = len(dialogue)
    if length >= 40:
        return "high"
    if length >= 16:
        return "medium"
    return "low"


def parse_action_entry(line: str) -> dict[str, str] | None:
    stripped = line.strip()
    if not stripped:
        return None
    raw_marker = ""
    text = stripped
    if stripped[0] in ACTION_PREFIXES:
        raw_marker = stripped[0]
        text = stripped[1:].strip()
    elif "：" in stripped or ":" in stripped:
        return None

    if not text:
        return None
    action_type = "action"
    upper_text = text.upper()
    if any(keyword in text for keyword in TITLE_CARD_KEYWORDS):
        action_type = "title_card"
    elif any(keyword in text for keyword in MEMORY_CUE_KEYWORDS):
        action_type = "memory"
    elif any(keyword in text for keyword in MESSAGE_CUE_KEYWORDS):
        action_type = "message"
    elif any(keyword in text for keyword in AUDIO_CUE_KEYWORDS):
        action_type = "audio_cue"
    elif any(keyword in upper_text for keyword in TRANSITION_KEYWORDS) or any(keyword in text for keyword in TRANSITION_KEYWORDS):
        action_type = "transition"
    elif any(keyword in text for keyword in SKILL_CUE_KEYWORDS):
        action_type = "skill_callout"
    elif any(keyword in upper_text for keyword in CAMERA_KEYWORDS) or any(keyword in text for keyword in CAMERA_KEYWORDS):
        action_type = "camera"
    elif any(keyword in text for keyword in VFX_KEYWORDS):
        action_type = "vfx"
    elif any(keyword in text for keyword in REACTION_KEYWORDS):
        action_type = "reaction"
    elif any(keyword in text for keyword in ("走", "站", "坐", "起身", "转身", "抬手", "按下", "离开", "出现")):
        action_type = "blocking"
    return {
        "raw_marker": raw_marker,
        "action_type": action_type,
        "text": text,
    }


def clean_line(line: str) -> str:
    action = parse_action_entry(line)
    if action:
        return action["text"]
    return line.lstrip("".join(ACTION_PREFIXES)).strip()


def summarize_text(lines: list[str], limit: int = 28) -> str:
    parts = [clean_line(line) for line in lines if clean_line(line)]
    text = " / ".join(parts[:2])
    if len(text) > limit:
        return text[: limit - 1].rstrip() + "…"
    return text


def find_asset_keywords(lines: list[str], location_raw: str) -> list[str]:
    found: list[str] = []
    joined = " ".join(lines)
    if location_raw:
        found.append(location_raw)
    for keyword in ASSET_KEYWORDS:
        if keyword in joined and keyword not in found:
            found.append(keyword)
    return found


def split_scene_blocks(section: dict[str, Any]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None
    for beat in section.get("beats", []):
        match = SCENE_SLUG_RE.match(beat)
        if match:
            time_location = match.group("time_location").strip()
            location_raw = time_location.split(maxsplit=1)[1] if " " in time_location else ""
            current = {
                "slug": match.group("slug"),
                "time_location": time_location,
                "location_raw": location_raw,
                "lines": [],
            }
            blocks.append(current)
            continue
        if current is None:
            current = {
                "slug": "",
                "time_location": section.get("time_location", ""),
                "location_raw": section.get("location", ""),
                "lines": [],
            }
            blocks.append(current)
        current["lines"].append(beat)
    return [block for block in blocks if block.get("lines")]


def extract_character_mentions(lines: list[str], known_names: set[str]) -> list[str]:
    found: list[str] = []
    for line in lines:
        entry = parse_dialogue_entry(line)
        speaker = entry["speaker"] if entry else None
        if speaker and speaker not in found:
            found.append(speaker)
        for name in known_names:
            if name in line and name not in found:
                found.append(name)
    return found


def build_scene_shots(scene_identifier: str, block: dict[str, Any], known_names: set[str]) -> list[dict[str, Any]]:
    groups: list[list[str]] = []
    current_group: list[str] = []
    current_kind: str | None = None

    for line in block["lines"]:
        speaker = speaker_from_dialogue(line)
        kind = "dialogue" if speaker else "action"
        should_split = False
        if current_group:
            if kind != current_kind:
                should_split = True
            elif kind == "action" and any(keyword in line for keyword in VISUAL_CUT_KEYWORDS):
                should_split = True
        if should_split:
            groups.append(current_group)
            current_group = []
        current_group.append(line)
        current_kind = kind
    if current_group:
        groups.append(current_group)

    shots: list[dict[str, Any]] = []
    for index, lines in enumerate(groups, start=1):
        dialogue_items: list[dict[str, Any]] = []
        action_items: list[dict[str, str]] = []
        emotion_parts: list[str] = []
        for line in lines:
            entry = parse_dialogue_entry(line)
            if entry:
                dialogue_items.append(entry)
                if entry.get("hint"):
                    emotion_parts.append(entry["hint"])
                continue
            action = parse_action_entry(line)
            if action:
                action_items.append(action)
                if action["action_type"] == "reaction":
                    inferred = infer_emotion(action["text"])
                    if inferred:
                        emotion_parts.append(inferred)
                continue
        characters = extract_character_mentions(lines, known_names)
        emotion = emotion_parts[0] if emotion_parts else infer_emotion(" ".join(lines))
        dialogue_text = " / ".join(
            (
                f"{item['speaker']}[{item['delivery_mode']}]：{item['dialogue']}"
                if item["speaker"]
                else f"[{item['delivery_mode']}]：{item['dialogue']}"
            )
            for item in dialogue_items
        )
        shots.append(
            {
                "id": f"{scene_identifier}-SH{index:02d}",
                "scene_id": scene_identifier,
                "characters": characters,
                "beat": summarize_text(lines),
                "action_core": summarize_text([item["text"] for item in action_items], limit=24),
                "camera_intent": infer_camera_intent(lines, bool(dialogue_items)),
                "dialogue": dialogue_text,
                "dialogue_items": dialogue_items,
                "dialogue_modes": [item["delivery_mode"] for item in dialogue_items],
                "action_items": action_items,
                "action_types": [item["action_type"] for item in action_items],
                "emotion": emotion,
                "required_assets": find_asset_keywords(lines, block.get("location_raw", "")),
                "difficulty": infer_difficulty(lines, characters),
                "source_lines": lines,
            }
        )
    return shots


def build_breakdown_structures(episode_id: str, sections: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    known_names = {
        speaker
        for section in sections
        for line in section.get("beats", [])
        for speaker in [speaker_from_dialogue(line)]
        if speaker
    }
    scenes: list[dict[str, Any]] = []
    shots: list[dict[str, Any]] = []
    dialogue_notes: list[dict[str, Any]] = []
    character_stats: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"first_scene": "", "recurring_scenes": [], "dialogue_count": 0}
    )

    scene_counter = 1
    for section in sections:
        for block in split_scene_blocks(section):
            scene_identifier = scene_id(episode_id, scene_counter)
            scene_counter += 1
            scene_shots = build_scene_shots(scene_identifier, block, known_names)
            scene_characters = []
            for shot in scene_shots:
                for character in shot.get("characters", []):
                    if character not in scene_characters:
                        scene_characters.append(character)
                        stats = character_stats[character]
                        if not stats["first_scene"]:
                            stats["first_scene"] = scene_identifier
                        if scene_identifier not in stats["recurring_scenes"]:
                            stats["recurring_scenes"].append(scene_identifier)
                for item in shot.get("dialogue_items", []):
                    speaker = item.get("speaker", "")
                    dialogue = item.get("dialogue", "")
                    if speaker:
                        character_stats[speaker]["dialogue_count"] += 1
                        dialogue_notes.append(
                            {
                                "shot_id": shot["id"],
                                "speaker": speaker,
                                "raw_speaker_tag": item.get("raw_speaker_tag", ""),
                                "delivery_mode": item.get("delivery_mode", "spoken"),
                                "dialogue_purpose": summarize_text([dialogue], limit=24) or "dialogue",
                                "emotion": shot.get("emotion", ""),
                                "lip_sync_sensitivity": infer_lip_sync_sensitivity(dialogue),
                            }
                        )
                    elif dialogue:
                        dialogue_notes.append(
                            {
                                "shot_id": shot["id"],
                                "speaker": "",
                                "raw_speaker_tag": item.get("raw_speaker_tag", ""),
                                "delivery_mode": item.get("delivery_mode", "spoken"),
                                "dialogue_purpose": summarize_text([dialogue], limit=24) or "dialogue",
                                "emotion": shot.get("emotion", ""),
                                "lip_sync_sensitivity": "low" if item.get("delivery_mode") != "spoken" else infer_lip_sync_sensitivity(dialogue),
                            }
                        )
            scenes.append(
                {
                    "id": scene_identifier,
                    "unit": section["id"],
                    "time_location": block.get("time_location", ""),
                    "location_id": "",
                    "location_raw": block.get("location_raw", ""),
                    "purpose": summarize_text(block["lines"]),
                    "characters": scene_characters,
                    "key_assets": find_asset_keywords(block["lines"], block.get("location_raw", "")),
                    "review_flags": [],
                }
            )
            shots.extend(scene_shots)

    character_map: list[dict[str, Any]] = []
    for character, stats in sorted(character_stats.items(), key=lambda item: item[1]["first_scene"]):
        density = "high" if stats["dialogue_count"] >= 4 else "medium" if stats["dialogue_count"] >= 2 else "low"
        priority = "high" if len(stats["recurring_scenes"]) >= 2 else "medium"
        character_map.append(
            {
                "character": character,
                "first_scene": stats["first_scene"],
                "recurring_scenes": stats["recurring_scenes"][1:],
                "dialogue_density": density,
                "asset_priority": priority,
                "review_flags": [],
            }
        )

    return scenes, shots, character_map, dialogue_notes


def scene_review_flags(scene: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    if scene.get("location_raw") and not scene.get("location_id"):
        flags.append("location_binding_needed")
    if scene.get("key_assets"):
        flags.append("canonical_asset_binding_needed")
    return flags


def shot_review_flags(shot: dict[str, Any], high_lip_sync_shots: set[str]) -> list[str]:
    flags: list[str] = []
    if shot.get("difficulty") == "high":
        flags.append("high_difficulty")
    if len(shot.get("characters", [])) > 2:
        flags.append("many_characters")
    required_assets = set(shot.get("required_assets", []))
    if "vfx" in shot.get("action_types", []) or any(keyword in required_assets for keyword in VFX_KEYWORDS):
        flags.append("strong_vfx")
    if shot.get("id", "") in high_lip_sync_shots:
        flags.append("lip_sync_high")
    return flags


def character_review_flags(item: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    character = item.get("character", "")
    if GENERIC_EXTRA_RE.match(character):
        flags.append("generic_extra_candidate")
    return flags


def manual_review_summary(
    scenes: list[dict[str, Any]], shots: list[dict[str, Any]], character_map: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    summary: list[dict[str, Any]] = []
    for scope, items, id_field in (
        ("scene", scenes, "id"),
        ("shot", shots, "id"),
        ("character", character_map, "character"),
    ):
        for item in items:
            flags = item.get("review_flags", [])
            if flags:
                summary.append(
                    {
                        "scope": scope,
                        "target_id": item.get(id_field, ""),
                        "review_flags": list(flags),
                    }
                )
    return summary


def breakdown_data(episode_id: str, sections: list[dict[str, Any]]) -> dict[str, Any]:
    scenes, shots, character_map, dialogue_notes = build_breakdown_structures(episode_id, sections)
    high_lip_sync_shots = {
        item["shot_id"]
        for item in dialogue_notes
        if item.get("delivery_mode") == "spoken" and item.get("lip_sync_sensitivity") == "high"
    }
    for scene in scenes:
        scene["review_flags"] = scene_review_flags(scene)
    for shot in shots:
        shot["review_flags"] = shot_review_flags(shot, high_lip_sync_shots)
    for item in character_map:
        item["review_flags"] = character_review_flags(item)
    theme_counter = Counter()
    for section in sections:
        for beat in section.get("beats", []):
            for keyword in ("抽卡", "神明", "学院", "异象", "校园", "哪吒", "通天教主"):
                if keyword in beat:
                    theme_counter[keyword] += 1
    core_theme = " / ".join(word for word, _ in theme_counter.most_common(3))
    risk_counter = []
    if any(shot.get("difficulty") == "high" for shot in shots):
        risk_counter.append("高风险镜头已自动标出")
    if any("异象" in shot.get("beat", "") for shot in shots):
        risk_counter.append("强 VFX 与剧情转折并存")
    if sum(1 for shot in shots if len(shot.get("characters", [])) > 2) > 0:
        risk_counter.append("多人镜头存在一致性压力")
    return {
        "project_type": "AI漫剧",
        "target_style": "",
        "core_theme": core_theme,
        "core_continuity_risks": risk_counter,
        "manual_review_summary": manual_review_summary(scenes, shots, character_map),
        "scenes": scenes,
        "shots": shots,
        "character_mention_map": character_map,
        "dialogue_and_emotion_notes": dialogue_notes,
    }


def ensure_archive(project_root: Path, source_script: Path, episode_id: str) -> None:
    archive_dir = project_root / "项目档案"
    if archive_dir.exists():
        return
    reset_script = Path(__file__).with_name("reset_project_creation.py")
    subprocess.run(
        [
            sys.executable,
            str(reset_script),
            str(project_root),
            "--mode",
            "archive-only",
            "--source-script",
            str(source_script),
            "--episode-id",
            episode_id,
            "--rebuild-skeleton",
            "--yes",
        ],
        check=True,
    )


def archive_has_imported_content(script_yaml: Path, breakdown_yaml: Path) -> bool:
    if script_yaml.exists():
        script_data = load_yaml(script_yaml)
        if script_data.get("sections"):
            return True
    if breakdown_yaml.exists():
        breakdown_data = load_yaml(breakdown_yaml)
        if breakdown_data.get("scenes") or breakdown_data.get("shots"):
            return True
    return False


def render_archive(project_root: Path) -> None:
    render_script = Path(__file__).with_name("render_project_archive.py")
    subprocess.run(
        [sys.executable, str(render_script), str(project_root / "项目档案")],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize 项目档案 from a source DOCX for ai-video-consistency."
    )
    parser.add_argument("project_root", help="Path to assets/<项目名>")
    parser.add_argument(
        "--source-script",
        help="Optional path to the source .docx. Required if 剧本/ contains zero or multiple .docx files.",
    )
    parser.add_argument(
        "--episode-id",
        default="ep001",
        help="Episode folder to initialize.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing script-normalized.yaml and breakdown.yaml for the target episode.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned writes without modifying files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    project_root = Path(args.project_root).resolve()
    source_script = discover_source_script(project_root, args.source_script)
    source_label = best_effort_relative(source_script, Path.cwd())
    paragraphs = extract_docx_paragraphs(source_script)
    sections = split_into_sections(paragraphs)
    if not sections:
        raise ValueError(f"No readable paragraphs were extracted from {source_script}")

    archive_dir = project_root / "项目档案"
    episode_dir = archive_dir / "episodes" / args.episode_id
    script_yaml = episode_dir / "script-normalized.yaml"
    breakdown_yaml = episode_dir / "breakdown.yaml"

    print(f"Project root: {project_root}")
    print(f"Source script: {source_script}")
    print(f"Episode: {args.episode_id}")
    print(f"Sections found: {len(sections)}")
    print(f"Will initialize archive: {not archive_dir.exists()}")
    print(f"Will write: {script_yaml}")
    print(f"Will write: {breakdown_yaml}")

    if args.dry_run:
        return

    ensure_archive(project_root, source_script, args.episode_id)
    episode_dir.mkdir(parents=True, exist_ok=True)
    if archive_has_imported_content(script_yaml, breakdown_yaml) and not args.force:
        raise SystemExit(
            f"{args.episode_id} already has imported content. Re-run with --force to overwrite."
        )

    dump_yaml(script_yaml, script_normalized_data(source_label, sections))
    dump_yaml(breakdown_yaml, breakdown_data(args.episode_id, sections))
    render_archive(project_root)
    print("Initialization completed.")


if __name__ == "__main__":
    main()
