#!/usr/bin/env python3
"""Reset an AI manhua project back to a clean pre-production state."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


HARD_RESET_DIRS = ("项目档案", "角色", "场景", "道具", "VFX")

DEFAULT_PRODUCTION_RULES = [
    "先角色后场景再道具和VFX",
    "角色资产优先走 Face Draft -> Full Body Master -> Banana Derived Pack",
    "Midjourney 只做各类资产的第一个 canonical base / master asset，不负责后续派生包",
    "Banana Pro 统一基于定稿做后续派生，例如角色三视图、表情、角度，场景反打与机位变体，道具变体，VFX look-dev 变体",
    "Banana Pro 派生提示词默认显式写 请参考当前资产定稿 或 请参考当前人物全身照",
]

DEFAULT_CANONICAL_RULES = [
    "本目录与 episodes 中已确认的档案文件，构成本项目的 canonical memory",
    "后续续集、资产补画、Seedance prompt、角色返修，默认先读 canonical 档案，再参考聊天记录",
    "如果聊天结论与仓库档案冲突，以仓库中最新确认版本为准",
    "临时探索图、未落盘图片、未写回档案的 prompt 结论，不视为 canonical",
]

@dataclass
class ResetContext:
    project_root: Path
    archive_dir: Path
    title: str
    project_id: str
    archive_version: str
    source_script: Path
    source_script_label: str
    episode_id: str
    mode: str
    rebuild_skeleton: bool


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


def dump_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def best_effort_relative(path: Path, base: Path) -> str:
    try:
        return path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def generate_project_id(title: str) -> str:
    letters = []
    last_was_sep = False
    for char in title:
        if char.isascii() and char.isalnum():
            letters.append(char.upper())
            last_was_sep = False
        elif not last_was_sep:
            letters.append("_")
            last_was_sep = True
    candidate = "".join(letters).strip("_")
    return candidate or "PROJECT"


def existing_series_metadata(project_root: Path) -> dict[str, str]:
    series_bible = project_root / "项目档案" / "series" / "series-bible.yaml"
    if not series_bible.exists():
        return {}
    try:
        data = load_yaml(series_bible)
    except Exception:
        return {}
    metadata: dict[str, str] = {}
    for key in ("project_id", "archive_version", "story_form", "title"):
        value = data.get(key)
        if isinstance(value, str) and value:
            metadata[key] = value
    return metadata


def stable_prefixes_for_episode(episode_id: str) -> dict[str, str]:
    return {
        "character": "CHAR_",
        "location": "LOC_",
        "prop": "PROP_",
        "vfx": "VFX_",
        "shot": f"{episode_id.upper()}-",
    }


def discover_source_script(project_root: Path, override: str | None) -> Path:
    if override:
        path = Path(override)
        if not path.exists():
            raise FileNotFoundError(f"Source script does not exist: {path}")
        return path.resolve()

    script_dir = project_root / "剧本"
    matches = sorted(script_dir.glob("*.docx"))
    if len(matches) == 1:
        return matches[0].resolve()
    if not matches:
        raise FileNotFoundError("No .docx file found under 剧本/. Pass --source-script explicitly.")
    raise ValueError("Multiple .docx files found under 剧本/. Pass --source-script explicitly.")


def build_context(args: argparse.Namespace) -> ResetContext:
    project_root = Path(args.project_root).resolve()
    if not project_root.exists():
        raise FileNotFoundError(f"Project root does not exist: {project_root}")
    if not project_root.is_dir():
        raise NotADirectoryError(f"Project root is not a directory: {project_root}")

    metadata = existing_series_metadata(project_root)
    source_script = discover_source_script(project_root, args.source_script)
    cwd = Path.cwd()
    source_script_label = best_effort_relative(source_script, cwd)
    return ResetContext(
        project_root=project_root,
        archive_dir=project_root / "项目档案",
        title=metadata.get("title") or project_root.name,
        project_id=metadata.get("project_id") or generate_project_id(project_root.name),
        archive_version=metadata.get("archive_version") or "v1",
        source_script=source_script,
        source_script_label=source_script_label,
        episode_id=args.episode_id,
        mode=args.mode,
        rebuild_skeleton=args.rebuild_skeleton,
    )


def archive_readme(ctx: ResetContext) -> str:
    archive_label = best_effort_relative(ctx.archive_dir, Path.cwd())
    return f"""# {ctx.title}｜项目档案

这个目录是本项目的长期记忆区，不依赖聊天上下文。

## Canonical 说明

