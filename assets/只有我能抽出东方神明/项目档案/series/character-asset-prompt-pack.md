# Character Asset Prompt Pack

> Generated from `character-asset-prompt-pack.yaml`. Do not edit this Markdown manually.

## Rules

- `midjourney_role`: base_generation_only
- `banana_role`: derive_turnaround_expression_angle_and_repair
- `canonical_note`: generated_from_character_bible
- `character_pipeline`: face_draft_then_full_body_then_banana_derived_pack
- `shared_manhua_style_anchor`: plain light gray background, clean comic linework, 2D Chinese manhua still, semi-flat rendering, 2-step cel shade with restrained rim light, matte fabric, minimal metal details
- `shared_negative_guardrails`: not photoreal, not glossy otome game art, not Korean photo face, not high-saturation moe anime, not ancient costume, not soft dress silhouette

## Scope

- `CHAR_MENGJIANG`
- `CHAR_SITUKUNLUN`
- `CHAR_SITUQINGQING`
- `CHAR_LINQIANQIAN`
- `CHAR_ZHANGHE`
- `CHAR_OLD_PROFESSOR`
- `CHAR_ZHANGQIANG`

## `CHAR_MENGJIANG`｜孟江

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 清瘦但挺拔的学院少年、被压抑很久的隐忍感、爆发时有东方神性压迫感

### Midjourney

#### face_draft

```text
one East Asian 男主, 18 years old, 细长眼型, 直鼻梁, 下颌线清楚, 黑色短发，额前碎发略乱, 深色学院制服，后期可叠加东方神性细节, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, 制服布料哑光，金属配件少量点缀, 清瘦但挺拔的学院少年, 被压抑很久的隐忍感, 爆发时有东方神性压迫感, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian 男主, 18 years old, same face and same hairstyle as the selected reference, 清瘦但挺拔的学院少年, 被压抑很久的隐忍感, 爆发时有东方神性压迫感, 偏瘦修长，肩线利落，站姿克制, 深色学院制服，后期可叠加东方神性细节, 制服布料哑光，金属配件少量点缀, colors 深蓝黑, 白, 暗金, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_MENGJIANG_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留孟江的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的深色学院制服，后期可叠加东方神性细节。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_SITUKUNLUN`｜司徒昆仑

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_SITUKUNLUN`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 中年院长气场、克制威严、面相沉稳

### Midjourney

#### face_draft

```text
one East Asian 校长 / 权威长辈, early 50s, 深眼窝, 眉骨清楚, 法令纹轻微, 深色短发，梳理整齐, 学院高层正装或院长制服, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, 深色厚布料，少量权威金属徽章, 中年院长气场, 克制威严, 面相沉稳, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian 校长 / 权威长辈, early 50s, same face and same hairstyle as the selected reference, 中年院长气场, 克制威严, 面相沉稳, 中年男性，肩背厚实，站姿笔直, 学院高层正装或院长制服, 深色厚布料，少量权威金属徽章, colors 炭黑, 深灰蓝, 暗金, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_SITUKUNLUN_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留司徒昆仑的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的学院高层正装或院长制服。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_SITUQINGQING`｜司徒青青

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_SITUQINGQING`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 学院精英少女、清冷利落、对异象反应敏锐

### Midjourney

#### face_draft

