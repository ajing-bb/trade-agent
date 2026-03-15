# EP001 Director Queue

> Generated from `director-queue.yaml`. Do not edit this Markdown manually.

## Queue Rules

- `blocked`：关键资产还未正式落盘，镜头不能进入生成阶段
- `ready`：关键资产已齐，可进入静帧或首尾帧生成
- `in_progress`：镜头正在制作
- `done`：镜头已完成并通过当前轮验收

| Shot ID | Purpose | Asset Gate | Primary Refs | Execution Mode | Queue Status | Next Action | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `EP001-S00-SH01` | 世界观建立 | `LOC_KAMIKAZE_PLAYGROUND_DAY`、`PROP_CARD_POOL_SCHOOL`、`ARCH_STUDENT_GENERIC` 未落盘 | LOC_KAMIKAZE_PLAYGROUND_DAY scene master、PROP_CARD_POOL_SCHOOL master、ARCH_STUDENT_GENERIC full body master | `image` | `blocked` | 先落盘操场母图、学院抽卡池和学生模板群，再做 montage 静帧 | 先做无学生近景版世界观静帧 |
| `EP001-S01-SH01` | 抽卡前蓄势 | `LOC_KAMIKAZE_PLAYGROUND_DAY`、`ARCH_STUDENT_GENERIC` 未落盘 | CHAR_MENGJIANG full body、CHAR_MENGJIANG angle pack、LOC_KAMIKAZE_PLAYGROUND_DAY scene master、ARCH_STUDENT_GENERIC angle pack | `image` | `blocked` | 先落盘操场母图和学生模板群，再合成孟江抽卡前中景 | 改为单人中景，无群演版 |
| `EP001-S01-SH02` | 金色异象降临 | `LOC_KAMIKAZE_PLAYGROUND_DAY`、`VFX_GOLDEN_SKY`、`VFX_RAINBOW_PILLAR` 未落盘 | LOC_KAMIKAZE_PLAYGROUND_DAY golden omen variant、VFX_GOLDEN_SKY master、VFX_RAINBOW_PILLAR master | `first-last` | `blocked` | 先落盘操场母图与金色异象特效，再做首尾帧 | 分层做天空与地面版本 |
| `EP001-S01-SH03` | 通天教主失败 | `CARD_TONGTIAN`、`CHAR_OLD_PROFESSOR` 未落盘 | CARD_TONGTIAN closeup variant、CHAR_MENGJIANG expression pack、CHAR_OLD_PROFESSOR expression pack | `image-merge` | `blocked` | 先落盘通天卡和老教授角色包，再做失败反应镜头 | 先做无老教授版本 |
| `EP001-S02-SH01` | 食堂分手羞辱 | `LOC_CAFETERIA_DAY`、`ARCH_STUDENT_GENERIC` 未落盘 | LOC_CAFETERIA_DAY scene master、CHAR_MENGJIANG full body、CHAR_LIN_QIANQIAN full body、CHAR_ZHANG_HE full body、ARCH_STUDENT_GENERIC reaction sheet | `image` | `blocked` | 先落盘食堂母图和学生模板群，再做对峙反打 | 先做主角三人版单向 coverage |
| `EP001-S03-SH01` | 夜间抽卡启动 | `LOC_PUBLIC_CARD_POOL_NIGHT`、`PROP_POINTS_CARD`、`PROP_CARD_POOL_PUBLIC`、`VFX_RED_SKY` 未落盘 | LOC_PUBLIC_CARD_POOL_NIGHT scene master、PROP_POINTS_CARD closeup variant、PROP_CARD_POOL_PUBLIC scene variant、VFX_RED_SKY shared variant | `first-last` | `blocked` | 先落盘夜景抽卡池、积分卡和赤红夜空，再做首尾帧 | 先做静帧锁构图 |
| `EP001-S04-SH01` | 多地反应 | `LOC_HEADMASTER_OFFICE_DAY`、`LOC_SENIOR_DORM_WINDOW_NIGHT`、`LOC_ZHANG_RESIDENCE_NIGHT`、`CHAR_SITU_QINGQING`、`CHAR_ZHANG_QIANG`、`VFX_RED_SKY` 未落盘 | LOC_HEADMASTER_OFFICE_DAY window reaction angle、LOC_SENIOR_DORM_WINDOW_NIGHT reaction angle、LOC_ZHANG_RESIDENCE_NIGHT father_son reaction angle、CHAR_SITU_KUNLUN full body、CHAR_SITU_QINGQING full body、CHAR_LIN_QIANQIAN full body、CHAR_ZHANG_HE full body、CHAR_ZHANG_QIANG full body、VFX_RED_SKY shared variant | `image` | `blocked` | 先落盘三套反应场景与缺失角色，再做多地蒙太奇 | 先拆成校方线、宿舍线、张家线三条单独制作 |
| `EP001-S05-SH01` | 哪吒觉醒 | `CARD_NEZHA`、`PROP_FENGHUO_WHEELS`、`PROP_FIRE_TIPPED_SPEAR`、`PROP_RED_SASH`、`VFX_NEZHA_DHARMA`、`LOC_PUBLIC_CARD_POOL_NIGHT` 未落盘 | CARD_NEZHA closeup variant、PROP_FENGHUO_WHEELS master、PROP_FIRE_TIPPED_SPEAR master、PROP_RED_SASH master、VFX_NEZHA_DHARMA character variant、LOC_PUBLIC_CARD_POOL_NIGHT upward hero angle | `layered-video` | `blocked` | 先落盘哪吒卡、法器组、法相和夜景抽卡池，再做分层视频 | 先拆成法器显形段和法相显形段 |

## Status Notes

- 当前没有镜头达到 ready，原因不是分镜不清，而是关键资产还没正式提交到仓库
- 当一个镜头所需的 scene master + 必要角色包 + 必要道具/VFX master 全部落盘后，才能从 blocked 改成 ready
- EP001-S04-SH01 和 EP001-S05-SH01 是本批次的最高风险镜头，应该最后进入生成
