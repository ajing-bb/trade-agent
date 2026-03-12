#!/usr/bin/env python3
"""Repo-local Xiaohongshu comment page fetcher with top_comment_id support.

This script exists because upstream `xhs comments` does not expose the
`top_comment_id` parameter already supported by the underlying xiaohongshu-cli
client. It reuses xiaohongshu-cli only for auth, token caching, signing, and
transport, without modifying the installed package.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any
from urllib.parse import quote


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
    from xhs_cli.cookies import cache_xsec_token, get_cookies
    from xhs_cli.exceptions import (
        IpBlockedError,
        NeedVerifyError,
        NoCookieError,
        SessionExpiredError,
        SignatureError,
        UnsupportedOperationError,
        XhsApiError,
    )
    from xhs_cli.formatter import parse_note_url
    from playwright.sync_api import sync_playwright
except Exception as exc:  # pragma: no cover - bootstrap failure path
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


def emit(payload: dict[str, Any]) -> None:
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def build_note_url(id_or_url: str, note_id: str, xsec_token: str) -> str:
    if "xiaohongshu.com" in id_or_url:
        return id_or_url
    if xsec_token:
        return (
            f"https://www.xiaohongshu.com/explore/{note_id}"
            f"?xsec_token={quote(xsec_token, safe='')}&xsec_source=pc_user"
        )
    return f"https://www.xiaohongshu.com/explore/{note_id}"


def detect_browser_executable(preferred: str) -> str:
    if preferred:
        path = Path(preferred).expanduser()
        if path.exists():
            return str(path)
        raise XhsApiError(f"Browser executable not found: {preferred}")

    candidates = [
        Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
        Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)

    raise XhsApiError(
        "No supported browser executable found. Set --browser-executable explicitly."
    )


def get_client(cookie_source: str, *, force_refresh: bool = False) -> tuple[str, XhsClient]:
    browser, cookies = get_cookies(cookie_source, force_refresh=force_refresh)
    return browser, XhsClient(cookies)


def run_client_action(cookie_source: str, action) -> tuple[str, Any]:
    browser, client = get_client(cookie_source)
    try:
        with client:
            return browser, action(client)
    except SessionExpiredError:
        browser, client = get_client(cookie_source, force_refresh=True)
        with client:
            return browser, action(client)


def fetch_all_comment_pages(
    client: XhsClient,
    *,
    note_id: str,
    xsec_token: str,
    top_comment_id: str,
    cursor: str,
    max_pages: int,
) -> dict[str, Any]:
    all_comments: list[dict[str, Any]] = []
    pages_fetched = 0
    current_cursor = cursor
    final_cursor = cursor

    while pages_fetched < max_pages:
        page = client.get_comments(
            note_id,
            cursor=current_cursor,
            xsec_token=xsec_token,
            top_comment_id=top_comment_id,
        )
        if not isinstance(page, dict):
            break

        comments = page.get("comments", [])
        all_comments.extend(comments)
        pages_fetched += 1

        has_more = bool(page.get("has_more"))
        next_cursor = str(page.get("cursor") or "")
        final_cursor = next_cursor
        if not has_more or not next_cursor or next_cursor == current_cursor:
            break
        current_cursor = next_cursor

    return {
        "comments": all_comments,
        "has_more": False,
        "cursor": final_cursor,
        "pages_fetched": pages_fetched,
        "total_fetched": len(all_comments),
    }


def extract_root_comment(data: dict[str, Any], root_comment_id: str) -> dict[str, Any] | None:
    for comment in data.get("comments", []):
        if str(comment.get("id") or "") == root_comment_id:
            return comment
    return None


def extract_dom_comment(locator) -> dict[str, Any]:
    return locator.evaluate(
        """(el) => {
            const clean = (value) => (value || "").replace(/\\s+/g, " ").trim();
            const text = (selector, root = el) => clean(root.querySelector(selector)?.innerText);
            const contentNode = el.querySelector(".content");
            const nicknameNodes = [...(contentNode?.querySelectorAll(".nickname") || [])]
                .map((node) => clean(node.innerText))
                .filter(Boolean);
            const dateParts = [...(el.querySelector(".date")?.querySelectorAll("span") || [])]
                .map((node) => clean(node.innerText))
                .filter(Boolean);

            return {
                id: clean(el.id).replace(/^comment-/, ""),
                author: text(".author .name"),
                author_tag: text(".author .tag"),
                is_author: Boolean(text(".author .tag")),
                content: text(".content .note-text"),
                raw_content: clean(contentNode?.innerText),
                reply_to: el.classList.contains("comment-item-sub") && nicknameNodes.length ? nicknameNodes[0] : "",
                date: dateParts[0] || "",
                location: dateParts[1] || "",
                like_count: text(".like .count"),
                reply_count: text(".reply .count"),
                classes: [...el.classList],
            };
        }"""
    )


def fetch_thread_via_browser(
    *,
    note_url: str,
    cookies: dict[str, str],
    top_comment_id: str,
    browser_executable: str,
    headless: bool,
    max_expand_clicks: int,
    expand_wait_ms: int,
) -> dict[str, Any]:
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            executable_path=browser_executable,
            headless=headless,
        )
        try:
            context = browser.new_context(viewport={"width": 1440, "height": 2200})
            context.add_cookies([
                {
                    "name": name,
                    "value": value,
                    "domain": ".xiaohongshu.com",
                    "path": "/",
                    "httpOnly": False,
                    "secure": True,
                    "sameSite": "None",
                }
                for name, value in cookies.items()
                if name != "saved_at"
            ])
            page = context.new_page()
            page.goto(note_url, wait_until="networkidle", timeout=60000)

            root_locator = page.locator(f"#comment-{top_comment_id}").first
            root_locator.wait_for(timeout=60000)
            root_locator.scroll_into_view_if_needed()

            parent = page.locator(f"div.parent-comment:has(#comment-{top_comment_id})").first
            expand_clicks: list[str] = []
            for _ in range(max_expand_clicks):
                expand = parent.locator(r"text=/展开(\s*\d+\s*条回复|更多回复)/").first
                if expand.count() == 0:
                    break
                expand_clicks.append(expand.inner_text())
                expand.click(timeout=5000)
                page.wait_for_timeout(expand_wait_ms)

            root_comment = extract_dom_comment(root_locator)
            reply_nodes = parent.locator(".comment-item-sub")
            replies = [
                extract_dom_comment(reply_nodes.nth(index))
                for index in range(reply_nodes.count())
            ]

            return {
                "note_url": note_url,
                "browser_executable": browser_executable,
                "headless": headless,
                "expand_clicks": expand_clicks,
                "root_comment": root_comment,
                "reply_count": len(replies),
                "replies": replies,
            }
        finally:
            browser.close()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch Xiaohongshu comment pages with optional top_comment_id anchoring."
    )
    parser.add_argument(
        "id_or_url",
        help="Note URL or note ID. If a URL is provided, xsec_token will be extracted and cached.",
    )
    parser.add_argument(
        "--top-comment-id",
        default="",
        help="Anchor the request on a specific top-level comment ID.",
    )
    parser.add_argument(
        "--cursor",
        default="",
        help="Comment page cursor.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Auto-paginate comment/page results.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=20,
        help="Maximum pages to fetch when --all is set. Default: 20.",
    )
    parser.add_argument(
        "--root-only",
        action="store_true",
        help="When --top-comment-id is set, return only the matching root comment if found.",
    )
    parser.add_argument(
        "--cookie-source",
        default="auto",
        help="Browser cookie source. Default: auto.",
    )
    parser.add_argument(
        "--browser-thread",
        action="store_true",
        help="Use a real browser context to fully expand one anchored comment thread.",
    )
    parser.add_argument(
        "--browser-executable",
        default="",
        help="Path to Chrome/Edge executable. Default: auto-detect.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window instead of running headless.",
    )
    parser.add_argument(
        "--max-expand-clicks",
        type=int,
        default=10,
        help="Maximum number of expand-more clicks in browser-thread mode. Default: 10.",
    )
    parser.add_argument(
        "--expand-wait-ms",
        type=int,
        default=1200,
        help="Wait time after each expand click in browser-thread mode. Default: 1200.",
    )
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if args.max_pages <= 0 or args.max_expand_clicks <= 0 or args.expand_wait_ms <= 0:
        emit({
            "ok": False,
            "error": {
                "code": "invalid_argument",
                "message": "--max-pages, --max-expand-clicks, and --expand-wait-ms must be positive integers.",
            },
        })
        return 1

    note_id, url_token = parse_note_url(args.id_or_url)
    xsec_token = url_token
    if xsec_token:
        cache_xsec_token(note_id, xsec_token)
    note_url = build_note_url(args.id_or_url, note_id, xsec_token)

    try:
        if args.browser_thread:
            if not args.top_comment_id:
                emit({
                    "ok": False,
                    "error": {
                        "code": "invalid_argument",
                        "message": "--browser-thread requires --top-comment-id.",
                    },
                })
                return 1

            cookie_browser, cookies = get_cookies(args.cookie_source)
            browser_data = fetch_thread_via_browser(
                note_url=note_url,
                cookies=cookies,
                top_comment_id=args.top_comment_id,
                browser_executable=detect_browser_executable(args.browser_executable),
                headless=not args.headed,
                max_expand_clicks=args.max_expand_clicks,
                expand_wait_ms=args.expand_wait_ms,
            )
            emit({
                "ok": True,
                "meta": {
                    "mode": "browser_thread",
                    "note_id": note_id,
                    "note_url": note_url,
                    "cookie_source": args.cookie_source,
                    "browser": cookie_browser,
                    "top_comment_id": args.top_comment_id,
                    "max_expand_clicks": args.max_expand_clicks,
                    "expand_wait_ms": args.expand_wait_ms,
                },
                "data": browser_data,
            })
            return 0

        def _action(client: XhsClient) -> dict[str, Any]:
            if args.all:
                return fetch_all_comment_pages(
                    client,
                    note_id=note_id,
                    xsec_token=xsec_token,
                    top_comment_id=args.top_comment_id,
                    cursor=args.cursor,
                    max_pages=args.max_pages,
                )
            return client.get_comments(
                note_id,
                cursor=args.cursor,
                xsec_token=xsec_token,
                top_comment_id=args.top_comment_id,
            )

        browser, data = run_client_action(args.cookie_source, _action)

        payload: dict[str, Any] = {
            "ok": True,
            "meta": {
                "note_id": note_id,
                "cookie_source": args.cookie_source,
                "browser": browser,
                "top_comment_id": args.top_comment_id,
                "cursor": args.cursor,
                "all": args.all,
                "max_pages": args.max_pages if args.all else None,
            },
            "data": data,
        }

        if args.root_only and args.top_comment_id:
            root_comment = extract_root_comment(data, args.top_comment_id)
            payload["data"] = {
                "root_comment": root_comment,
                "found": root_comment is not None,
            }

        emit(payload)
        return 0
    except Exception as exc:
        emit({
            "ok": False,
            "error": {
                "code": error_code_for_exception(exc),
                "message": str(exc),
            },
        })
        return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
