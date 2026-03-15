# EP001 Asset Manifest

> Generated from `asset-manifest.yaml`. Do not edit this Markdown manually.

## Source Assets

| 类型 | ID | 状态 | 路径 |
| --- | --- | --- | --- |
| 剧本 | `SRC_SCRIPT_DOCX` | committed | `assets/只有我能抽出东方神明/剧本/只有我能抽出东方神明.docx` |
| 角色 | `CHAR_MENGJIANG` | committed | `assets/只有我能抽出东方神明/角色/孟江` |
| 角色 | `CHAR_LIN_QIANQIAN` | committed | `assets/只有我能抽出东方神明/角色/林倩倩` |
| 角色 | `CHAR_ZHANG_HE` | committed | `assets/只有我能抽出东方神明/角色/ 张贺` |
| 角色 | `CHAR_SITU_KUNLUN` | committed | `assets/只有我能抽出东方神明/角色/司徒昆仑` |
| 角色 | `CHAR_SITU_QINGQING` | prompted | `missing` |
| 角色 | `CHAR_OLD_PROFESSOR` | prompted | `missing` |
| 角色 | `CHAR_ZHANG_QIANG` | prompted | `missing` |
| 角色 | `ARCH_STUDENT_GENERIC` | prompted | `missing` |
| 场景 | `LOC_KAMIKAZE_PLAYGROUND_DAY` | prompted | `missing` |
| 场景 | `LOC_HEADMASTER_OFFICE_DAY` | prompted | `missing` |
| 场景 | `LOC_CAFETERIA_DAY` | prompted | `missing` |
| 场景 | `LOC_PUBLIC_CARD_POOL_NIGHT` | prompted | `missing` |
| 场景 | `LOC_CITY_REACTION_MONTAGE` | prompted | `missing` |
| 场景 | `LOC_SENIOR_DORM_WINDOW_NIGHT` | prompted | `missing` |
| 场景 | `LOC_ZHANG_RESIDENCE_NIGHT` | prompted | `missing` |
| 道具 | `PROP_CARD_POOL_SCHOOL` | prompted | `missing` |
| 道具 | `PROP_CARD_POOL_PUBLIC` | prompted | `missing` |
| 道具 | `PROP_POINTS_CARD` | prompted | `missing` |
| 道具 | `CARD_TONGTIAN` | prompted | `missing` |
| 道具 | `CARD_NEZHA` | prompted | `missing` |
| 道具 | `PROP_FENGHUO_WHEELS` | prompted | `missing` |
| 道具 | `PROP_FIRE_TIPPED_SPEAR` | prompted | `missing` |
| 道具 | `PROP_RED_SASH` | prompted | `missing` |
| VFX | `VFX_GOLDEN_SKY` | prompted | `missing` |
| VFX | `VFX_RAINBOW_PILLAR` | prompted | `missing` |
| VFX | `VFX_RED_SKY` | prompted | `missing` |
| VFX | `VFX_NEZHA_DHARMA` | prompted | `missing` |

## Notes

- 新角色资产以 脸部定稿 / 全身 / 三视图 / 表情 / 角度 为最小完整角色包
- 历史已落盘角色暂以 全身 / 三视图 / 表情 / 角度 为现状，不强制回补 脸部定稿
- 场景资产以 scene master + Banana 反打/机位变体 为标准工作流
- 道具与 VFX 资产以 master asset + Banana 派生变体 为标准工作流
- 后续新图落盘后，应先更新本文件，再同步对应 bible
- 回填顺序固定为 asset-manifest -> 对应 series bible -> style-bible（如有全局变化）-> director-queue/continuity-plan（如有关联）
- prompted 表示该资产的 prompt pack 已写入 canonical memory，但图片还未正式落盘
