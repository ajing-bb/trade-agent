# EP001 First Production Pack

> 首轮只做最关键的 6 步，目标是先拿到可复用母资产，不追求一口气做完整一集。

## 执行顺序

1. `CHAR_MENGJIANG` face draft
2. `CHAR_MENGJIANG` full body master
3. `PROP_DRAW_POOL_MAIN` master view
4. `LOC_KAMIKAZE_ACADEMY_GROUNDS` scene master
5. `VFX_GOLDEN_SKY_ANOMALY` keyframe
6. `VFX_RAINBOW_LIGHT_PILLAR` keyframe

只有这 6 步稳定后，再继续：
- `LOC_KAMIKAZE_ACADEMY_GROUNDS` reverse seed
- `CARD_TONGTIAN_JIAOZHU`
- `CHAR_SITUKUNLUN`
- `LOC_PRINCIPAL_OFFICE`

## 1. 孟江脸部定稿

输出路径：
`assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/face-draft-v001.png`

Midjourney：

```text
young East Asian male student hero, 18 years old, sharp clean face, calm but stubborn eyes, straight nose bridge, defined jawline, black layered short hair, clean forehead, no accessories, black academy uniform with muted gold trim and white inner shirt, waist-up portrait, plain light gray background, restrained underdog aura, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not photoreal --ar 3:4 --v 7 --raw
```

验收标准：
- 脸不能过于偶像化，必须保留“被压着但不服”的气质。
- 发型必须简洁稳定，后续方便做侧面、表情和动作。
- 制服先只看上半身语言，不追求全身版型。

## 2. 孟江全身定稿

输出路径：
`assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG/full-body-master-v001.png`

Midjourney：

```text
young East Asian male student hero, 18 years old, same face and same hairstyle as the selected reference, lean athletic build, long legs, upright stance, black academy uniform with muted gold trim, white shirt, fitted dark trousers, matte school fabric, restrained metallic trim, solo full body, centered composition, plain light gray background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_MENGJIANG_FACE_DRAFT] --ow 250
```

Banana Pro：

```text
保留孟江的脸、发型、年龄感和身材比例不变，只统一校服结构。上衣为黑色学院制服，细窄暗金包边，白色内衬，长裤利落，整体偏克制的校园异能主角风。不要改成偶像制服，不要加夸张装饰，不要改变人物身份和画风。
```

验收标准：
- 先追求“全身比例稳定”，不要一上来做转面表。
- 站姿要正，方便后面做纯 front / pure side / pure back。
- 校服必须和后续学院体系兼容。

## 3. 抽卡池母资产

输出路径：
`assets/只有我能抽出东方神明/道具/PROP_DRAW_POOL_MAIN/master-view-v001.png`

Midjourney：

```text
ritual draw pool device, circular ceremonial pedestal, central output slot, obvious summon button area, hybrid of modern academy machine and mythic ritual altar, readable silhouette, clean background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not photoreal --ar 1:1 --v 7 --raw
```

Banana Pro：

```text
保留抽卡池主体轮廓不变，只清理结构和细节。强调中央出卡口、按钮区、底座层级和可读性。不要把它改成科幻扭蛋机，也不要改成传统香炉祭坛。
```

验收标准：
- 一眼能看出这是本世界的核心抽卡设施。
- 轮廓必须简洁，方便放进远景、中景和特写。
- 不能过度赛博，也不能过度古风。

## 4. 神风学院操场白天母场景

输出路径：
`assets/只有我能抽出东方神明/场景/LOC_KAMIKAZE_ACADEMY_GROUNDS/scene-master-v001.png`

Midjourney：

```text
academy ceremonial courtyard, central draw pool pedestal in the middle, modern school facade and open sports ground, surrounding western myth statues, crowd ring space for student audience, clear hero lane toward the draw pool, bright daytime, readable wide composition, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not photoreal --ar 16:9 --v 7 --raw
```

Banana Pro：

```text
保留神风学院操场的空间布局、透视、抽卡池位置、雕像分布和白天光照不变，只清理错误结构与不稳定细节，让它成为后续镜头可复用的白天母场景。不要改变画风，不要随意增加建筑。
```

验收标准：
- 中心必须给抽卡池留出英雄位。
- 雕像要形成“西方神魔世界”的说明性背景。
- 不要把操场做成空旷广场；要有学院属性。

## 5. 金色天幕异象

输出路径：
`assets/只有我能抽出东方神明/VFX/VFX_GOLDEN_SKY_ANOMALY/keyframe-v001.png`

Midjourney：

```text
golden sky anomaly, imperial gold cloud layer spreading over a school courtyard, sacred Eastern deity pressure, large-scale sky takeover, readable energy silhouette, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not photoreal --ar 16:9 --v 7 --raw
```

Banana Pro：

```text
保留金色天幕的整体构图不变，只调整金色层次、边缘扩散和压迫感。目标是天空被金色异象接管，但仍然清楚可读，不要变成普通夕阳或金色滤镜。
```

验收标准：
- 必须像“天地变色”，不能只是天更黄一点。
- 金色要有东方神明压迫感，不是西方圣光滤镜。

## 6. 七彩光柱异象

输出路径：
`assets/只有我能抽出东方神明/VFX/VFX_RAINBOW_LIGHT_PILLAR/keyframe-v001.png`

Midjourney：

```text
rainbow summon light pillar descending from the sky onto a ritual draw pool, spectral multi-color core, sacred pressure, clear vertical silhouette, clean comic linework, 2-step cel shading, 2D Chinese manhua still, not photoreal --ar 16:9 --v 7 --raw
```

Banana Pro：

```text
保留七彩光柱垂直贯穿的主体结构不变，只调整颜色层次、核心亮度和边缘清晰度，让它看起来像真正降临的召唤异象，不要散成烟花或舞台灯柱。
```

验收标准：
- 重点是“从天而降的召唤感”。
- 色彩可以丰富，但轮廓必须干净，不要炸得太碎。

## 落盘后怎么回写系统

如果你确认某个资产已经定稿并放进对应目录，执行：

```bash
python3 scripts/archive_cli.py status 'assets/只有我能抽出东方神明' CHAR_MENGJIANG --status committed --path 'assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG'
python3 scripts/archive_cli.py status 'assets/只有我能抽出东方神明' PROP_DRAW_POOL_MAIN --status committed --path 'assets/只有我能抽出东方神明/道具/PROP_DRAW_POOL_MAIN'
python3 scripts/archive_cli.py status 'assets/只有我能抽出东方神明' LOC_KAMIKAZE_ACADEMY_GROUNDS --status committed --path 'assets/只有我能抽出东方神明/场景/LOC_KAMIKAZE_ACADEMY_GROUNDS'
python3 scripts/archive_cli.py status 'assets/只有我能抽出东方神明' VFX_GOLDEN_SKY_ANOMALY --status committed --path 'assets/只有我能抽出东方神明/VFX/VFX_GOLDEN_SKY_ANOMALY'
python3 scripts/archive_cli.py status 'assets/只有我能抽出东方神明' VFX_RAINBOW_LIGHT_PILLAR --status committed --path 'assets/只有我能抽出东方神明/VFX/VFX_RAINBOW_LIGHT_PILLAR'
```

然后重新生成：

```bash
python3 scripts/archive_cli.py sync 'assets/只有我能抽出东方神明' --episode ep001 --batch-id Batch-01
```

这样 `director-queue` 会自动把被这些资产解锁的镜头往前推。
