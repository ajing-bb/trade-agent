# EP001 Continuity Plan

> Generated from `continuity-plan.yaml`. Do not edit this Markdown manually.

## 高优先级锁定项

1. 孟江必须先锁定 face draft 与 full body master，后续所有近景、低机位和异象反光都以此为准。
2. 神风学院操场白天 master 与公共抽卡池夜景 master 必须先做出来，再拆分反打和特写。
3. 抽卡池装置、标准卡面、通天教主卡、哪吒卡应先统一外观体系，避免不同场次像不同项目。
4. 金色天空异象和赤红天穹异象必须在色相与材质上彻底分层，不能混成同一套 VFX。

## Shot Build Policy

| Shot ID | Build Method | Why |
| --- | --- | --- |
| `EP001-S02-SH01` | `scene_master + character_composite` | 白天操场第一次正式亮相，需要先用操场母图锁空间，再把孟江放到抽卡池前。 |
| `EP001-S02-SH03` | `character_close_medium over scene_plate` | 这是孟江抽卡前的关键情绪镜头，重点是脸和姿态稳定，不需要先上大特效。 |
| `EP001-S04-SH01` | `scene_master + character_composite` | 夜间公共抽卡池第一次亮相，需要先锁夜景与孟江的单人站位。 |
| `EP001-S04-SH03` | `prop_insert close-up` | 按钮按下是后续红色异象的起点，先用抽卡池装置细节建立操作逻辑。 |
| `EP001-S04-SH07` | `character_medium over night_plate` | 孟江一句“成了？”是夜间第二段的重要角色确认镜头，先保人物稳定，再叠加异象反光。 |
| `EP001-S02-SH09` | `dialogue_two_shot on office_master` | 校长办公室双人对话是世界观解释位，适合在大 VFX 前先建立高层观察关系。 |

## Continuity Risks

| 风险 | 说明 | 对策 |
| --- | --- | --- |
| 人群镜头漂移 | 操场与食堂都有围观镜头，若把群演当独立角色逐张生成，脸和制服会快速漂移。 | 只锁定男女学生群演模板各一套，前景有限复用，背景人群软化处理。 |
| 异象覆盖掉环境锚点 | 金色或赤红异象太强时，容易把学院与公共抽卡池做成抽象背景。 | 先生成稳定环境 plate，再叠加 VFX，确保建筑、地面纹样和抽卡池结构始终可读。 |
| 东方与西方体系视觉混线 | 如果雕像、卡面和异象语言没有严格分流，观众会看不出东方神明的异常性。 | 西方体系坚持冷硬石雕和暗色能量，东方体系只用古金或火红加更干净的神性几何。 |
| 男主近景脸型不稳定 | 孟江要同时承受校园弱者与神性爆发两种状态，最容易在近景中跑脸。 | 先做 face draft，再用同脸锁 full body，之后近景和低机位都从这套母图派生。 |
