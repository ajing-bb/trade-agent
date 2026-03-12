#!/usr/bin/env python3
"""Dump a Xiaohongshu user's notes, comments, and relevant expanded threads."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote


REPO_ROOT = Path(__file__).resolve().parent.parent
THREAD_SCRIPT = REPO_ROOT / "scripts" / "xhs-comment-page.py"

NOTE_KEYWORDS = [
    "ai视频",
    "ai动画",
    "动画",
    "视频",
    "镜头",
    "机位",
    "动作",
    "一致性",
    "融图",
    "多角色",
    "场景",
    "分镜",
    "图生",
    "3d",
    "kontext",
    "banana",
    "nanobanana",
    "veo",
    "flow",
]

THREAD_KEYWORDS = [
    "怎么",
    "如何",
    "为啥",
    "为什么",
    "可以",
    "不行",
    "用什么",
    "workflow",
    "工作流",
    "流程",
    "模型",
    "提示词",
    "一致性",
    "分镜",
    "动作",
    "姿势",
    "机位",
    "镜头",
    "场景",
    "口型",
    "清晰",
    "黑边",
    "糊",
    "裁剪",
    "融图",
    "多主体",
    "多人",
    "角色",
    "骨骼",
    "迁移",
    "线稿",
    "comfy",
    "kontext",
    "banana",
    "veo",
    "flow",
    "scail",
    "可灵",
    "gemini",
]


def _tool_python_candidates() -> list[Path]:
    home = Path.home()
    return [
        home / ".local/share/uv/tools/xiaohongshu-cli/bin/python3",
        home / ".local/share/uv/tools/xiaohongshu-cli/bin/python",
        home / ".local/pipx/venvs/xiaohongshu-cli/bin/python",
        home / ".local/share/pipx/venvs/xiaohongshu-cli/bin/python",
    ]


def _bootstrap_xhs_cli_imports() -> list[Path]:
    home = Path.home()
    candidates = [
        home / ".local/share/uv/tools/xiaohongshu-cli/lib",
        home / ".local/pipx/venvs/xiaohongshu-cli/lib",
        home / ".local/share/pipx/venvs/xiaohongshu-cli/lib",
    ]

    for lib_root in candidates:
        if not lib_root.exists():
            continue
        for site_packages in lib_root.glob("python*/site-packages"):
            sys.path.insert(0, str(site_packages))
    return _tool_python_candidates()


_PYTHON_CANDIDATES = _bootstrap_xhs_cli_imports()

try:
    from xhs_cli.client import XhsClient
    from xhs_cli.cookies import get_cookies
    from xhs_cli.exceptions import (
        IpBlockedError,
        NeedVerifyError,
        NoCookieError,
        SessionExpiredError,
        SignatureError,
        UnsupportedOperationError,
        XhsApiError,
    )
except Exception as exc:  # pragma: no cover
    current = Path(sys.executable).resolve()
    fallback = next((candidate for candidate in _PYTHON_CANDIDATES if candidate.exists()), None)
    if fallback and fallback.resolve() != current:
        completed = subprocess.run([str(fallback), __file__, *sys.argv[1:]], check=False)
        raise SystemExit(completed.returncode)

    raise SystemExit(
        "Unable to import xiaohongshu-cli dependencies. "
        "Install it first with `uv tool install xiaohongshu-cli`.\n"
        f"Import error: {exc}"
    )


def error_code_for_exception(exc: Exception) -> str:
    if isinstance(exc, (NoCookieError, SessionExpiredError)):
        return "not_authenticated"
    if isinstance(exc, NeedVerifyError):
        return "verification_required"
    if isinstance(exc, IpBlockedError):
        return "ip_blocked"
    if isinstance(exc, SignatureError):
        return "signature_error"
    if isinstance(exc, UnsupportedOperationError):
        return "unsupported_operation"
    if isinstance(exc, XhsApiError):
        return "api_error"
    return "unknown_error"


def run_client_action(cookie_source: str, action) -> tuple[str, Any]:
    browser, cookies = get_cookies(cookie_source)
    client = XhsClient(cookies)
    try:
        with client:
            return browser, action(client)
    except SessionExpiredError:
        browser, cookies = get_cookies(cookie_source, force_refresh=True)
        client = XhsClient(cookies)
        with client:
            return browser, action(client)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("user_id", help="Target Xiaohongshu user id.")
    parser.add_argument(
        "--out-dir",
        default=str(REPO_ROOT / ".tmp" / "xhs-profile-dump"),
        help="Directory for generated JSON files.",
    )
    parser.add_argument(
        "--cookie-source",
        default="auto",
        help="Browser cookie source. Default: auto.",
    )
    parser.add_argument(
        "--max-comment-pages",
        type=int,
        default=100,
        help="Maximum pages when fetching top-level comments per note.",
    )
    parser.add_argument(
        "--max-expand-threads",
        type=int,
        default=40,
        help="Maximum relevant threads to expand via browser.",
    )
    return parser.parse_args(argv)


def to_url(note_id: str, xsec_token: str) -> str:
    return (
        f"https://www.xiaohongshu.com/explore/{note_id}"
        f"?xsec_token={quote(xsec_token, safe='')}&xsec_source=pc_user"
    )


def normalize(text: str) -> str:
    return " ".join((text or "").lower().split())


def note_is_relevant(note: dict[str, Any]) -> bool:
    text = normalize(" ".join([
        str(note.get("title") or ""),
        str(note.get("desc") or ""),
        " ".join(str(tag.get("name") or "") for tag in note.get("tags", [])),
    ]))
    return any(keyword in text for keyword in NOTE_KEYWORDS)


def thread_is_relevant(comment: dict[str, Any]) -> bool:
    blob = [str(comment.get("content") or "")]
    for reply in comment.get("sub_comments", []):
        blob.append(str(reply.get("content") or ""))
    text = normalize(" ".join(blob))
    if any(keyword in text for keyword in THREAD_KEYWORDS):
        return True
    return "?" in text or "？" in text


def fetch_all_notes(client: XhsClient, user_id: str) -> list[dict[str, Any]]:
    cursor = ""
    notes: list[dict[str, Any]] = []
    while True:
        data = client.get_user_notes(user_id, cursor=cursor)
        notes.extend(data.get("notes", []))
        if not data.get("has_more"):
            break
        next_cursor = str(data.get("cursor") or "")
        if not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
    return notes


def sanitize_note_card(note_card: dict[str, Any], *, url: str, relevant: bool) -> dict[str, Any]:
    return {
        "note_id": note_card.get("note_id"),
        "url": url,
        "title": note_card.get("title"),
        "desc": note_card.get("desc"),
        "type": note_card.get("type"),
        "time": note_card.get("time"),
        "last_update_time": note_card.get("last_update_time"),
        "interact_info": note_card.get("interact_info", {}),
        "user": note_card.get("user", {}),
        "tags": note_card.get("tag_list", []),
        "relevant_for_ai_video": relevant,
    }


def sanitize_comment(comment: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": comment.get("id"),
        "content": comment.get("content"),
        "create_time": comment.get("create_time"),
        "ip_location": comment.get("ip_location"),
        "like_count": comment.get("like_count"),
        "sub_comment_count": comment.get("sub_comment_count"),
        "sub_comment_has_more": comment.get("sub_comment_has_more"),
        "sub_comment_cursor": comment.get("sub_comment_cursor"),
        "user_info": {
            "user_id": comment.get("user_info", {}).get("user_id"),
            "nickname": comment.get("user_info", {}).get("nickname"),
        },
        "sub_comments": [
            {
                "id": reply.get("id"),
                "content": reply.get("content"),
                "create_time": reply.get("create_time"),
                "ip_location": reply.get("ip_location"),
                "like_count": reply.get("like_count"),
                "user_info": {
                    "user_id": reply.get("user_info", {}).get("user_id"),
                    "nickname": reply.get("user_info", {}).get("nickname"),
                },
                "show_tags": reply.get("show_tags", []),
                "target_comment": {
                    "id": reply.get("target_comment", {}).get("id"),
                    "user_info": {
                        "user_id": reply.get("target_comment", {}).get("user_info", {}).get("user_id"),
                        "nickname": reply.get("target_comment", {}).get("user_info", {}).get("nickname"),
                    },
                },
            }
            for reply in comment.get("sub_comments", [])
        ],
        "show_tags": comment.get("show_tags", []),
    }


def expand_thread(note_url: str, comment_id: str) -> dict[str, Any] | None:
    if not THREAD_SCRIPT.exists():
        return None
    cmd = [
        sys.executable,
        str(THREAD_SCRIPT),
        note_url,
        "--top-comment-id",
        comment_id,
        "--browser-thread",
        "--max-expand-clicks",
        "20",
        "--expand-wait-ms",
        "1000",
    ]
    completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if completed.returncode != 0:
        return {
            "ok": False,
            "stderr": completed.stderr.strip(),
            "stdout": completed.stdout.strip(),
        }
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return {
            "ok": False,
            "stdout": completed.stdout.strip(),
            "stderr": completed.stderr.strip(),
        }


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        browser, payload = run_client_action(
            args.cookie_source,
            lambda client: {
                "profile": client.get_user_info(args.user_id),
                "notes": fetch_all_notes(client, args.user_id),
            },
        )

        result: dict[str, Any] = {
            "fetched_at": datetime.now(timezone.utc).isoformat(),
            "cookie_source": args.cookie_source,
            "browser": browser,
            "user_id": args.user_id,
            "profile": payload["profile"],
            "notes": [],
        }

        expanded_threads = 0

        browser, _ = run_client_action(args.cookie_source, lambda client: True)
        result["browser"] = browser

        def collect_note(client: XhsClient, note_stub: dict[str, Any]) -> dict[str, Any]:
            nonlocal expanded_threads

            note_id = str(note_stub.get("note_id") or "")
            xsec_token = str(note_stub.get("xsec_token") or "")
            note_data = client.get_note_by_id(note_id, xsec_token=xsec_token)
            note_card = (note_data.get("items") or [{}])[0].get("note_card") or {}
            note_url = to_url(note_id, xsec_token) if xsec_token else ""
            relevant = note_is_relevant(note_card)

            comments_data = client.get_all_comments(
                note_id,
                xsec_token=xsec_token,
                max_pages=args.max_comment_pages,
            )
            comments = comments_data.get("comments", [])
            sanitized_comments = [sanitize_comment(comment) for comment in comments]

            expanded: list[dict[str, Any]] = []
            for comment in sanitized_comments:
                if expanded_threads >= args.max_expand_threads:
                    break
                if not comment.get("sub_comment_has_more"):
                    continue
                if not thread_is_relevant(comment):
                    continue
                if not note_url:
                    continue
                expanded_payload = expand_thread(note_url, str(comment["id"]))
                expanded.append({
                    "comment_id": comment["id"],
                    "data": expanded_payload,
                })
                expanded_threads += 1

            return {
                "note": sanitize_note_card(note_card, url=note_url, relevant=relevant),
                "comments_meta": {
                    "top_level_total": len(sanitized_comments),
                    "pages_fetched": comments_data.get("pages_fetched"),
                    "reported_total": note_card.get("interact_info", {}).get("comment_count"),
                },
                "comments": sanitized_comments,
                "expanded_threads": expanded,
            }

        _, notes = run_client_action(
            args.cookie_source,
            lambda client: [collect_note(client, note_stub) for note_stub in payload["notes"]],
        )
        result["notes"] = notes

        summary = {
            "user_id": args.user_id,
            "nickname": payload["profile"].get("basic_info", {}).get("nickname"),
            "note_count": len(notes),
            "relevant_note_count": sum(1 for item in notes if item["note"].get("relevant_for_ai_video")),
            "expanded_thread_count": sum(len(item["expanded_threads"]) for item in notes),
        }

        dataset_path = out_dir / "dataset.json"
        summary_path = out_dir / "summary.json"
        dataset_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        print(json.dumps({
            "ok": True,
            "out_dir": str(out_dir),
            "dataset": str(dataset_path),
            "summary": str(summary_path),
            "summary_data": summary,
        }, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "error": {
                "code": error_code_for_exception(exc),
                "message": str(exc),
            },
        }, ensure_ascii=False, indent=2))
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
