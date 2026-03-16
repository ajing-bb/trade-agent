# Style Bible

> Generated from `style-bible.yaml`. Do not edit this Markdown manually.

## Style Summary

| Field | Value |
| --- | --- |
| Project Style Name | 东方神明抽卡学院漫剧 |
| Core Format | 2D manhua |
| Overall Density | medium |
| Realism Level | semi-flat |
| Reference Warning | 不要跑成 glossy 乙游立绘、不要跑成韩系写真脸、不要跑成高饱和萌系校园番、不要跑成重写实电影质感 |

## Line and Render Rules

| Category | Rule |
| --- | --- |
| Line Quality | hard-clean with selective weight change |
| Shadow Depth | 2-step cel shade with restrained rim light |
| Skin Finish | matte with slight warm highlight |
| Hair Finish | grouped locks first, detail strands second |
| Fabric Finish | medium folds, readable silhouette before texture |
| Metallic Finish | limited bright edges, no mirror chrome |

## Color and Light Rules

| Category | Rule |
| --- | --- |
| Day Palette | 学院灰白、深蓝制服、克制肤色暖调 |
| Night Palette | 深蓝黑夜、城市冷灰、异象反射色作为唯一高饱和来源 |
| Gold Fire Energy Palette | golden_event: 金色天空 + 七彩光柱，偏神圣昭示、nezha_event: 赤红天幕 + 红色光柱，偏压迫与灼烧 |
| Academy Base Palette | 石灰白、冷灰蓝、深金点缀 |
| Contrast Policy | medium-high |
| Highlight Policy | restrained in daily shots, strong only on异象与法器 |

## World Design Rules

| Category | Rule |
| --- | --- |
| School Uniform System | 神风学院制服统一为深色学院装，主角与核心人物在剪裁细节上区分身份，不走潮流校服路线 |
| Architecture Language | 西式学院建筑、雕像与广场装置构成世界主视觉，强调西方神魔统治感 |
| Prop Language | 抽卡池、卡片、法器都要有强识别轮廓，卡片与神像系统要明显区分东西方阵营 |
| Vfx Split Rules | 日间异象偏金色圣示，夜间异象偏赤红压迫，避免所有特效混成同一类金闪闪 |
| East Vs West Visual Contrast | 西方神魔体系偏冷灰石雕与规则秩序，东方神明降临偏高纯度能量和强气场轮廓 |

## Camera and Composition Rules

| Category | Rule |
| --- | --- |
| Default Framing | 先中景和可读全景，确保抽卡池、人群、主角站位稳定 |
| Dialogue Coverage | 多人对白优先拆成双人或单人反应，不直接长时间群像口型 |
| Reveal Shots | 神明与异象 reveal 先锁定静帧，再决定是否做低角度英雄机位 |
| Vfx Hero Shots | 特效英雄镜头优先 scene plate + effect overlay，不让人物脸承担全部特效压力 |
| Crowd Policy | 群演作为软背景模板复用，核心人物与群演层分开规划 |

## Failure Boundaries

- 不要把主角定稿做成过重逆光海报脸，否则后续 SD2 引用会把光影当身份
- 不要让金色异象和红色异象共用同一套颜色逻辑
- 不要在一个镜头里同时要求多人对白、强特效、长机位运动
- 不要把辅助 continuity 卡直接当成正片首帧构图
