#!/usr/bin/env python3
"""Post a tweet with media using a stock twitter-cli installation for auth only.

This script exists as a repo-local fallback until upstream twitter-cli ships
native media upload support. It reuses twitter-cli's cookie extraction so it can
work with the same logged-in browser session, but the upload + post flow lives
here in the repo.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path


def _tool_python_candidates() -> list[Path]:
    home = Path.home()
    return [
        home / ".local/share/uv/tools/twitter-cli/bin/python",
        home / ".local/pipx/venvs/twitter-cli/bin/python",
        home / ".local/share/pipx/venvs/twitter-cli/bin/python",
    ]


def _bootstrap_twitter_cli_imports() -> list[Path]:
    home = Path.home()
    candidates = [
        home / ".local/share/uv/tools/twitter-cli/lib",
        home / ".local/pipx/venvs/twitter-cli/lib",
        home / ".local/share/pipx/venvs/twitter-cli/lib",
    ]

    for lib_root in candidates:
        if not lib_root.exists():
            continue
        for site_packages in lib_root.glob("python*/site-packages"):
            sys.path.insert(0, str(site_packages))
    return _tool_python_candidates()


_PYTHON_CANDIDATES = _bootstrap_twitter_cli_imports()

try:
    from curl_cffi import CurlMime
    from twitter_cli.auth import get_cookies
    from twitter_cli.client import FEATURES, TwitterClient, _deep_get, _get_cffi_session
    from twitter_cli.exceptions import TwitterAPIError
except Exception as exc:  # pragma: no cover - bootstrap failure path
    current = Path(sys.executable).resolve()
    fallback = next((candidate for candidate in _PYTHON_CANDIDATES if candidate.exists()), None)
    if fallback and fallback.resolve() != current:
        completed = subprocess.run([str(fallback), __file__, *sys.argv[1:]], check=False)
        raise SystemExit(completed.returncode)

    raise SystemExit(
        "Unable to import twitter-cli dependencies. "
        "Install twitter-cli first with `uv tool install twitter-cli`.\n"
        f"Import error: {exc}"
    )


class MediaTwitterClient(TwitterClient):
    """Small extension that adds media upload + media-aware posting."""

    MEDIA_RETRYABLE_STATUS_CODES = {408, 429, 500, 502, 503, 504}
    MEDIA_MAX_ATTEMPTS = 3
    MEDIA_RETRY_BASE_DELAY = 1.0

    @staticmethod
    def _media_category_for_type(media_type: str) -> str:
        if media_type == "image/gif":
            return "tweet_gif"
        if media_type.startswith("video/"):
            return "tweet_video"
        return "tweet_image"

    @staticmethod
    def _format_error_detail(detail: object) -> str:
        if detail is None:
            return "Unknown error"
        if isinstance(detail, str):
            return detail
        try:
            return json.dumps(detail, ensure_ascii=False)
        except TypeError:
            return str(detail)

    def _extract_create_tweet_error(self, data: object) -> str | None:
        if not isinstance(data, dict):
            return None

        errors = data.get("errors")
        if errors:
            return self._format_error_detail(errors)

        create_tweet = _deep_get(data, "data", "create_tweet")
        if isinstance(create_tweet, dict) and create_tweet.get("errors"):
            return self._format_error_detail(create_tweet.get("errors"))

        tweet_results = _deep_get(data, "data", "create_tweet", "tweet_results", "result")
        if isinstance(tweet_results, dict):
            for key in ("reason", "typename", "__typename"):
                value = tweet_results.get(key)
                if value and value != "Tweet":
                    return self._format_error_detail(value)

        return None

    def _upload_media_request(
        self,
        method: str,
        params: dict[str, object],
        multipart_factory: Callable[[], CurlMime] | None = None,
    ) -> dict:
        url = "https://upload.twitter.com/i/media/upload.json"
        headers = self._build_headers(url=url, method=method)
        session = _get_cffi_session()

        last_error: TwitterAPIError | None = None
        for attempt in range(1, self.MEDIA_MAX_ATTEMPTS + 1):
            multipart = multipart_factory() if multipart_factory is not None else None
            request_headers = dict(headers)
            if multipart is not None:
                request_headers.pop("Content-Type", None)

            try:
                response = session.request(
                    method,
                    url,
                    headers=request_headers,
                    params=params,
                    multipart=multipart,
                    timeout=30,
                )
            except Exception as exc:
                if multipart is not None:
                    multipart.close()
                last_error = TwitterAPIError(0, f"Twitter media upload network error: {exc}")
                if attempt >= self.MEDIA_MAX_ATTEMPTS:
                    raise last_error
                time.sleep(self.MEDIA_RETRY_BASE_DELAY * attempt)
                continue

            if multipart is not None:
                multipart.close()

            if response.status_code >= 400:
                last_error = TwitterAPIError(
                    response.status_code,
                    f"Twitter media upload error {response.status_code}: {response.text[:500]}",
                )
                if response.status_code in self.MEDIA_RETRYABLE_STATUS_CODES and attempt < self.MEDIA_MAX_ATTEMPTS:
                    time.sleep(self.MEDIA_RETRY_BASE_DELAY * attempt)
                    continue
                raise last_error

            payload = response.text.strip()
            try:
                parsed = json.loads(payload) if payload else {}
            except json.JSONDecodeError as exc:
                last_error = TwitterAPIError(0, f"Twitter media upload returned invalid JSON: {exc}")
                if attempt >= self.MEDIA_MAX_ATTEMPTS:
                    raise last_error
                time.sleep(self.MEDIA_RETRY_BASE_DELAY * attempt)
                continue

            if isinstance(parsed, dict) and parsed.get("errors"):
                last_error = TwitterAPIError(
                    0,
                    f"Twitter media upload error: {self._format_error_detail(parsed.get('errors'))}",
                )
                raise last_error

            return parsed

        if last_error is not None:
            raise last_error
        raise TwitterAPIError(0, "Twitter media upload failed unexpectedly")

    def upload_media(self, media_path: Path) -> str:
        media_type = mimetypes.guess_type(media_path.name)[0] or "application/octet-stream"
        total_bytes = media_path.stat().st_size
        init_data = self._upload_media_request(
            "POST",
            {
                "command": "INIT",
                "total_bytes": total_bytes,
                "media_type": media_type,
                "media_category": self._media_category_for_type(media_type),
            },
        )
        media_id = str(init_data.get("media_id_string") or init_data.get("media_id") or "")
        if not media_id:
            raise TwitterAPIError(0, f"Failed to initialize media upload for {media_path}")

        with media_path.open("rb") as media_file:
            segment_index = 0
            while True:
                chunk = media_file.read(8 * 1024 * 1024)
                if not chunk:
                    break

                self._upload_media_request(
                    "POST",
                    {
                        "command": "APPEND",
                        "media_id": media_id,
                        "segment_index": segment_index,
                    },
                    multipart_factory=lambda chunk=chunk: self._build_media_part(media_path.name, chunk),
                )
                segment_index += 1

        finalize_data = self._upload_media_request("POST", {"command": "FINALIZE", "media_id": media_id})
        processing_info = finalize_data.get("processing_info")
        while processing_info and processing_info.get("state") in {"pending", "in_progress"}:
            time.sleep(float(processing_info.get("check_after_secs") or 1))
            status_data = self._upload_media_request("GET", {"command": "STATUS", "media_id": media_id})
            processing_info = status_data.get("processing_info")

        if processing_info and processing_info.get("state") == "failed":
            error = processing_info.get("error") or {}
            raise TwitterAPIError(0, f"Twitter media processing failed: {error.get('message') or processing_info}")

        return media_id

    @staticmethod
    def _build_media_part(filename: str, chunk: bytes) -> CurlMime:
        multipart = CurlMime()
        multipart.addpart(
            name="media",
            filename=filename,
            content_type="application/octet-stream",
            data=chunk,
        )
        return multipart

    def create_tweet_with_media(
        self,
        text: str,
        media_ids: list[str],
        reply_to_id: str | None = None,
    ) -> str:
        variables: dict[str, object] = {
            "tweet_text": text,
            "media": {
                "media_entities": [{"media_id": media_id, "tagged_users": []} for media_id in media_ids],
                "possibly_sensitive": False,
            },
            "semantic_annotation_ids": [],
            "dark_request": False,
        }
        if reply_to_id:
            variables["reply"] = {
                "in_reply_to_tweet_id": reply_to_id,
                "exclude_reply_user_ids": [],
            }

        data = self._graphql_post("CreateTweet", variables, FEATURES)
        self._write_delay()
        result = _deep_get(data, "data", "create_tweet", "tweet_results", "result")
        if result:
            return str(result.get("rest_id") or "")
        detail = self._extract_create_tweet_error(data)
        if detail:
            raise TwitterAPIError(0, f"Failed to create tweet: {detail}")
        raise TwitterAPIError(0, "Failed to create tweet: unknown response shape")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Post a tweet with optional media using twitter-cli authentication.",
    )
    parser.add_argument("text", help="Tweet body text.")
    parser.add_argument(
        "--media",
        action="append",
        default=[],
        help="Media file to attach. Repeat up to 4 times.",
    )
    parser.add_argument("--reply-to", help="Reply to an existing tweet ID.", default=None)
    parser.add_argument("--dry-run", action="store_true", help="Validate inputs and print the payload without posting.")
    parser.add_argument("--json", action="store_true", help="Print the result as JSON.")
    return parser.parse_args(argv)


def resolve_media(media_args: list[str]) -> list[Path]:
    if len(media_args) > 4:
        raise SystemExit("Twitter supports at most 4 media files per tweet.")

    resolved: list[Path] = []
    for raw_path in media_args:
        path = Path(raw_path).expanduser().resolve()
        if not path.exists():
            raise SystemExit(f"Media file not found: {raw_path}")
        if not path.is_file():
            raise SystemExit(f"Media path is not a file: {raw_path}")
        resolved.append(path)
    return resolved


def print_result(result: dict[str, object], as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    print(f"success: {result['success']}")
    print(f"tweet_id: {result['id']}")
    print(f"url: {result['url']}")
    print(f"media_count: {result['mediaCount']}")


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    media_paths = resolve_media(args.media)

    if args.dry_run:
        payload = {
            "success": True,
            "dryRun": True,
            "text": args.text,
            "replyTo": args.reply_to,
            "media": [str(path) for path in media_paths],
        }
        print_result(
            {
                "success": True,
                "id": "dry-run",
                "url": "dry-run",
                "mediaCount": len(media_paths),
                "payload": payload,
            },
            args.json,
        )
        if not args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    cookies = get_cookies()
    client = MediaTwitterClient(
        cookies["auth_token"],
        cookies["ct0"],
        cookie_string=cookies.get("cookie_string"),
    )

    media_ids = [client.upload_media(path) for path in media_paths]
    tweet_id = client.create_tweet_with_media(args.text, media_ids, reply_to_id=args.reply_to)
    result = {
        "success": True,
        "id": tweet_id,
        "url": f"https://x.com/i/status/{tweet_id}",
        "mediaCount": len(media_ids),
    }
    print_result(result, args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
