#!/usr/bin/env python3
"""Initialize an AI manhua project archive from a source DOCX."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Any
from xml.etree import ElementTree

import yaml


WORD_NAMESPACE = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


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


def breakdown_data(episode_id: str, sections: list[dict[str, Any]]) -> dict[str, Any]:
    scenes = []
    for index, section in enumerate(sections, start=1):
        scenes.append(
            {
                "id": scene_id(episode_id, index),
                "unit": section["id"],
                "time_location": section.get("time_location", ""),
                "location_id": "",
                "purpose": section.get("summary", ""),
                "characters": [],
                "key_assets": [],
            }
        )
    return {
        "project_type": "AI漫剧",
        "target_style": "",
        "core_theme": "",
        "core_continuity_risks": [],
        "scenes": scenes,
        "shots": [],
    }


def ensure_archive(project_root: Path, source_script: Path, episode_id: str) -> None:
    archive_dir = project_root / "项目档案"
    if archive_dir.exists():
        return
    reset_script = Path(__file__).with_name("reset-project-creation.py")
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
    render_script = Path(__file__).with_name("render-project-archive.py")
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