```text
one East Asian female academy elite protagonist, 18 years old, slim elite academy girl, sharp almond-shaped eyes, refined facial features but not sweet, slightly tightened chin, cool observant expression, lips held in a subtle straight line, mouth corners slightly tightened, dark long hair with tidy strands, dark academy uniform, high collar structure, matte fabric, minimal metal details, subtle cloud motif only in the trim and emblem, colors deep navy black, white, muted silver gray, solo character, waist-up portrait, centered composition, plain light gray background, clean comic linework, 2D Chinese manhua still, semi-flat rendering, 2-step cel shade with restrained rim light, not photoreal, not glossy otome game art, not Korean photo face, not high-saturation moe anime, not ancient costume, not soft dress silhouette --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian female academy elite protagonist, 18 years old, same face and same hairstyle as the selected reference, slim academy girl, sharp almond-shaped eyes, refined facial features but not sweet, slightly tightened chin, cool observant expression, dark long hair with tidy strands, upright posture, dark academy uniform, high collar structure, matte fabric, minimal metal details, subtle cloud motif only in the trim and emblem, colors deep navy black, white, muted silver gray, solo character, full body, centered composition, plain light gray background, clean comic linework, 2D Chinese manhua still, semi-flat rendering, 2-step cel shade with restrained rim light, not photoreal, not glossy otome game art, not Korean photo face, not high-saturation moe anime, not ancient costume, not soft dress silhouette --ar 9:16 --v 7 --raw --oref [CHAR_SITUQINGQING_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留司徒青青的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的改良学院制服，精英感更强。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_LINQIANQIAN`｜林倩倩

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_LINQIANQIAN`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 校园美女、外表精致、眼神带轻蔑

### Midjourney

#### face_draft

```text
one East Asian 前女友 / 现实势利对照组, 18 years old, 大眼但不萌, 唇形清晰, 面部轮廓流畅, 长发顺直，打理精致, 学院制服但更贴身精致, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, 服装更利落，饰品可少量增加, 校园美女, 外表精致, 眼神带轻蔑, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian 前女友 / 现实势利对照组, 18 years old, same face and same hairstyle as the selected reference, 校园美女, 外表精致, 眼神带轻蔑, 少女体型，姿态外放, 学院制服但更贴身精致, 服装更利落，饰品可少量增加, colors 深蓝, 白, 冷粉少量点缀, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_LINQIANQIAN_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留林倩倩的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的学院制服但更贴身精致。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_ZHANGHE`｜张贺

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_ZHANGHE`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 高富帅压迫感、学院风云人物、带侵略性

### Midjourney

#### face_draft

```text
one East Asian 校园强势反派, 18 years old, 眉眼上挑, 鼻梁挺, 下颌偏锋利, 深色短发，发型精致, 学院制服强化版，带家族贵气, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, 制服更挺阔，少量硬质配件, 高富帅压迫感, 学院风云人物, 带侵略性, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian 校园强势反派, 18 years old, same face and same hairstyle as the selected reference, 高富帅压迫感, 学院风云人物, 带侵略性, 高挑结实，站姿外扩, 学院制服强化版，带家族贵气, 制服更挺阔，少量硬质配件, colors 黑, 深蓝, 金, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_ZHANGHE_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留张贺的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的学院制服强化版，带家族贵气。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_OLD_PROFESSOR`｜老教授

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_OLD_PROFESSOR`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 年迈学者、仪式主持者、神情夸张

### Midjourney

#### face_draft

```text
one East Asian 抽奖仪式主持者, 18 years old, 老年皱纹, 眼眶深, 胡须或唇周岁月感明显, 稀疏白发或灰白短发, 学院仪式教授袍, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, 布料厚重，边缘旧感, 年迈学者, 仪式主持者, 神情夸张, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian 抽奖仪式主持者, 18 years old, same face and same hairstyle as the selected reference, 年迈学者, 仪式主持者, 神情夸张, 瘦削年长男性, 学院仪式教授袍, 布料厚重，边缘旧感, colors 深灰, 棕灰, 暗金, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_OLD_PROFESSOR_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留老教授的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的学院仪式教授袍。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_ZHANGQIANG`｜张强

### Summary

- `status`: planned
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_ZHANGQIANG`
- `reference_assets`: `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`
- `visual_anchors`: 家族长辈、中年强者、冷硬

### Midjourney

#### face_draft

```text
one East Asian 张家家主 / 父辈强者, early 50s, 眉峰硬, 鼻梁厚重, 法令纹明确, 深色短发，整理严谨, 家族权势感正装或高阶制服, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, 厚重布料，少量硬质配件, 家族长辈, 中年强者, 冷硬, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian 张家家主 / 父辈强者, early 50s, same face and same hairstyle as the selected reference, 家族长辈, 中年强者, 冷硬, 中年偏壮，姿态沉稳, 家族权势感正装或高阶制服, 厚重布料，少量硬质配件, colors 黑, 深灰, 暗红, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shade with restrained rim light, 2D Chinese manhua still, not photoreal --ar 9:16 --v 7 --raw --oref [CHAR_ZHANGQIANG_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留张强的脸、发型、年龄感和身材比例不变，只统一服装系统为当前项目设定中的家族权势感正装或高阶制服。保留人物身份和画风，不要改成通用模板。
```

### Archive Updates

- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `/Users/fayon/workspace/github/pnpm/trade-agent/assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`
