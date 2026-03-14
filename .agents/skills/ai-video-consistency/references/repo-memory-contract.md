# Repo Memory Contract

Use this when the project should survive beyond the chat and remain reusable for sequels.

## Canonical Meaning

In this workflow, `canonical` means the single long-term authoritative version stored in the repository.

- Chat replies, temporary prompt drafts, and exploratory notes are not canonical by default.
- Repository archive files under `assets/<项目名>/项目档案/` are canonical once confirmed.
- Future sequels, asset revisions, and prompt generation should read canonical repo files first instead of rebuilding memory from chat context.

## Default Storage

Persist canonical outputs to:

`assets/<项目名>/项目档案/`

Default structure:

- `series/`
  - cross-episode canon
  - recurring characters
  - recurring scenes
  - recurring props and VFX
- `episodes/epXXX/`
  - normalized script
  - breakdown
  - continuity plan
  - director queue
  - asset manifest

## Default File Set

For `series/`, prefer paired `.md + .yaml`:

- `series-bible`
- `style-bible`
- `character-bible`
- `scene-bible`
- `prop-vfx-bible`

For each `episodes/epXXX/`, prefer paired `.md + .yaml`:

- `script-normalized`
- `breakdown`
- `continuity-plan`
- `director-queue`
- `asset-manifest`

## Rules

1. Repository files are the canonical memory, not the chat.
2. Use stable IDs for characters, locations, props, VFX, and shots.
3. Record the real committed asset paths that exist in the repo.
4. If an asset exists conceptually but is not committed yet, mark it `planned` or `missing`.
5. Do not silently rename existing asset paths in archive files unless the real files are renamed too.
6. When a new sequel or batch is added, add a new `epXXX/` folder instead of overwriting the old one.

## Canonical Update Checklist

When a new asset is committed to the repo, update canonical memory in this order:

1. Confirm the real committed path and stable asset ID.
2. Update the current episode's `asset-manifest` first.
3. Update the matching series bible:
   - character asset -> `character-bible`
   - scene master -> `scene-bible`
   - prop or card -> `prop-vfx-bible`
   - VFX plate or anomaly -> `prop-vfx-bible`
4. If the new asset changes global visual rules, update `style-bible`.
5. If the asset changes shot execution dependencies, update the episode's `director-queue` or `continuity-plan`.

Do not treat an asset as canonical until steps 1-3 are complete.

## Recommended ID Shapes

- character: `CHAR_*`
- location: `LOC_*`
- prop: `PROP_*`
- vfx: `VFX_*`
- shot: `EPXXX-Sxx-SHxx`
