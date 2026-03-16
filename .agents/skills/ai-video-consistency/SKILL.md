---
name: ai-video-consistency
description: Plan SD2 or S2 first AI animation workflows with character continuity, scene continuity, shot breakdown, midpoint-frame anchors, shot bridging, tail-frame planning, and repository memory. Use when the user asks how to keep 角色一致性, 场景一致性, 分镜连续性, 接镜头, 中间帧大法, 定尾帧, 定景不定人, 首尾帧衔接, 镜头拆解, 批量生视频规划, 资产锁定, 剧本结构化, or wants to turn a script into a stable multi-shot SD2 animation workflow.
---

# AI Video Consistency

Use this skill to turn a story idea, script, scene list, or creator reference set into a consistency-first SD2 production plan.

Default mode:
- SD2 or S2 first
- asset-first, not prompt-first
- still-frame planning before video execution
- continuity anchors before long generation

## Read Order

Read only what the task needs.

- Read [references/xhs-author-derived-principles.md](references/xhs-author-derived-principles.md) first when the user wants creator-derived workflow guidance, the “小红书作者那套方法”, or asks about `中间帧大法`, `接镜头`, `定尾帧`, or `定景不定人`.
- Read [references/creator-failure-playbook.md](references/creator-failure-playbook.md) when the user asks why shots fail, why clips do not connect, or how to recover from drift.
- Read [references/ai-video-creation-playbook.md](references/ai-video-creation-playbook.md) when the user wants a broad “怎么做 AI 视频 / 少踩坑” summary.
- Read [references/repo-memory-contract.md](references/repo-memory-contract.md) when the user wants the breakdown, bibles, queue, or continuity plan persisted into the repository.
- Read [references/industrial-pipeline.md](references/industrial-pipeline.md) only when the user wants a larger script-to-batch system.
- Read templates only when generating that artifact:
  - [references/script-breakdown-template.md](references/script-breakdown-template.md)
  - [references/calibration-pack-template.md](references/calibration-pack-template.md)
  - [references/character-bible-template.md](references/character-bible-template.md)
  - [references/scene-master-template.md](references/scene-master-template.md)
  - [references/shot-continuity-checklist.md](references/shot-continuity-checklist.md)
  - [references/director-queue-template.md](references/director-queue-template.md)
  - [references/asset-prompt-pack-template.md](references/asset-prompt-pack-template.md)
  - [references/style-bible-template.md](references/style-bible-template.md)

## Workflow

1. Scope the continuity problem.
   - Identify recurring characters, recurring locations, key props, and the hardest continuity risk.
   - If the user already has a script, extract scenes, shots, and shot IDs immediately.

2. Lock static assets before motion.
   - Character first.
   - Scene master second.
   - Props and VFX third.
   - Do not treat SD2 as a replacement for weak asset prep.

3. Build shot anchors for SD2.
   - Use `Master Shot` when geography matters.
   - Use a midpoint frame when the sequence must stay continuous across cuts.
   - Use a tail frame when extension or ending state matters.
   - Use previous-shot state when two clips need to connect.

4. Decide how much the shot should constrain the person.
   - If motion continuity matters more than pose precision, lock scene first and let the person continue the previous action.
   - If placement matters more than motion freedom, lock blocking and use stronger visual anchors.

5. Keep the workflow asset-first.
   - Still-image planning first.
   - Video generation second.
   - Post repair, cutaways, and manual bridge shots when direct continuation fails.

6. Persist project memory when needed.
   - Default path: `assets/<项目名>/项目档案/`
   - Use canonical YAML plus rendered Markdown when the user wants long-term reuse.

## Output Shape

When helping the user, prefer this structure:

- `Workflow Summary`
- `Creator Workflow Summary` when the user wants creator-derived advice
- `Creator Failure Playbook` when the user asks how to avoid or recover from common failure modes
- `Script Breakdown`
- `Character Bible`
- `Scene Master Plan`
- `Midpoint / Tail / Bridge Plan`
- `Shot Continuity Checklist`
- `Director Queue`
- `Continuity Risks`
- `Repo Archive Update` when the project memory should be written back into the repository

Default to table-like outputs when the user is actively developing a project. Use the template reference files instead of inventing a new structure each time.

## Working Rules

- Optimize for repeatability, not one-shot magic.
- Treat consistency as a workflow problem first, not a prompt problem first.
- Prefer controllability before automation.
- Prefer consistency before spectacle.
- Prefer one primary engine per stage.
- Use one image to carry continuity when words are not precise enough.
- Recommend testing one hard sequence before building the full episode.

## Common Trigger Cases

- “这个角色怎么保持一致”
- “帮我把剧本拆成场景和分镜”
- “帮我做 SD2 分镜校准”
- “帮我做导演队列 / 批量生视频规划”
- “多机位为什么一切就乱了”
- “帮我把这个剧本拆成能稳定生成的视频流程”
- “怎么把小红书作者那种 workflow 用到我自己的故事里”
- “只基于作者自己说的话总结”
- “这些镜头为什么总翻车”
- “这两个镜头为什么接不上”
- “中间帧大法怎么用”
- “定尾帧怎么做”
- “定景不定人怎么写”
- “AI 视频常见失败怎么修”
- “这个技能拆分出的剧本应该沉淀在代码库中”
- “把拆分结果保存到仓库里，方便续集”
