# Series Bible

> Generated from `series-bible.yaml`. Do not edit this Markdown manually.

## 项目摘要

| 字段 | 值 |
| --- | --- |
| 项目 ID | `ONLY_EASTERN_GODS` |
| 项目名 | 只有我能抽出东方神明 |
| 当前导入范围 | opening ~ episode_3 |
| 作品形态 | AI漫剧 |
| 主叙事钩子 | 西方神魔独占的抽卡世界里，只有穿越者孟江能抽出东方神明，并以连续异象打破既有秩序。 |

## 世界观硬规则

1. 世界公开抽卡体系默认只承认西方神魔卡牌，学院与城市公共秩序均围绕该体系建立。
2. 东方神明在这个世界属于异常存在，出现时应与西方神魔体系形成强烈视觉反差。
3. 抽卡异象不是普通背景特效，而是决定人物地位和世界反应的叙事事件。
4. 孟江的能力建立在东方神明召唤上，前期核心戏剧张力来自异象巨大但力量兑现节奏不对称。

## 审美与制作规则

1. 先角色后场景再道具和VFX
2. SD2 / S2 默认先做静帧与 continuity anchor，再做视频执行
3. 复杂连续段默认采用中间帧、尾帧、上一镜状态引用三件套，不直接长段裸跑
4. 角色资产优先走 Face Draft -> Full Body Master -> Banana Derived Pack
5. Midjourney 只做各类资产的第一个 canonical base / master asset，不负责后续派生包
6. Banana Pro 统一基于定稿做后续派生，例如角色三视图、表情、角度，场景反打与机位变体，道具变体，VFX look-dev 变体
7. Banana Pro 派生提示词默认显式写 请参考当前资产定稿 或 请参考当前人物全身照

## Canonical 使用规则

1. 本目录与 episodes 中已确认的档案文件，构成本项目的 canonical memory
2. 后续续集、资产补画、Seedance prompt、角色返修，默认先读 canonical 档案，再参考聊天记录
3. 如果聊天结论与仓库档案冲突，以仓库中最新确认版本为准
4. 临时探索图、未落盘图片、未写回档案的 prompt 结论，不视为 canonical

## 稳定 ID 规则

- 角色：`CHAR_`
- 场景：`LOC_`
- 道具：`PROP_`
- 特效：`VFX_`
- 镜头：`EP001-`

## 当前导入说明

- {datetime.date(2026, 3, 16): '项目执行 hard reset，仅保留源剧本后重新导入。'}
- {datetime.date(2026, 3, 16): '当前 series 层为 SD2-first 规划态，角色/场景/道具/VFX 先以 planned 建档。'}
