# Character Asset Prompt Pack

> Generated from `character-asset-prompt-pack.yaml`. Do not edit this Markdown manually.

## Rules

- `midjourney_role`: base_generation_only
- `banana_role`: derive_turnaround_expression_angle_and_repair
- `canonical_note`: first_batch_prompted
- `character_pipeline`: face_draft_then_full_body_then_banana_derived_pack

## Scope

- `CHAR_MENGJIANG`
- `CHAR_SITUKUNLUN`
- `CHAR_SITUQINGQING`

## `CHAR_MENGJIANG`｜孟江

### Summary

- `status`: prompted
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_MENGJIANG`
- `reference_assets`: `assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`full_body_master`、`banana_uniform_fix_if_needed`
- `visual_anchors`: 黑发瘦高男生、细长偏锋利眼型、深色学院制服、克制隐忍但有压住的神性

### Midjourney

#### face_draft

```text
one East Asian academy boy, 18 years old, slender face, sharp narrow eyes, straight nose bridge, restrained expression, black short hair with slightly messy forehead strands, dark academy uniform collar visible, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, matte skin, grouped hair locks, subtle sacred pressure, not idol-like, not cute anime, not photoreal --ar 3:4 --v 7 --raw
```

#### full_body_master

```text
one East Asian academy boy, 18 years old, same face and same hairstyle as the selected reference, restrained and tense protagonist, tall slim build, clean shoulder line, dark western-magic academy uniform with structured collar and minimal crest detail, straight standing pose, solo character, full body, centered composition, plain light gray background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, matte fabric, slight ancient-gold accent only, not ancient armor, not glossy game poster --ar 9:16 --v 7 --raw --oref [MENGJIANG_FACE_DRAFT] --ow 250
```

### Banana Pro

#### uniform_fix

```text
保留孟江的脸、发型、年龄感、身材比例和站姿不变，只统一这套男式学院制服的领口、门襟、袖口和下装结构，使其符合当前项目的同一学院体系。不要改成古风战甲，不要变成乙游立绘，不要改变画风。
```

#### sheet_prep_note

```text
请参考当前人物全身照。后续如果进入三视图或表情包阶段，保留孟江的脸、发型、制服、身材比例和画风不变，再单独派生，不要一次同时修改脸和服装。
```

### Archive Updates

- `assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_SITUKUNLUN`｜司徒昆仑

### Summary

- `status`: prompted
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_SITUKUNLUN`
- `reference_assets`: `assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`half_body_master`
- `visual_anchors`: 中年学院权威、沉稳锐利眼神、深色高层制服、克制威压

### Midjourney

#### face_draft

```text
one East Asian academy authority man, early 50s, sharp steady eyes, clear age lines, strong jawline, dark short hair with slight gray, stern restrained expression, high-ranking academy coat collar visible, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, matte skin, not modern businessman, not fantasy king, not photoreal --ar 3:4 --v 7 --raw
```

#### half_body_master

```text
one East Asian academy authority man, early 50s, same face and same hairstyle as the selected reference, calm but powerful school leader, solid mature build, dark high-ranking academy uniform or long coat, upright posture, half body, centered composition, plain light gray background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, dark bronze and deep blue accents, not suit, not military general --ar 4:5 --v 7 --raw --oref [SITUKUNLUN_FACE_DRAFT] --ow 220
```

### Banana Pro

#### uniform_fix

```text
保留司徒昆仑的脸、发型、年龄感和体态不变，只统一这套学院高层制服或长外套的领口、肩线、门襟和徽记，使其明显高于学生制服层级。不要改成现代西装，不要改成年轻人。
```

### Archive Updates

- `assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`

## `CHAR_SITUQINGQING`｜司徒青青

### Summary

- `status`: prompted
- `target_path`: `assets/只有我能抽出东方神明/角色/CHAR_SITUQINGQING`
- `reference_assets`: `assets/只有我能抽出东方神明/项目档案/series/style-bible.yaml`、`assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `required_outputs`: `face_draft`、`half_body_master`
- `visual_anchors`: 学院精英女学生、利落五官、非甜妹路线、干净制服层级

### Midjourney

#### face_draft

```text
one East Asian elite academy girl, 18 years old, clean sharp eyes, neat features, composed surprised expression, tidy long hair or high ponytail, refined academy collar visible, waist-up portrait, plain light gray background, clean comic linework, 2D Chinese manhua still, matte skin, not cute idol anime, not glossy dating game style --ar 3:4 --v 7 --raw
```

#### half_body_master

```text
one East Asian elite academy girl, 18 years old, same face and same hairstyle as the selected reference, upright refined student posture, higher-tier female academy uniform with clear tailoring and subtle crest detail, half body, centered composition, plain light gray background, clean comic linework, 2-step cel shading, 2D Chinese manhua still, navy white pale-gold accents, not sweet school idol, not modern blazer fashion photo --ar 4:5 --v 7 --raw --oref [SITUQINGQING_FACE_DRAFT] --ow 220
```

### Banana Pro

#### uniform_fix

```text
保留司徒青青的脸、发型、年龄感和身材比例不变，只统一她的学院精英制服结构，使其和司徒昆仑同属一个高阶学院体系，但仍保持学生身份。不要改成甜妹，不要改变画风。
```

### Archive Updates

- `assets/只有我能抽出东方神明/项目档案/episodes/ep001/asset-manifest.yaml`
- `assets/只有我能抽出东方神明/项目档案/series/character-bible.yaml`
- `assets/只有我能抽出东方神明/项目档案/series/character-asset-prompt-pack.yaml`
