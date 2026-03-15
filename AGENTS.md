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

## AI Manhua Workflow
For this repository's AI manhua / AI short-drama creation workflow, use the following default system unless the user explicitly overrides it.

- Treat repository archives as canonical memory. Chat discussion, exploratory prompts, and temporary conclusions are not canonical by default.
- Canonical project memory lives under `assets/<项目名>/项目档案/`.
- If `assets/<项目名>/项目档案/` does not exist, treat the project as a true fresh start with no canonical memory yet. In that case, do not infer old canon from prior chats or deleted files; rebuild the archive only when the user explicitly starts `ai-video-consistency` work again.
- Read canonical files before continuing sequel work, revisions, or prompt generation:
  - `series/series-bible`
  - `series/style-bible`
  - `series/character-bible`
  - `series/scene-bible`
  - `series/prop-vfx-bible`
  - current `episodes/epXXX/` breakdown, continuity-plan, director-queue, and asset-manifest
- For structured production archive files, use `YAML` as the canonical single source of truth and treat Markdown as generated read-only views.
- Current YAML-canonical files:
  - `series/series-bible.yaml`
  - `series/style-bible.yaml`
  - `series/character-bible.yaml`
  - `series/character-asset-prompt-pack.yaml`
  - `series/scene-bible.yaml`
  - `series/scene-asset-prompt-pack.yaml`
  - `series/prop-vfx-bible.yaml`
  - `series/prop-vfx-asset-prompt-pack.yaml`
  - `episodes/epXXX/breakdown.yaml`
  - `episodes/epXXX/continuity-plan.yaml`
  - `episodes/epXXX/script-normalized.yaml`
  - `episodes/epXXX/asset-manifest.yaml`
  - `episodes/epXXX/director-queue.yaml`
- Do not manually edit generated Markdown for those files. Update the YAML first, then run:
  - `python3 scripts/render-project-archive.py assets/<项目名>/项目档案`
- To wipe a project back to only its source script, use:
  - `python3 scripts/reset-project-creation.py assets/<项目名> --yes`
- To wipe a project and immediately recreate an empty archive skeleton, use:
  - `python3 scripts/reset-project-creation.py assets/<项目名> --rebuild-skeleton --yes`
- To initialize a fresh project archive from the remaining source script, use:
  - `python3 scripts/init-project-archive.py assets/<项目名>`
- Optional repo automation:
  - install hooks with `sh scripts/install-git-hooks.sh`
  - current `pre-commit` hook auto-renders generated Markdown from YAML before commit
  - hooks enforce sync, but they do not infer semantic progress changes for you

### Tool Boundary
- `Midjourney` is for base images only:
  - character face drafts
  - character full-body masters
  - scene masters
  - prop / VFX base plates
- `Banana Pro` is the default editor for all revisions:
  - generate turnaround / expression / angle packs from an approved character master
  - generate reverse angles / shot variants from an approved scene master
  - generate prop / VFX variants from an approved master asset
  - costume unification
  - front / side / back correction
  - single-panel extraction
  - image repair
  - reinserting repaired panels into turnaround sheets
- `Seedance` is used after assets are stable, for video prompt execution and shot generation.
- `Jianying` / 剪映 handles post-production and publishing assembly:
  - shot stitching
  - subtitles
  - dubbing / voice
  - music and SFX
  - final export variants

### Prompting Rules
- Default character pipeline:
  - `Face Draft -> Full Body Master -> Banana Derived Pack`
  - first lock the face in Midjourney using a face draft or half-body close-up
  - then use that face draft as the highest-priority reference to generate the full-body master
  - then generate turnaround / expression / angle assets in Banana Pro from that approved full-body master
- Default scene / prop / VFX pipeline:
  - `Midjourney master -> Banana derived variants`
  - do not keep re-generating parallel variants in Midjourney after one usable master is approved
- Do not use Midjourney as the primary repair tool once a usable base image exists.
- Do not write Banana Pro prompts in Midjourney style. Banana Pro prompts should be short, local, and edit-specific.
- For Banana Pro derived prompts, explicitly reference the approved master:
  - use phrases like `请参考当前资产定稿`
  - for characters, use phrases like `请参考当前人物全身照`
  - treat the approved master as the only primary identity / layout reference unless the user explicitly overrides it
- For Banana Pro, prefer one edit objective at a time:
  - only fix side-view direction
  - only unify costume
  - only remove duplicate view
  - only replace the center turnaround panel
- For turnaround sheets, explicitly constrain direction when needed:
  - front must be pure front
  - side must specify left-facing or right-facing
  - head, body, and feet must face the same direction
  - nose direction and shoe-tip direction should be stated when side-view drift is likely

### Canonical Update Order
Whenever a new asset is actually committed to the repo, update memory in this order:

1. Confirm the real committed path and stable asset ID.
2. Update the current episode's `asset-manifest`.
3. Update the matching series bible YAML:
   - character asset -> `series/character-bible`
   - scene master -> `series/scene-bible`
   - prop / card / weapon / anomaly -> `series/prop-vfx-bible`
4. If the asset changes global visual rules, update `series/style-bible`.
5. If the asset changes shot dependencies, update `director-queue` or `continuity-plan`.
6. Re-render generated Markdown from YAML for the structured archive files.

Do not treat an asset as canonical until steps 1-3 are complete.

### Progress Tracking
- This workflow is expected to survive Codex exits and later resumptions.
- If any of the following changes, update repository memory before ending the work session:
  - a new asset master or face draft is approved
  - an asset moves from `planned` to `prompted`
  - an asset moves from `prompted` to `committed`
  - a global workflow or style rule changes
  - a shot's blocking state changes in `director-queue`
- Keep `director-queue` as a production queue, not just a shot list:
  - record blocking assets
  - record primary refs
  - record the next action
  - record fallback execution
- Prefer checking `assets/<项目名>/项目档案/progress-update-sop.md` before wrapping up a session.
