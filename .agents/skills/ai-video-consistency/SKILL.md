---
name: ai-video-consistency
description: Plan character, scene, storyboard, asset, calibration, batch-routing, and continuity consistency for narrative AI video projects before prompt writing or generation. Use when the user asks how to keep 角色一致性, 场景一致性, 多机位一致性, 多角色调度, 分镜连续性, 首尾帧衔接, 分层方案, 镜头拆解, master shot 设计, 剧本结构化, 分镜校准, 角色校准, 场景校准, 导演队列, 批量生图, 批量生视频, 资产锁定, 生图提示词, 角色定稿 prompt, 场景母图 prompt, 道具/VFX 资产 prompt, or wants to turn a script into a stable multi-shot AI-video workflow. Use before or alongside `$seedance` when Seedance prompts alone are not enough to guarantee consistency.
---

# AI Video Consistency

Use this skill to turn a story idea, script, scene list, or creator reference set into a consistency-first production plan.

This skill now supports both:
- a consistency-first creative workflow
- an industrial script-to-batch pipeline inspired by AI manhua production tools

Read [references/ai-video-creation-playbook.md](references/ai-video-creation-playbook.md) first when the user needs a broad strategic summary of AI video creation, tool routing, pitfalls, or “少踩坑” guidance. Read [references/xhs-author-derived-principles.md](references/xhs-author-derived-principles.md) when the user explicitly wants creator-derived workflow guidance, wants the “小红书作者那套方法”, or wants conclusions based only on the creator's own words. Read [references/creator-failure-playbook.md](references/creator-failure-playbook.md) when the user asks why shots fail, how to avoid common drift, or how to recover from unstable AI-video outputs. Read [references/industrial-pipeline.md](references/industrial-pipeline.md) when the user wants an end-to-end industrial workflow, script-to-batch pipeline, desktop-tool style production flow, or asks how to organize “剧本 -> 角色 -> 场景 -> 导演 -> Seedance” as one system. Read [references/script-breakdown-template.md](references/script-breakdown-template.md) when the user needs script parsing and structured scene/shot extraction. Read [references/calibration-pack-template.md](references/calibration-pack-template.md) when the user needs prompt refinement for scene, shot, character, or emotional calibration before generation. Read [references/director-queue-template.md](references/director-queue-template.md) when the user wants batch routing, shot assignment, first/last-frame planning, or provider/model mapping. Read [references/consistency-sop.md](references/consistency-sop.md) for the detailed workflow, [references/character-bible-template.md](references/character-bible-template.md) for recurring character lock tables, [references/scene-master-template.md](references/scene-master-template.md) for recurring location planning, [references/shot-continuity-checklist.md](references/shot-continuity-checklist.md) for per-shot execution planning, [references/asset-prompt-pack-template.md](references/asset-prompt-pack-template.md) for reusable asset prompt outputs, [references/midjourney-asset-prompting.md](references/midjourney-asset-prompting.md) for Midjourney-specific asset prompting rules, and [references/seedance-handoff.md](references/seedance-handoff.md) when the project will later be executed in `$seedance`.

## Workflow

1. Determine project scope before writing prompts.
   - If the user asks a broad “how to do AI video well” question, start with the playbook summary before moving to templates.
   - If the user asks for creator-derived advice, source that summary from the creator-principles reference instead of generic audience commentary.
   - If the user asks why the current workflow keeps failing, source the diagnosis from the creator failure playbook instead of inventing generic prompt tweaks.
   - If the user asks for a production pipeline or software-style workflow, switch to the industrial pipeline framing instead of only giving creative advice.
   - Identify recurring characters, recurring locations, key props, signature VFX, and the most difficult continuity risks.
   - If the user already has a script, extract these items explicitly.

2. Structure the script before generation.
   - Break the script into scenes, shots, characters, dialogue, emotion beats, and camera intent.
   - Normalize recurring names, locations, props, and action verbs.
   - Create shot IDs early so later image, video, and asset tasks can map back to the same structure.

3. Build the calibration pack.
   - Calibrate scene prompts with environment, atmosphere, time of day, lighting, and material cues.
   - Calibrate shot prompts with lens logic, framing, angle, camera motion, and edit intent.
   - Calibrate character prompts with appearance anchors, costume anchors, expression targets, and motion behavior.
   - Do this before batch image or video generation.

