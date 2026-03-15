#!/usr/bin/env python3
"""Compatibility wrapper for the unified archive CLI."""

from archive.archive_cli import main


if __name__ == "__main__":
    raise SystemExit(main())