- `canonical` 指仓库里唯一长期有效、后续默认以其为准的标准版本。
- 聊天里的临时讨论、试验 prompt、探索图结论，不自动算 canonical。
- 写入 `{archive_label}/` 的确认版本，才作为续集、补镜头、重做资产时的默认依据。
- 当前以下结构化档案以 `YAML single source of truth` 为准，同名 `.md` 为脚本生成的只读展示：
  - `series/series-bible`
  - `series/style-bible`
  - `series/character-bible`
  - `series/character-asset-prompt-pack`
  - `series/scene-bible`
  - `series/scene-asset-prompt-pack`
  - `series/prop-vfx-bible`
  - `series/prop-vfx-asset-prompt-pack`
  - `episodes/{ctx.episode_id}/breakdown`
  - `episodes/{ctx.episode_id}/continuity-plan`
  - `episodes/{ctx.episode_id}/script-normalized`
  - `episodes/{ctx.episode_id}/asset-manifest`
  - `episodes/{ctx.episode_id}/director-queue`
- 对以上结构化文件，不要手改生成出来的 `.md`；应先改 `.yaml`，再运行：
  - `python3 scripts/render-project-archive.py {archive_label}`

## 结构

- `series/`
  - 跨批次复用的总设定、角色总表、场景总表、道具与 VFX 总表
- `episodes/{ctx.episode_id}/`
  - 当前 fresh start 的标准化文本、拆解、连续性方案、导演队列、资产清单
- `progress-update-sop.md`
  - 每次工作结束前如何判断是否需要更新进度，以及更新顺序

## 当前约定

- 原始剧本来源：`{ctx.source_script_label}`
- 当前状态：`fresh reset`
- `Midjourney` 只负责底图
- `Banana Pro` 统一负责改图、修正规则、抽单格和回拼
- 对角色资产，优先增加 `Face Draft` 步骤：先用 `Midjourney` 生成脸部或半身定稿，再用它作为最高优面部参考去生成全身定稿
- 所有后续派生资产都基于这个定稿在 `Banana Pro` 中完成，例如：三视图、表情、角度、反打、局部修订、场景反打、道具变体、VFX look-dev 变体
- 后续 `Banana Pro` 提示词默认都要显式写入“请参考当前资产定稿 / 当前人物全身照”，避免模型漂移

## Fresh Start 工作流

1. 先导入 `script-normalized.yaml`
2. 再补 `breakdown.yaml`
3. 再建立 `series/` 下的 style / character / scene / prop-vfx
4. 新资产落盘后，先更新 `asset-manifest`，再更新对应 bible
"""


def progress_update_sop(ctx: ResetContext) -> str:
    archive_label = best_effort_relative(ctx.archive_dir, Path.cwd())
    return f"""# Progress Update SOP

用于保证本项目支持：

- 随时退出 Codex
- 下次继续时快速恢复进度
- 不依赖聊天上下文

## 一句话原则

只要发生了 `定稿 / 落盘 / 状态变化 / 规则变化 / 阻塞变化` 这五类事情中的任意一种，就更新进度。

## Single Source of Truth

以下结构化档案以 `.yaml` 作为唯一事实源：

- `series/series-bible.yaml`
- `series/style-bible.yaml`
- `series/character-bible.yaml`
- `series/character-asset-prompt-pack.yaml`
- `series/scene-bible.yaml`
- `series/scene-asset-prompt-pack.yaml`
- `series/prop-vfx-bible.yaml`
- `series/prop-vfx-asset-prompt-pack.yaml`
- `episodes/{ctx.episode_id}/breakdown.yaml`
- `episodes/{ctx.episode_id}/continuity-plan.yaml`
- `episodes/{ctx.episode_id}/script-normalized.yaml`
- `episodes/{ctx.episode_id}/asset-manifest.yaml`
- `episodes/{ctx.episode_id}/director-queue.yaml`

对应 `.md` 为脚本生成的只读展示，不应手工编辑。

渲染命令：

```bash
python3 scripts/render-project-archive.py {archive_label}
```

## Fresh Start 默认顺序

1. 从 `script-normalized.yaml` 开始重新导入剧本
2. 补 `breakdown.yaml`
3. 补 `series/` 中的 style / character / scene / prop-vfx
4. 资产正式落盘后，再更新 `asset-manifest.yaml`
5. 有镜头依赖变化时，再更新 `director-queue.yaml` 和 `continuity-plan.yaml`

## 不算进度更新的内容

