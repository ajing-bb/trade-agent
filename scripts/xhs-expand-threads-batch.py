#!/usr/bin/env python3
"""Expand all missing Xiaohongshu sub-comment threads from a dumped dataset."""

from __future__ import annotations

import argparse
import json
import random
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
THREAD_SCRIPT = REPO_ROOT / "scripts" / "xhs-comment-page.py"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--dataset",
        default=str(REPO_ROOT / ".tmp" / "xhs-memmy22-top-comments" / "dataset.json"),
        help="Path to dumped dataset.json.",
    )
    parser.add_argument(
        "--out-dir",
        default=str(REPO_ROOT / ".tmp" / "xhs-memmy22-all-threads"),
        help="Directory for expanded thread JSON files.",
    )
    parser.add_argument(
        "--seed-dir",
        default="",
        help=(
            "Optional directory with existing expanded thread files to reuse. "
            "Matching successful files are filtered into --out-dir before fetching."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="Optional max thread count for testing.",
    )
    parser.add_argument(
        "--sleep-seconds",
        type=float,
        default=10.0,
        help="Base sleep between thread fetches. Default: 10 seconds.",
    )
    parser.add_argument(
        "--sleep-jitter",
        type=float,
        default=5.0,
        help="Additional random sleep jitter between thread fetches. Default: 5 seconds.",
    )
    parser.add_argument(
        "--session-limit",
        type=int,
        default=25,
        help="Max threads to fetch in one run before stopping. Default: 25.",
    )
    parser.add_argument(
        "--burst-size",
        type=int,
        default=0,
        help="After every N freshly fetched threads, take a longer cooldown. Default: 0 (disabled).",
    )
    parser.add_argument(
        "--burst-pause-seconds",
        type=float,
        default=10.0,
        help="Base cooldown after each burst. Default: 10 seconds.",
    )
    parser.add_argument(
        "--burst-pause-jitter",
        type=float,
        default=5.0,
        help="Additional random cooldown after each burst. Default: 5 seconds.",
    )
    parser.add_argument(
        "--note-switch-pause-seconds",
        type=float,
        default=10.0,
        help="Base pause when switching to a different note. Default: 10 seconds.",
    )
    parser.add_argument(
        "--note-switch-pause-jitter",
        type=float,
        default=5.0,
        help="Additional random pause when switching to a different note. Default: 5 seconds.",
    )
    parser.add_argument(
        "--comment-scope",
        choices=("author-only", "author-complete", "all"),
        default="author-only",
        help=(
            "Which threads to expand. "
            "'author-only' keeps only threads where the author spoke and filters replies to author only. "
            "'author-complete' expands every hidden-reply thread and filters results to author only. "
            "'all' preserves every queued thread. Default: author-only."
        ),
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_successful_thread_file(path: Path) -> bool:
    if not path.exists() or path.stat().st_size == 0:
        return False
    try:
        payload = load_json(path)
    except Exception:
        return False
    return bool(payload.get("ok"))


def note_author_id(item: dict[str, Any]) -> str:
    note = item.get("note") or {}
    comments_meta = item.get("comments_meta") or {}
    return str(
        comments_meta.get("author_id")
        or (note.get("user") or {}).get("user_id")
        or ""
    )


def comment_matches_scope(comment: dict[str, Any], *, comment_scope: str, author_id: str) -> bool:
    if comment_scope == "all":
        return True
    if comment_scope == "author-complete":
        return True

    top_is_author = str((comment.get("user_info") or {}).get("user_id") or "") == author_id
    if top_is_author:
        return True

    return any(
        str((reply.get("user_info") or {}).get("user_id") or "") == author_id
        for reply in (comment.get("sub_comments") or [])
    )


def filter_thread_payload(payload: dict[str, Any], *, comment_scope: str) -> dict[str, Any]:
    if comment_scope == "all" or not payload.get("ok"):
        return payload

    data = payload.get("data") or {}
    root_comment = data.get("root_comment") or {}
    author_replies = [
        reply
        for reply in (data.get("replies") or [])
        if reply.get("is_author")
    ]
    has_author_content = bool(root_comment.get("is_author") or author_replies)

    if comment_scope == "author-complete" and not has_author_content:
        return {
            **payload,
            "data": {
                "root_comment": {},
                "replies": [],
                "reply_count": 0,
                "author_top_comment": False,
                "filtered_scope": comment_scope,
                "has_author_content": False,
                "thread_checked": True,
            },
        }

    filtered_data = dict(data)
    filtered_data["root_comment"] = root_comment
    filtered_data["replies"] = author_replies
    filtered_data["reply_count"] = len(author_replies)
    filtered_data["author_top_comment"] = bool(root_comment.get("is_author"))
    filtered_data["filtered_scope"] = comment_scope
    filtered_data["has_author_content"] = has_author_content
    return {
        **payload,
        "data": filtered_data,
    }


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    dataset_path = Path(args.dataset).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    seed_dir = Path(args.seed_dir).expanduser().resolve() if args.seed_dir else None
    out_dir.mkdir(parents=True, exist_ok=True)

    data = load_json(dataset_path)

    queue: list[dict[str, str]] = []
    for item in data["notes"]:
        note = item["note"]
        note_url = note.get("url") or ""
        note_id = note.get("note_id") or ""
        title = note.get("title") or ""
        author_id = note_author_id(item)
        for comment in item["comments"]:
            if not comment.get("sub_comment_has_more"):
                continue
            if not comment_matches_scope(
                comment,
                comment_scope=args.comment_scope,
                author_id=author_id,
            ):
                continue
            queue.append({
                "note_id": note_id,
                "note_url": note_url,
                "title": title,
                "comment_id": comment["id"],
            })

    fresh_queue: list[dict[str, str]] = []
    retry_queue: list[dict[str, str]] = []
    cached_queue: list[dict[str, str]] = []
    for item in queue:
        out_file = out_dir / f"{item['note_id']}__{item['comment_id']}.json"
        if not is_successful_thread_file(out_file) and seed_dir:
            seed_file = seed_dir / out_file.name
            if is_successful_thread_file(seed_file):
                save_json(
                    out_file,
                    filter_thread_payload(load_json(seed_file), comment_scope=args.comment_scope),
                )
        if is_successful_thread_file(out_file):
            cached_queue.append(item)
        elif out_file.exists() and out_file.stat().st_size > 0:
            retry_queue.append(item)
        else:
            fresh_queue.append(item)

    pending_queue = fresh_queue + retry_queue

    if args.limit > 0:
        pending_queue = pending_queue[:args.limit]
    elif args.session_limit > 0:
        pending_queue = pending_queue[:args.session_limit]

    manifest = {
        "dataset": str(dataset_path),
        "out_dir": str(out_dir),
        "total_threads": len(queue),
        "cached_threads": len(cached_queue),
        "fresh_threads": len(fresh_queue),
        "retry_threads": len(retry_queue),
        "pending_threads_this_run": len(pending_queue),
        "comment_scope": args.comment_scope,
        "seed_dir": str(seed_dir) if seed_dir else "",
        "completed": [],
        "failed": [],
    }

    for index, item in enumerate(cached_queue, start=1):
        out_file = out_dir / f"{item['note_id']}__{item['comment_id']}.json"
        manifest["completed"].append({
            "index": index,
            **item,
            "status": "cached",
            "path": str(out_file),
        })

    start_index = len(cached_queue) + 1
    fresh_fetches = 0
    previous_note_id = ""
    for index, item in enumerate(pending_queue, start=start_index):
        out_file = out_dir / f"{item['note_id']}__{item['comment_id']}.json"

        if previous_note_id and item["note_id"] != previous_note_id:
            time.sleep(args.note_switch_pause_seconds + random.uniform(0, args.note_switch_pause_jitter))

        cmd = [
            sys.executable,
            str(THREAD_SCRIPT),
            item["note_url"],
            "--top-comment-id",
            item["comment_id"],
            "--browser-thread",
            "--max-root-scrolls",
            "140",
            "--max-expand-clicks",
            "40",
            "--expand-wait-ms",
            "1200",
        ]
        completed = subprocess.run(cmd, capture_output=True, text=True, check=False)
        payload: dict[str, Any]

        if completed.returncode == 0:
            try:
                payload = json.loads(completed.stdout)
            except json.JSONDecodeError:
                payload = {
                    "ok": False,
                    "error": {
                        "code": "invalid_json",
                        "message": completed.stdout[:1000],
                    },
                }
        else:
            payload = {
                "ok": False,
                "error": {
                    "code": "command_failed",
                    "message": completed.stderr[:1000] or completed.stdout[:1000],
                },
            }

        payload = filter_thread_payload(payload, comment_scope=args.comment_scope)

        save_json(out_file, payload)

        record = {
            "index": index,
            **item,
            "path": str(out_file),
            "ok": bool(payload.get("ok")),
        }
        if payload.get("ok"):
            manifest["completed"].append(record)
        else:
            manifest["failed"].append({
                **record,
                "error": payload.get("error", {}),
            })

        save_json(out_dir / "manifest.json", manifest)
        fresh_fetches += 1
        previous_note_id = item["note_id"]

        time.sleep(args.sleep_seconds + random.uniform(0, args.sleep_jitter))
        if args.burst_size > 0 and fresh_fetches % args.burst_size == 0:
            time.sleep(args.burst_pause_seconds + random.uniform(0, args.burst_pause_jitter))

    save_json(out_dir / "manifest.json", manifest)
    print(json.dumps({
        "ok": True,
        "out_dir": str(out_dir),
        "total_threads": len(queue),
        "cached_threads": len(cached_queue),
        "pending_threads_this_run": len(pending_queue),
        "completed": len(manifest["completed"]),
        "failed": len(manifest["failed"]),
        "manifest": str(out_dir / "manifest.json"),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
