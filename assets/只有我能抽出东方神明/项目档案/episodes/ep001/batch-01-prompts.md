# EP001 Batch 01 Prompts

这份文件是执行用速查表。

canonical 仍以以下 YAML 为准：

- `series/character-asset-prompt-pack.yaml`
- `series/scene-asset-prompt-pack.yaml`
- `series/prop-vfx-asset-prompt-pack.yaml`

## 1. 孟江 Face Draft

目标输出：

- `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/mj-face-draft-v001.png`

Midjourney:

```text
one East Asian academy boy, 18 years old, slender face, sharp narrow eyes, straight nose bridge, restrained expression, black short hair with slightly messy forehead strands, dark academy uniform collar visible, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, matte skin, grouped hair locks, subtle sacred pressure, not idol-like, not cute anime, not photoreal --ar 3:4 --v 7 --raw
```

## 2. 孟江 Full Body Master

前置：

- 使用上一步的 face draft 作为 `--oref`

目标输出：

- `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/mj-full-body-master-v001.png`

Midjourney:

```text
one East Asian academy boy, 18 years old, same face and same hairstyle as the selected reference, restrained and tense protagonist, tall slim build, clean shoulder line, dark western-magic academy uniform with structured collar and minimal crest detail, straight standing pose, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, matte fabric, slight ancient-gold accent only, not ancient armor, not glossy game poster --ar 9:16 --v 7 --raw --oref [MENGJIANG_FACE_DRAFT] --ow 250
```

Banana Pro:

```text
保留孟江的脸、发型、年龄感、身材比例和站姿不变，只统一这套男式学院制服的领口、门襟、袖口和下装结构，使其符合当前项目的同一学院体系。不要改成古风战甲，不要变成乙游立绘，不要改变画风。
```

建议修正后输出：

- `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/banana-uniform-fix-v001.png`

## 3. 抽卡池装置 Master

目标输出：

- `assets/只有我能抽出东方神明/道具/PROP_DRAW_POOL_DEVICE/mj-master-3q-view-v001.png`

Midjourney:

```text
one ritual draw pool device, carved stone body with restrained dark metal inlays, central card slot, clear press button platform, circular sacred machine silhouette, altar plus machine feeling, readable 3/4 hero view, clean background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not sci-fi console, not fountain, not gacha capsule toy --ar 1:1 --v 7 --raw
```

Banana Pro:

```text
保留这个抽卡池装置的主体轮廓、石质结构、卡槽和按钮平台不变，只统一细节，使它既能用于学院操场版本也能用于公共抽卡池版本。不要改成纯科技设备，不要改变正面识别结构。
```

建议修正后输出：

- `assets/只有我能抽出东方神明/道具/PROP_DRAW_POOL_DEVICE/banana-unified-master-v001.png`

## 4. 神风学院操场 Scene Master

目标输出：

- `assets/只有我能抽出东方神明/场景/LOC_ACADEMY_PLAYGROUND_DAY/mj-scene-master-day-v001.png`

Midjourney:

```text
Shenfeng Academy playground, wide academy plaza used for ritual card drawing, academy main building in background, central stone draw pool device in the middle of the field, rows of western god and demon statues along the axis, track edge lines and viewing stand readable, bright daylight, clear sky, crowd-ready open space, gothic academy architecture, clean comic linework, 2-step cel shading, 2D Chinese manhua still, readable wide composition, not modern high school, not shopping mall, not sci-fi campus --ar 16:9 --v 7 --raw
```

Banana Pro:

```text
保留操场、抽卡池、学院主体建筑、雕像轴线和白天光照不变，只清理画面里不稳定的杂乱人群或错误建筑，使这个场景能作为后续多人镜头母图。保持透视、地面高度和场景布局不变。
```

建议修正后输出：

- `assets/只有我能抽出东方神明/场景/LOC_ACADEMY_PLAYGROUND_DAY/banana-crowd-ready-v001.png`

反打种子：

```text
same Shenfeng Academy playground, reverse-side view of the same ritual space, preserve academy main building relationship, preserve central draw pool position, preserve statue-lined axis, preserve field markings and viewing stand logic, same daylight mood, readable shot coverage for character reverse shots, clean comic linework, 2-step cel shading, 2D Chinese manhua still --ar 16:9 --v 7 --raw --oref [ACADEMY_PLAYGROUND_MASTER] --ow 200
```

## 5. 公共抽卡池 Night Master

目标输出：

- `assets/只有我能抽出东方神明/场景/LOC_PUBLIC_DRAW_POOL_NIGHT/mj-scene-master-night-v001.png`

Midjourney:

```text
public draw pool at night, ritual plaza in the city, central circular stone draw pool device, carved ground patterns, card slot and button platform readable, distant city skyline behind, dark blue-black night base with crimson anomaly reflection on the ground, empty single-character-ready space, sacred mythic mood, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not wasteland, not ruin, not cyberpunk neon city --ar 16:9 --v 7 --raw
```

Banana Pro:

```text
保留公共抽卡池、城市天际线、地面红光反射和夜景布局不变，只清理不稳定的灯光、错误建筑和多余人物，使其成为后续哪吒异象叠加的稳定 plate。不要改变空间结构和视角。
```

建议修正后输出：

- `assets/只有我能抽出东方神明/场景/LOC_PUBLIC_DRAW_POOL_NIGHT/banana-anomaly-plate-v001.png`

反打种子：

```text
same public draw pool night plaza, reverse-side view of the same space, preserve central draw pool scale, preserve skyline placement, preserve carved ground pattern and red light reflection, same night mood, readable reverse-shot coverage, clean comic linework, 2-step cel shading, 2D Chinese manhua still --ar 16:9 --v 7 --raw --oref [PUBLIC_DRAW_POOL_NIGHT_MASTER] --ow 200
```

## Batch 01 完成后立刻解锁的镜头

- `EP001-S02-SH01`
- `EP001-S02-SH03`
- `EP001-S04-SH01`
- `EP001-S04-SH03`
- `EP001-S04-SH07`

## 真正落盘后的更新动作

1. 把图片放进上面对应路径。
2. 在 `episodes/ep001/asset-manifest.yaml` 把对应资产改成 `committed`。
3. 在对应的 `series/*.yaml` 把状态改成 `committed`。
4. 在 `director-queue.yaml` 里把已解锁镜头从 `blocked` 往前推进。
5. 运行：

```bash
python3 scripts/archive_cli.py render assets/只有我能抽出东方神明/项目档案
python3 scripts/archive_cli.py check assets/只有我能抽出东方神明
```
