# Repository Guidelines

## Project Structure & Module Organization
This repository is a lightweight workspace for local agent skills, helper scripts, and reference assets.

- `.agents/skills/`: installable or vendored skills. Each skill keeps its own `SKILL.md`, and some include full Python packages with `pyproject.toml`, source, and `tests/`.
- `scripts/`: repo-local utilities such as `cloudflare-crawl.mjs`, `xhs-*.py`, and `twitter-post-media.py`.
- `assets/`: static creative assets and source material. Treat large binaries and generated content as data, not code.
- `skills-lock.json`: lockfile for pinned skill sources and hashes.

## Build, Test, and Development Commands
There is no single root build or test command. Use the script or skill you are changing.

- `node scripts/cloudflare-crawl.mjs --help`: inspect and run the Cloudflare crawl helper.
- `python3 scripts/xhs-profile-dump.py --help`: dump Xiaohongshu profile data.
- `python3 scripts/xhs-expand-threads-batch.py --help`: expand stored XHS threads.
- `python3 scripts/twitter-post-media.py --dry-run "text" --media path/to/file.jpg`: validate Twitter media posts without sending.
- `cd .agents/skills/twitter-cli && uv run pytest -q`: run tests for the Twitter skill.
- `cd .agents/skills/xiaohongshu-cli && uv run ruff check . && uv run pytest -q`: lint and test the XHS skill.

## Coding Style & Naming Conventions
Match the style of the file you are editing.

- Python: 4-space indentation, type hints where useful, `snake_case` for functions/files, short module docstrings.
- JavaScript: ESM modules, semicolons, double quotes, and small focused functions.
- Keep repo-local scripts dependency-light and CLI-first. Prefer descriptive file names like `xhs-comment-page.py`.
- Only add comments when behavior is not obvious from the code.

## Testing Guidelines
Root-level scripts do not have a unified test suite; validate them with `--help`, `--dry-run`, or a narrow real invocation. For packaged skills, place tests under each skill’s `tests/` directory and follow `test_*.py` naming. Run the nearest skill-local test suite before submitting changes.

## Commit & Pull Request Guidelines
Recent history favors short, imperative subjects, usually with Conventional Commit prefixes such as `feat:`, `refactor:`, and `chore:`. Use `type: concise summary` when possible.

PRs should state the changed paths, the user-facing impact, required auth or `.env` setup, and exact verification commands. Include sample output or screenshots when a script changes visible CLI behavior or generated assets.

## Security & Configuration Tips
Do not commit `.env`, `.tmp/`, credentials, cookies, or generated reports. If a change touches authenticated flows, document the required local tools clearly, for example `uv tool install twitter-cli` or `uv tool install xiaohongshu-cli`.
