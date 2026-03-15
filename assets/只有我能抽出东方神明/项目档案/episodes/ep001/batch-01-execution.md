# EP001 Batch 01 Execution

这份 runbook 不是 canonical single source of truth。

canonical 仍然以以下 YAML 为准：

- `series/character-asset-prompt-pack.yaml`
- `series/scene-asset-prompt-pack.yaml`
- `series/prop-vfx-asset-prompt-pack.yaml`
- `episodes/ep001/asset-manifest.yaml`
- `episodes/ep001/director-queue.yaml`
- `episodes/ep001/continuity-plan.yaml`

本文件只用于把当前已写好的 canonical prompt pack 变成实际执行顺序。

## Batch 01 目标

先拿到能解锁首批镜头的基础母图：

1. 孟江 `face draft`
2. 孟江 `full body master`
3. 抽卡池装置 `master`
4. 神风学院操场 `scene master`
5. 公共抽卡池 `scene master`

这五项完成后，可优先推进：

- `EP001-S02-SH01`
- `EP001-S02-SH03`
- `EP001-S04-SH01`
- `EP001-S04-SH03`
- `EP001-S04-SH07`

## Batch 01 执行顺序

| Order | Asset ID | Tool | Prompt Source | Recommended Output |
| --- | --- | --- | --- | --- |
| 1 | `CHAR_MENGJIANG` | Midjourney | `character-asset-prompt-pack.yaml -> face_draft` | `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/mj-face-draft-v001.png` |
| 2 | `CHAR_MENGJIANG` | Midjourney | `character-asset-prompt-pack.yaml -> full_body_master` | `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/mj-full-body-master-v001.png` |
| 3 | `CHAR_MENGJIANG` | Banana Pro | `character-asset-prompt-pack.yaml -> uniform_fix` | `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/banana-uniform-fix-v001.png` |
| 4 | `PROP_DRAW_POOL_DEVICE` | Midjourney | `prop-vfx-asset-prompt-pack.yaml -> master_3q_view` | `assets/只有我能抽出东方神明/道具/PROP_DRAW_POOL_DEVICE/mj-master-3q-view-v001.png` |
| 5 | `PROP_DRAW_POOL_DEVICE` | Banana Pro | `prop-vfx-asset-prompt-pack.yaml -> academy_public_unify` | `assets/只有我能抽出东方神明/道具/PROP_DRAW_POOL_DEVICE/banana-unified-master-v001.png` |
| 6 | `LOC_ACADEMY_PLAYGROUND_DAY` | Midjourney | `scene-asset-prompt-pack.yaml -> scene_master_day` | `assets/只有我能抽出东方神明/场景/LOC_ACADEMY_PLAYGROUND_DAY/mj-scene-master-day-v001.png` |
| 7 | `LOC_ACADEMY_PLAYGROUND_DAY` | Banana Pro | `scene-asset-prompt-pack.yaml -> crowd_ready_cleanup` | `assets/只有我能抽出东方神明/场景/LOC_ACADEMY_PLAYGROUND_DAY/banana-crowd-ready-v001.png` |
| 8 | `LOC_PUBLIC_DRAW_POOL_NIGHT` | Midjourney | `scene-asset-prompt-pack.yaml -> scene_master_night` | `assets/只有我能抽出东方神明/场景/LOC_PUBLIC_DRAW_POOL_NIGHT/mj-scene-master-night-v001.png` |
| 9 | `LOC_PUBLIC_DRAW_POOL_NIGHT` | Banana Pro | `scene-asset-prompt-pack.yaml -> anomaly_plate_cleanup` | `assets/只有我能抽出东方神明/场景/LOC_PUBLIC_DRAW_POOL_NIGHT/banana-anomaly-plate-v001.png` |

## Batch 01 解锁关系

| Asset | Unblocks |
| --- | --- |
| `CHAR_MENGJIANG` face draft | `EP001-S02-SH03`, `EP001-S04-SH07` |
| `CHAR_MENGJIANG` full body master | `EP001-S02-SH01`, `EP001-S04-SH01` |
| `PROP_DRAW_POOL_DEVICE` master | `EP001-S02-SH01`, `EP001-S04-SH01`, `EP001-S04-SH03` |
| `LOC_ACADEMY_PLAYGROUND_DAY` master | `EP001-S02-SH01`, `EP001-S02-SH03` |
| `LOC_PUBLIC_DRAW_POOL_NIGHT` master | `EP001-S04-SH01`, `EP001-S04-SH03`, `EP001-S04-SH07` |

## Batch 02 预备顺序

Batch 01 稳定后再跑这些：

1. `CHAR_SITUKUNLUN`
2. `CHAR_SITUQINGQING`
3. `LOC_HEADMASTER_OFFICE_DAY`
4. `CARD_TONGTIANJIAOZHU`
5. `CARD_NEZHA`
6. `VFX_GOLDEN_SKY_OMEN`
7. `VFX_RAINBOW_DESCENT_PILLAR`
8. `VFX_RED_SKY_FIRE_OMEN`
9. `VFX_RED_ASCENT_PILLAR`
10. `VFX_NEZHA_WEAPON_MANIFEST`

推荐文件名：

- `assets/只有我能抽出东方神明/角色/CHAR_SITUKUNLUN/mj-face-draft-v001.png`
- `assets/只有我能抽出东方神明/角色/CHAR_SITUQINGQING/mj-face-draft-v001.png`
- `assets/只有我能抽出东方神明/场景/LOC_HEADMASTER_OFFICE_DAY/mj-office-master-day-v001.png`
- `assets/只有我能抽出东方神明/道具/CARD_TONGTIANJIAOZHU/mj-master-card-v001.png`
- `assets/只有我能抽出东方神明/道具/CARD_NEZHA/mj-master-card-v001.png`
- `assets/只有我能抽出东方神明/VFX/VFX_GOLDEN_SKY_OMEN/mj-keyframe-v001.png`
- `assets/只有我能抽出东方神明/VFX/VFX_RAINBOW_DESCENT_PILLAR/mj-keyframe-v001.png`
- `assets/只有我能抽出东方神明/VFX/VFX_RED_SKY_FIRE_OMEN/mj-keyframe-v001.png`
- `assets/只有我能抽出东方神明/VFX/VFX_RED_ASCENT_PILLAR/mj-keyframe-v001.png`
- `assets/只有我能抽出东方神明/VFX/VFX_NEZHA_WEAPON_MANIFEST/mj-keyframe-v001.png`

## 每次落盘后的最小更新动作

当某个资产真的保存到仓库后，按这个顺序更新：

1. 在 `episodes/ep001/asset-manifest.yaml` 把对应资产从 `prompted` 改成 `committed`
2. 在对应的 `series/*.yaml` 里把该资产从 `prompted` 改成 `committed`
3. 如果这个资产已经足够解锁某个镜头，就把 `director-queue.yaml` 里的阻塞条件缩小
4. 运行：

```bash
python3 scripts/archive_cli.py render assets/只有我能抽出东方神明/项目档案
python3 scripts/archive_cli.py check assets/只有我能抽出东方神明
```

## 不要跳步

- 不要先做大特效，再去补环境母图。
- 不要在孟江脸没锁的时候就直接做强红光近景。
- 不要把 `金色通天教主异象` 和 `赤红哪吒异象` 混成一套调色。
- 不要把空目录当成已落盘资产；只有真实图片进入仓库后才算 `committed`。