4. Lock assets in this order.
   - Character bible
   - Style bible
   - Scene master shots
   - Props and VFX bible
   - Shot list
   Do not jump to video generation until these are stable.

5. Build the consistency plan.
   - Decide which scenes need a `Master Shot`.
   - Decide where to split character and background generation.
   - Decide which shots need region-based compositing, layered video, or first/last-frame control.
   - Identify which shots can tolerate model freedom and which need tight control.

6. Route each task to the right tool class.
   - Use image generation/editing tools to lock character look, scene design, camera angle seeds, and keyframes.
   - Use video models only after the static assets are stable.
   - Use `$seedance` for execution prompts, multi-modal references, first/last-frame prompts, video extension, and edit prompts after the consistency plan exists.
   - If the user wants industrial batch flow, define provider routing and retry strategy at the same time as model routing.

7. Produce practical outputs.
   - Script breakdown
   - Calibration pack
   - Character bible table
   - Scene master table
   - Shot-by-shot continuity checklist
   - Asset prompt pack
   - Director queue / batch routing plan
   - Model/tool routing notes
   - Risk list and fallback plan

## Output Shape

When helping the user, prefer this structure:

- `Workflow Summary` for broad strategy requests
- `Creator Workflow Summary` when the user wants creator-derived advice
- `Creator Tool Routing` when the user asks what each tool/model should handle
- `Creator Failure Playbook` when the user asks how to avoid or recover from common failure modes
- `Project Adaptation` when the user wants the creator logic translated to a target style such as 2D manhua, stylized 3D, or semi-real CG
- `Script Breakdown`
- `Calibration Pack`
- `Character Bible`
- `Scene Master Plan`
- `Shot Continuity Checklist`
- `Asset Prompt Pack`
- `Director Queue`
- `Provider / Model Routing`
- `Continuity Risks`
- `Seedance Handoff` when prompt writing is needed
- `Seedance Multi-Shot Plan` when the user wants multi-shot stitched narrative generation

Default to table-like outputs when the user is actively developing a project. Use the template reference files instead of inventing a new structure each time.

If the user asks for prompt writing immediately, first give the minimum viable consistency plan, then hand off to `$seedance`.

## Working Rules

- Optimize for repeatability, not one-shot magic.
- Treat consistency as a workflow problem first, not a prompt problem first.
- Treat industrialization as a data-flow problem: one stage's output should be reusable as the next stage's input.
- Prefer controllability before automation.
- Prefer consistency before spectacle.
- Prefer one primary model per stage; use secondary models only for gaps.
- Keep the user from over-trusting lip-sync, multi-character long shots, or large camera-angle changes without prebuilt assets.
- For multi-shot projects, always recommend testing one representative scene before building the full episode.
- When generating still-image asset prompts for Midjourney, prefer short, concrete prompts plus the right reference type and parameters over instruction-heavy prose.
- When the user wants scale or batch execution, define:
  - task unit (`shot`, `scene`, `asset pack`, `video segment`)
  - provider routing
  - retry policy
  - status fields
  - handoff fields between still-image and video stages

## Common Trigger Cases

- “这个角色怎么保持一致”
- “帮我把剧本拆成场景和分镜”
- “帮我做分镜校准 / 场景校准 / 角色校准”
- “帮我做导演队列 / 批量生图 / 批量生视频规划”
- “多机位为什么一切就乱了”
- “帮我把这个剧本拆成能稳定生成的视频流程”
- “Seedance 有没有办法直接解决一致性”
- “我应该先做角色还是先写 prompt”
- “怎么把小红书作者那种 workflow 用到我自己的故事里”
- “只基于作者自己说的话总结”
- “这些镜头为什么总翻车”
- “AI 视频常见失败怎么修”
- “AI 视频创作到底该怎么做”
- “怎么做工业化批量生产”
- “剧本到成片怎么串起来”
- “先给我一版少踩坑总结”
- “帮我写角色定稿图 prompt”
- “帮我写场景母图 prompt”
- “帮我写 Midjourney 资产提示词”
