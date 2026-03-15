# EP001 Director Queue

> Generated from `director-queue.yaml`. Do not edit this Markdown manually.

## Queue Rules

- `blocked`：关键资产还未正式落盘，镜头不能进入生成阶段
- `ready`：关键资产已齐，可进入静帧或首尾帧生成
- `in_progress`：镜头正在制作
- `done`：镜头已完成并通过当前轮验收

| Shot ID | Purpose | Asset Gate | Primary Refs | Execution Mode | Queue Status | Next Action | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `EP001-S02-SH01` | 白天操场抽卡开场 wide reveal，先建立孟江与抽卡池、人群、学院空间关系。 | `CHAR_MENGJIANG`、`LOC_ACADEMY_PLAYGROUND_DAY`、`PROP_DRAW_POOL_DEVICE` 未落盘 | CHAR_MENGJIANG full body master、LOC_ACADEMY_PLAYGROUND_DAY scene master、PROP_DRAW_POOL_DEVICE master | `still_frame_first` | `blocked` | 等孟江全身母图、操场场景母图和抽卡池装置母图落盘后，先做无强特效的角色入场 wide shot。 | 如果操场大场景暂时不稳定，先做中景版池边站位，再回补大广角。 |
| `EP001-S02-SH03` | 孟江抽卡前的坚定情绪镜头，作为白天线的人物识别确认帧。 | `CHAR_MENGJIANG`、`LOC_ACADEMY_PLAYGROUND_DAY` 未落盘 | CHAR_MENGJIANG face draft、LOC_ACADEMY_PLAYGROUND_DAY scene master | `character_first_close_medium` | `blocked` | 等孟江 face draft 与操场母图落盘后，先做近中景情绪版，不急着叠金色异象。 | 如果场景合成不稳定，先出纯灰底角色情绪参考，再做场景合成。 |
| `EP001-S02-SH09` | 校长办公室父女对话，承担对异象的高层解释功能。 | `CHAR_SITUKUNLUN` 未落盘 | LOC_HEADMASTER_OFFICE_DAY planned master、CHAR_SITUKUNLUN planned design、CHAR_SITUQINGQING planned design | `hold_for_batch_two` | `blocked` | 第二批补办公室与司徒父女资产后再执行，目前只记录为解释位优先镜头。 | 若角色资产未齐，先只做办公室空镜与窗边反应 plate。 |
| `EP001-S04-SH01` | 夜间公共抽卡池第一次出场，建立孟江单人、城市天际线和抽卡池的关系。 | `CHAR_MENGJIANG`、`LOC_PUBLIC_DRAW_POOL_NIGHT`、`PROP_DRAW_POOL_DEVICE` 未落盘 | CHAR_MENGJIANG full body master、LOC_PUBLIC_DRAW_POOL_NIGHT scene master、PROP_DRAW_POOL_DEVICE master | `still_frame_first` | `blocked` | 等夜景母图和孟江全身母图落盘后，先做无异象版站位图，作为后续红色异象底板。 | 如果夜景 skyline 不稳定，先缩小景别，保住抽卡池和人物站位。 |
| `EP001-S04-SH03` | 右手按下按钮的操作特写，建立夜间抽卡动作的机械逻辑。 | `LOC_PUBLIC_DRAW_POOL_NIGHT`、`PROP_DRAW_POOL_DEVICE` 未落盘 | PROP_DRAW_POOL_DEVICE master、LOC_PUBLIC_DRAW_POOL_NIGHT scene master | `prop_insert_close_up` | `blocked` | 等抽卡池装置母图落盘后，先裁出按钮与卡槽逻辑，再做手部操作特写。 | 如果完整场景先不稳，先单独出装置 3/4 视图和按钮 close-up。 |
| `EP001-S04-SH07` | 孟江夜间确认“成了？”的角色镜头，用于承接红色异象前的情绪翻转。 | `CHAR_MENGJIANG`、`LOC_PUBLIC_DRAW_POOL_NIGHT` 未落盘 | CHAR_MENGJIANG face draft、LOC_PUBLIC_DRAW_POOL_NIGHT scene master | `character_medium_with_light_fx` | `blocked` | 等孟江 face draft 与夜景母图落盘后，先做受红光映射的中景确认帧，再考虑后续强特效版本。 | 如果红光映射难稳定，先做无 VFX 中景，后期在 Banana 或视频阶段补红光。 |

## Status Notes

- 已完成第一轮文字级 canon 锁定，但当前仍没有 committed 视觉资产。
- 孟江、神风学院操场、公共抽卡池和抽卡池装置已进入 prompted，正在等待首批 Midjourney 母图结果。
- 司徒父女、校长办公室、通天教主卡、哪吒卡与关键异象已进入 prompted，可在第二批继续补解释位与特效位。
- 执行顺序参考 episodes/ep001/batch-01-execution.md。