- 聊天里讨论过但没落档的结论
- 外部平台里挑中的图但没有保存到仓库
- 临时试过的 prompt
- 口头确认但没有改状态
"""


def series_bible_data(ctx: ResetContext) -> dict[str, Any]:
    return {
        "project_id": ctx.project_id,
        "title": ctx.title,
        "source_script": ctx.source_script_label,
        "archive_version": ctx.archive_version,
        "ingested_units": [],
        "current_ingested_range": "",
        "story_form": "AI漫剧",
        "story_hook": "",
        "genre": [],
        "world_rules": [],
        "production_rules": DEFAULT_PRODUCTION_RULES,
        "canonical_rules": DEFAULT_CANONICAL_RULES,
        "current_import_notes": [],
        "stable_id_prefixes": stable_prefixes_for_episode(ctx.episode_id),
    }


def style_bible_data() -> dict[str, Any]:
    return {
        "style_name": "",
        "core_format": "",
        "overall_density": "",
        "realism_level": "",
        "reference_warning": [],
        "line_and_render": {},
        "color_and_light": {},
        "world_design": {},
        "camera_rules": {},
        "failure_boundaries": [],
    }


def character_bible_data() -> dict[str, Any]:
    return {
        "notes": [
            "项目已 fresh reset，角色 canonical 资产待重新建立。",
            "新角色标准角色包默认应有：脸部定稿 / 全身 / 三视图 / 表情 / 角度。",
        ],
        "characters": [],
    }


def empty_character_prompt_pack() -> dict[str, Any]:
    return {
        "prompt_pack_id": "CHARACTER_ASSET_PROMPT_PACK_V1",
        "project_id": "",
        "scope": [],
        "rules": {
            "midjourney_role": "base_generation_only",
            "banana_role": "derive_turnaround_expression_angle_and_repair",
            "canonical_note": "fresh_reset",
            "character_pipeline": "face_draft_then_full_body_then_banana_derived_pack",
        },
        "characters": [],
    }


def scene_bible_data() -> dict[str, Any]:
    return {
        "rules": ["项目已 fresh reset，场景 canonical 资产待重新建立。"],
        "locations": [],
    }


def empty_scene_prompt_pack() -> dict[str, Any]:
    return {
        "prompt_pack_id": "SCENE_ASSET_PROMPT_PACK_V1",
        "project_id": "",
        "rules": {
            "midjourney_role": "scene_master_only",
            "banana_role": "derive_reverse_angle_variant_and_repair",
            "scene_pipeline": "scene_master_then_banana_derived_views",
        },
        "locations": [],
    }


def prop_vfx_bible_data() -> dict[str, Any]:
    return {
        "rules": ["项目已 fresh reset，道具与 VFX canonical 资产待重新建立。"],
        "props": [],
        "vfx": [],
    }


def empty_prop_vfx_prompt_pack() -> dict[str, Any]:
    return {
        "prompt_pack_id": "PROP_VFX_ASSET_PROMPT_PACK_V1",
        "project_id": "",
        "rules": {
            "midjourney_role": "asset_master_only",
            "banana_role": "derive_variant_and_repair",
        },
        "props": [],
        "vfx": [],
    }


def script_normalized_data(ctx: ResetContext) -> dict[str, Any]:
    return {
        "source_file": ctx.source_script_label,
        "covered_units": [],
        "source_notes": [f"原文件：{ctx.source_script_label}", "项目已 fresh reset，请重新导入剧本内容。"],
        "sections": [],
    }


def breakdown_data() -> dict[str, Any]:
    return {
        "project_type": "AI漫剧",
        "target_style": "",
        "core_theme": "",
        "core_continuity_risks": [],
        "scenes": [],
        "shots": [],
    }


def continuity_plan_data() -> dict[str, Any]:
    return {
        "high_priority_locks": [],
        "canonical_character_assets": [],
        "pending_character_assets": [],
        "shot_build_policy": [],
        "risks": [],
    }


def director_queue_data() -> dict[str, Any]:
    return {
        "queue_rules": {
            "blocked": "关键资产还未正式落盘，镜头不能进入生成阶段",
            "ready": "关键资产已齐，可进入静帧或首尾帧生成",
            "in_progress": "镜头正在制作",
            "done": "镜头已完成并通过当前轮验收",
        },
        "status_notes": ["项目已 fresh reset，当前没有镜头排产。"],
        "queue": [],
    }


def asset_manifest_data(ctx: ResetContext) -> dict[str, Any]:
    return {
        "notes": [
            "项目已 fresh reset，当前只保留原始剧本文件。",
            "后续新图落盘后，应先更新本文件，再同步对应 bible。",
        ],
        "assets": [
            {
                "id": "SRC_SCRIPT_DOCX",
                "type": "script",
                "status": "committed",
                "path": ctx.source_script_label,
            }
        ],
    }


def reset_targets(ctx: ResetContext) -> tuple[list[Path], list[Path]]:
    remove_paths: list[Path] = [ctx.archive_dir]
    if ctx.mode == "hard":
        for dirname in HARD_RESET_DIRS:
            if dirname == "项目档案":
                continue
            target = ctx.project_root / dirname
            if target.exists():
                remove_paths.append(target)
        root_ds_store = ctx.project_root / ".DS_Store"
        if root_ds_store.exists():
            remove_paths.append(root_ds_store)

    create_paths: list[Path] = []
    if ctx.rebuild_skeleton:
        create_paths = [
            ctx.archive_dir,
            ctx.archive_dir / "series",
            ctx.archive_dir / "episodes",
            ctx.archive_dir / "episodes" / ctx.episode_id,
        ]
    return remove_paths, create_paths


def print_plan(ctx: ResetContext, remove_paths: list[Path], create_paths: list[Path]) -> None:
    print(f"Mode: {ctx.mode}")
    print(f"Rebuild skeleton: {ctx.rebuild_skeleton}")
    print(f"Project root: {ctx.project_root}")
    print(f"Source script: {ctx.source_script}")
    print("Will remove:")
    for path in remove_paths:
        print(f"  - {path}")
    if create_paths:
        print("Will create:")
        for path in create_paths:
            print(f"  - {path}")


def confirm_reset() -> None:
    prompt = "Type RESET to continue: "
    if input(prompt).strip() != "RESET":
        raise SystemExit("Reset cancelled.")


def remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def write_archive_files(ctx: ResetContext) -> None:
    series_dir = ctx.archive_dir / "series"
    episode_dir = ctx.archive_dir / "episodes" / ctx.episode_id

    dump_text(ctx.archive_dir / "README.md", archive_readme(ctx))
    dump_text(ctx.archive_dir / "progress-update-sop.md", progress_update_sop(ctx))

    character_prompt = empty_character_prompt_pack()
    character_prompt["project_id"] = ctx.project_id
    scene_prompt = empty_scene_prompt_pack()
    scene_prompt["project_id"] = ctx.project_id
    prop_prompt = empty_prop_vfx_prompt_pack()
    prop_prompt["project_id"] = ctx.project_id

    dump_yaml(series_dir / "series-bible.yaml", series_bible_data(ctx))
    dump_yaml(series_dir / "style-bible.yaml", style_bible_data())
    dump_yaml(series_dir / "character-bible.yaml", character_bible_data())
    dump_yaml(series_dir / "character-asset-prompt-pack.yaml", character_prompt)
    dump_yaml(series_dir / "scene-bible.yaml", scene_bible_data())
    dump_yaml(series_dir / "scene-asset-prompt-pack.yaml", scene_prompt)
    dump_yaml(series_dir / "prop-vfx-bible.yaml", prop_vfx_bible_data())
    dump_yaml(series_dir / "prop-vfx-asset-prompt-pack.yaml", prop_prompt)

    dump_yaml(episode_dir / "script-normalized.yaml", script_normalized_data(ctx))
    dump_yaml(episode_dir / "breakdown.yaml", breakdown_data())
    dump_yaml(episode_dir / "continuity-plan.yaml", continuity_plan_data())
    dump_yaml(episode_dir / "director-queue.yaml", director_queue_data())
    dump_yaml(episode_dir / "asset-manifest.yaml", asset_manifest_data(ctx))


def render_archive(ctx: ResetContext) -> None:
    render_script = Path(__file__).with_name("render-project-archive.py")
    subprocess.run(
        [sys.executable, str(render_script), str(ctx.archive_dir)],
        check=True,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Reset an AI manhua project so only the source script remains by default."
    )
    parser.add_argument("project_root", help="Path to assets/<项目名>")
    parser.add_argument(
        "--mode",
        choices=("hard", "archive-only"),
        default="hard",
        help="Reset scope. 'hard' also deletes derived asset directories, while 'archive-only' only removes 项目档案.",
    )
    parser.add_argument(
        "--source-script",
        help="Optional path to the source .docx. Required if 剧本/ contains zero or multiple .docx files.",
    )
    parser.add_argument(
        "--episode-id",
        default="ep001",
        help="Episode folder to recreate when --rebuild-skeleton is enabled.",
    )
    parser.add_argument(
        "--rebuild-skeleton",
        action="store_true",
        help="Recreate a fresh 项目档案 skeleton after deletion. Default behavior leaves only the script files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without modifying files.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Skip interactive confirmation.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ctx = build_context(args)
    remove_paths, create_paths = reset_targets(ctx)
    print_plan(ctx, remove_paths, create_paths)

    if args.dry_run:
        return
    if not args.yes:
        confirm_reset()

    for path in remove_paths:
        remove_path(path)
    for path in create_paths:
        path.mkdir(parents=True, exist_ok=True)
    if ctx.rebuild_skeleton:
        write_archive_files(ctx)
        render_archive(ctx)
    print("Reset completed.")


if __name__ == "__main__":
    main()
