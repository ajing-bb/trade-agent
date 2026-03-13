# Shot Continuity Checklist

Use this template when turning a script into executable shots.

## How To Use

- Fill one row per shot, not per scene paragraph.
- Keep the shot objective simple: one shot should solve one storytelling beat.
- Mark high-risk shots early so the user tests them before scaling the project.
- Add a `Seedance Mode` only after the still-image planning is stable.

## Table

| Shot ID | Story Beat | Scene | Characters | Shot Type / Framing | Camera Angle / Movement | Action Core | Key Props / VFX | Source Assets Needed | Continuity Risk | Recommended Build Method | Seedance Mode | Success Criteria | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Example: 01-1A | 孟江站上抽卡池前的准备 | 神风学院操场 | 孟江、围观学生 | 中景 | 平视，轻推近 | 手按按钮前的蓄力 | 抽卡池 | 孟江正面设定、操场 master shot、抽卡池特写图 | Medium | 先静帧锁人和池位置，再视频轻推 | image referenced | 孟江脸不漂、池体结构不漂、围观人群不抢戏 | 开场建立世界 |

## Recommended Build Method Values

Use one of these short labels:
- `still first`
- `master-shot crop`
- `image merge`
- `regional composite`
- `first/last frame`
- `layered video`
- `video reference`
- `manual post fix`

Combine when necessary, for example:
- `master-shot crop + image merge`
- `still first + first/last frame`

## Continuity Risk Levels

Low:
- single character
- simple reaction
- stable environment

Medium:
- two-character dialogue
- moderate camera change
- hero prop emphasis

High:
- many characters in frame
- strong VFX and dialogue together
- large angle jump
- identity-critical reveal
- long continuous shot

## Success Criteria Examples

Good:
- “主角脸型、发型、制服轮廓稳定，抽卡池位置与前镜头一致”
- “反打镜头里桌椅布局与前镜头相互对应”
- “哪吒法器全部到位，且不串成无关道具”

Bad:
- “看起来对”
- “差不多”

## When To Escalate A Shot

Escalate from plain prompting to a more controlled build method when:
- the character identity is mission-critical
- the angle jump is large
- more than two important characters share one frame
- the shot introduces a recurring environment
- the shot contains signature VFX or signature props

## Seedance Mode Suggestions

Common values:
- `text only`
- `@图片 reference`
- `@视频 reference`
- `first frame`
- `first/last frame`
- `extend`
- `edit`

Prefer not to assign a Seedance mode until the asset dependency column is complete.
