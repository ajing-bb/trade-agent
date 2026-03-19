# Asset Decision Tree

Use this file when the user gives a rough production request and you need to quickly decide:

- `which asset type this really is`
- `whether it belongs to Midjourney or Banana Pro`
- `which suffix block to attach`
- `which words to avoid`

This is a routing aid, not a replacement for the base templates.

## Step 1: Decide The Tool

Ask this first:

`Is the user asking for a new base image, or an edit to an existing approved image?`

If `new base image`:

- use `Midjourney`

If `edit / fix / unify / replace / merge / extract / reinsert`:

- use `Banana Pro`

Short Chinese rule:

- `从零生成` -> `MJ`
- `基于现图修` -> `Banana`

## Step 2: Decide The Asset Type

### Character Face Draft

Trigger words:

- `头像`
- `脸部定稿`
- `脸型`
- `先锁脸`
- `半身像`

Use:

- `Face Draft`

Default suffix:

```text
controlled palette, high resolution, crisp facial features, detailed but clean --ar 3:4 --v 7 --raw
```

Avoid:

- heavy camera jargon
- architectural language
- environment-heavy lighting words

### Character Full-Body Master

Trigger words:

- `全身`
- `角色立绘`
- `人物定稿`
- `站姿`
- `角色母图`

Use:

- `Full-Body Base`

Default suffix:

```text
controlled palette, readable silhouette, refined fabric folds, precise costume seams --ar 9:16 --v 7 --raw
```

Add when identity matters:

```text
--oref [reference] --ow [weight]
```

Avoid:

- `photorealistic`
- `35mm`
- `50mm`
- `HDR`

### Turnaround Sheet

Trigger words:

- `三视图`
- `正侧背`
- `front side back`
- `转面图`
- `角色设定板`

Use:

- `Turnaround Sheet`

Default suffix:

```text
detailed but clean, precise costume seams --ar 16:9 --v 7 --raw
```

Mandatory engineering block:

- `exactly three views only`
- `left pure front`
- `center left-facing pure side`
- `right pure back`

Hard avoid:

- `photorealistic`
- `cinematic`
- `35mm`
- `50mm`
- `leica lens`
- `HDR`

Reason:

The task is view accuracy, not mood.

### Expression Sheet

Trigger words:

- `表情包`
- `表情设定`
- `喜怒哀乐`
- `表情板`

Use:

- `Expression Sheet`

Default suffix:

```text
controlled palette, crisp facial features, detailed but clean --ar 16:9 --v 7 --raw
```

Avoid:

- cinematic lens language
- scene-heavy atmosphere words

### Angle Pack

Trigger words:

- `多角度`
- `角度包`
- `低机位`
- `3/4`
- `不同视角`

Use:

- `Angle Pack`

Default suffix:

```text
readable silhouette, refined fabric folds, detailed but clean --ar 16:9 --v 7 --raw
```

Avoid:

- environment mood overload

### Scene Master

Trigger words:

- `场景母图`
- `固定场景`
- `教室`
- `房间`
- `街道`
- `世界观场景`

Use:

- `Scene Master`

Default suffix:

```text
high resolution, intricate details, atmospheric depth, readable foreground midground background --ar 16:9 --v 7 --raw
```

Optional richer block:

```text
cinematic lighting, [35mm lens / 50mm lens]
```

Use that richer block only if the user wants:

- `电影感`
- `镜头感`
- `氛围感`
- `写实一点`

### Reverse-Side Scene View

Trigger words:

- `反打场景`
- `反方向`
- `同场景反面`
- `镜头反打`

Use:

- `Reverse-Side Scene View`

Default suffix:

```text
high resolution, intricate details, atmospheric depth --ar 16:9 --v 7 --raw --oref [reference] --ow [weight]
```

### Prop Sheet

Trigger words:

- `道具`
- `武器`
- `卡牌`
- `装置`
- `符号`

Use:

- `Prop Sheet`

Default suffix:

```text
high detail surface, material contrast, readable silhouette, sharp edge highlights --ar 1:1 --v 7 --raw
```

### VFX Keyframe

Trigger words:

- `特效`
- `异象`
- `能量`
- `火焰`
- `传送门`
- `技能效果`

Use:

- `VFX Keyframe`

Default suffix:

```text
layered emissive color, glow falloff, energy filaments, clean negative space --ar 16:9 --v 7 --raw
```

## Step 3: Pick A Color Block

If the user only says `绿色`, do not leave it at `green`.

Prefer a more precise block:

- `jade green`
- `emerald green`
- `viridian`
- `olive green`
- `ruby red`
- `carmine rose`
- `deep red`
- `ivory`
- `off-white`
- `carbon black`

Rule:

- `character` -> restrained palette
- `scene` -> broader palette is acceptable
- `VFX` -> high-contrast palette is acceptable

## Step 4: Pick Parameter Intent

### Exploration Pass

Use when the user says:

- `多试几个`
- `先探索`
- `先看方向`

Suggested suffix:

```text
--v 7 --raw --draft --c 20
```

Do not combine this exploration suffix with:

- `--oref`

### Stable Identity Pass

Use when the user says:

- `按这个角色继续`
- `同一个人`
- `别跑脸`

Suggested suffix:

```text
--v 7 --raw --oref [reference] --ow 300
```

Avoid combining with:

- `--draft`
- `--q 4`

### Style Lock Pass

Use when the user says:

- `统一这个画风`
- `全套保持一种风格`
- `整个项目同风格`

Suggested suffix:

```text
--v 7 --raw --sref [style reference] --sw 300
```

### More Literal Pass

Use when the user says:

- `更贴提示词`
- `别太放飞`
- `按设定来`

Suggested suffix:

```text
--v 7 --raw --s 75
```

### More Expressive Pass

Use when the user says:

- `更有设计感`
- `更艺术一点`
- `再放一点`

Suggested suffix:

```text
--v 7 --raw --s 300
```

## Fast Chinese Routing Table

### User says `给我一个角色三视图 prompt`

Route:

- `Midjourney`
- `Turnaround Sheet`
- add strict view constraints
- do not add camera jargon

### User says `把这张角色改成同一学校制服`

Route:

- `Banana Pro`
- `Outfit-System Unification`
- preserve face, hairstyle, body ratio, identity

### User says `给我一个教室场景母图`

Route:

- `Midjourney`
- `Scene Master`
- may add atmospheric detail

### User says `把角色放进这个教室`

Route:

- `Banana Pro`
- `Scene Merge`
- preserve scene layout and lighting

### User says `做一个传送门特效底图`

Route:

- `Midjourney`
- `VFX Keyframe`
- use emissive and glow language

### User says `中间 side 方向不对，修一下`

Route:

- `Banana Pro`
- `Side-View Head And Foot Repair`
- only adjust direction, keep identity and outfit

## Default Answer Shape

When answering a user with a rough request, prefer:

1. `Tool`
2. `Asset Type`
3. `Midjourney Base Prompt` or `Banana Pro Edit Prompt`
4. `Optional Suffix Block`
5. `Notes`
