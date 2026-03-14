---
name: mj-banana-character-assets-prompt
description: "Use this skill when the user wants reusable prompt workflows for AI manhua or AI short-drama script assets with Midjourney and Banana Pro, including character face drafts, full-body base sheets, turnaround sheets, expression sheets, angle packs, scene masters, prop sheets, VFX keyframes, outfit-system unification, or fixing front/side/back direction issues. This skill enforces one pipeline: Midjourney generates base images only, Banana Pro handles all edits, repairs, extraction, and reintegration."
---

# MJ + Banana Script Assets

Use this skill for script-asset prompt writing when the project separates:

- `Midjourney` for base-image generation
- `Banana Pro` for all edits and corrections

Do not mix the two prompt styles.

## Core Rules

1. `Midjourney only for base images`
   - Use it for first-pass face drafts, full-body base sheets, turnaround sheets, expression sheets, angle packs, and rough outfit exploration.
   - Midjourney prompts may include model parameters such as `--ar`, `--v 7`, `--raw`, `--oref`, and `--ow`.

2. `Banana Pro only for edits`
   - Use it to fix clothing systems, unify characters into the same school/world, correct front/side/back pose errors, extract one view from a sheet, or merge a repaired view back into a sheet.
   - Banana Pro prompts should be short, edit-local, and specific to the current image state.
   - Do not write Midjourney-style repeated identity paragraphs for Banana Pro.
   - Do not include Midjourney parameters in Banana Pro prompts.

3. `One edit per Banana prompt when possible`
   - Good: fix side-view head direction
   - Good: change only the uniform structure
   - Bad: fix face, clothes, pose, background, and layout at once

4. `For sheets, lock engineering constraints explicitly`
   - State exact view count
   - State view order
   - State head/body/feet direction
   - State whether to preserve identity and outfit

## Asset Scope

This skill covers the still-image assets normally needed before video:

- `Character assets`
  - face drafts
  - full-body bases
  - turnaround sheets
  - expression sheets
  - angle packs
- `Scene assets`
  - recurring location masters
  - reverse-side masters
  - angle seeds
- `Prop assets`
  - hero props
  - cards / symbols
  - recurring devices
- `VFX assets`
  - anomaly frames
  - energy motifs
  - elemental look-dev frames
- `Repair assets`
  - extracted panels
  - repaired front/side sheets
  - reintegrated final sheets

## When To Use Which Tool

### Use Midjourney when the task is:

- generating a new character from scratch
- exploring alternate looks
- generating first-pass face sheets
- generating first-pass full-body sheets
- generating initial turnaround, expression, or angle packs
- generating recurring scene masters
- generating prop sheets
- generating VFX concept frames

### Use Banana Pro when the task is:

- keeping the same character but changing clothes
- aligning one character's outfit language to another character's school system
- aligning one scene to another scene's world design
- placing a character into an approved scene
- replacing a prop while preserving the scene
- refining a VFX frame while preserving composition
- fixing side-view head direction
- fixing front-view symmetry
- fixing shoe-tip direction
- removing duplicate views from a sheet
- extracting one view from a sheet
- inserting a repaired view back into the original sheet

## Prompt Writing Rules

### Midjourney Rules

- Write complete prompts because Midjourney is generating from scratch.
- Keep prompts image-like, not instruction-heavy.
- Lead with subject identity, then visual anchors, then clothing, then output type.
- For scenes, lead with geography and anchors.
- For props and VFX, lead with silhouette and material or energy logic.
- Include parameters at the end.
- For reference-driven generations, use `--oref` and `--ow` when identity matters.

### Banana Pro Rules

- Assume the current image already contains most of the needed information.
- Only mention what must change and what must not change.
- Name the preserved parts explicitly:
  - face
  - hairstyle
  - age
  - outfit
  - body proportion
  - pose
  - art style
- If fixing only one region, say `only adjust ...`.
- If preserving identity, say `do not turn into a generic template`.
- If preserving layout, say `preserve scale perspective and lighting`.
- If preserving a world system, say `same school/world system`.

## Script-To-Asset Workflow

Use this sequence unless the user asks for only one asset type:

1. `Character faces`
2. `Character full bodies`
3. `Character sheets`
4. `Outfit-system unification`
5. `Scene masters`
6. `Prop sheets`
7. `VFX frames`
8. `Repair / extraction / reintegration`

Reason:
- character identity drifts fastest
- scene geography should inherit approved character scale and costume logic
- props and VFX should inherit the world language after characters and scenes are stable

## Direction Constraints For Turnaround Sheets

Use these exact concepts whenever the user needs stable front/side/back sheets.

### Pure Front

Required constraints:

- `pure front view`
- `head body and feet all face forward`
- `left-right symmetrical standing pose`
- `both hands visible`
- `shoe tips point forward`

### Pure Side

Required constraints:

- `pure side view`
- specify `left-facing` or `right-facing`
- `head body and feet all face the same direction`
- `nose points left/right`
- `shoe tips point left/right`
- `not 3/4`
- `do not look back at the camera`

### Pure Back

Required constraints:

- `pure back view`
- `head body and feet all face away`
- `back-facing symmetrical standing pose`

### Exact View Count

When the sheet should have only three views, state:

- `strict character turnaround sheet`
- `exactly three views only`
- `left pure front, center left-facing pure side, right pure back`

## Output Shape

When the user asks for prompts, prefer this structure:

- `Midjourney Base Prompt`
- `Banana Pro Edit Prompt`
- `Direction Constraint`
- `Notes`

If the user asks only for one tool, return only that tool's prompt.

## Common Prompt Patterns

Use [references/prompt-patterns.md](references/prompt-patterns.md) when you need concrete prompt skeletons for:

- face drafts
- full-body bases
- scene masters
- reverse-side scene views
- prop sheets
- VFX keyframes
- outfit-system unification
- side-view repair
- front-view repair
- scene merge edits
- prop replacement
- VFX refinement
- removing extra views
- extracting one sheet panel
- reintegrating a repaired panel into a turnaround sheet

## Common Trigger Cases

- “帮我写 Midjourney 底图 prompt”
- “帮我写 Banana Pro 改图 prompt”
- “这个角色先用 MJ 出底图，后面用 Banana 改”
- “帮我做这个剧本的所有资产”
- “帮我写场景母图 prompt”
- “帮我写道具 prompt”
- “帮我写异象/VFX prompt”
- “把角色放进场景里”
- “把这个角色改成同一学校的制服”
- “三视图 side 的头和脚方向不对”
- “front view 不够正”
- “把中间的 side 抠出来修完再拼回去”
- “去掉多余的一个 side”
- “给我分开写 MJ 和 Banana 的提示词”
