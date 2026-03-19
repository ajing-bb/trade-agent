# Prompt Patterns

Use these as short reusable templates. Replace bracketed fields.

For `Midjourney`, treat each template as:

`base skeleton + optional color block + optional detail block + parameter suffix`

Do not blindly append every enhancement word. Prefer:

- `1 color block`
- `1 detail block`
- `1 lighting or camera block`

## Midjourney Base Prompt Patterns

### Face Draft

```text
one [character type], [age], [face anchors], [expression], [hair anchors], [outfit anchors], plain light gray background, waist-up portrait, clean comic linework, soft cel shading, Chinese webtoon animation still --ar 3:4 --v 7 --raw
```

Optional enhancer block:

```text
[optional color block], controlled palette, high resolution, crisp facial features, detailed but clean
```

### Full-Body Base

```text
one [character type], [age], same face and same hairstyle as the selected reference, [identity anchors], [body build], [outfit anchors], standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, soft cel shading, Chinese webtoon animation still --ar 9:16 --v 7 --raw --oref [reference] --ow [weight]
```

Optional enhancer block:

```text
[optional color block], controlled palette, readable silhouette, refined fabric folds, precise costume seams
```

### Scene Master

```text
[location], [clear spatial layout], [major anchors], [time/weather], [project world style], readable wide composition, clean comic linework, soft cel shading, Chinese webtoon animation still --ar 16:9 --v 7 --raw
```

Optional enhancer block:

```text
[optional color block], high resolution, intricate details, atmospheric depth, readable foreground midground background
```

Optional cinematic block:

```text
cinematic lighting, [35mm lens / 50mm lens]
```

### Reverse-Side Scene View

```text
[same location], reverse-side view of the same space, preserve [major anchors], preserve layout logic, same time and mood, readable shot coverage, clean comic linework, soft cel shading, Chinese webtoon animation still --ar 16:9 --v 7 --raw --oref [reference] --ow [weight]
```

Optional enhancer block:

```text
[optional color block], high resolution, intricate details, atmospheric depth
```

### Prop Sheet

```text
one [prop], [material], [shape], [ornament], readable front or 3/4 view, clean background, clean comic linework, soft cel shading, Chinese webtoon animation still --ar 1:1 --v 7 --raw
```

Optional enhancer block:

```text
[optional color block], high detail surface, material contrast, readable silhouette, sharp edge highlights
```

### VFX Keyframe

```text
[effect], [color logic], [energy texture], [clear context], readable silhouette, clean comic linework, soft cel shading, Chinese webtoon animation still --ar 16:9 --v 7 --raw
```

Optional enhancer block:

```text
[optional color block], layered emissive color, glow falloff, energy filaments, clean negative space
```

### Turnaround Sheet

```text
one [character type], [age], same face and same hairstyle as the selected reference, [outfit anchors], strict character turnaround sheet, exactly three views only, left pure front view, center left-facing pure side view, right pure back view, in the side view the head body and feet all face left, nose points left, shoe tips point left, full body, plain white background, clean comic linework, soft cel shading, Chinese webtoon animation style --ar 16:9 --v 7 --raw --oref [reference] --ow [weight]
```

Optional safe enhancer block:

```text
[optional color block], detailed but clean, precise costume seams
```

Avoid on turnaround sheets:

- `photorealistic`
- `HDR`
- `35mm`
- `50mm`
- `leica lens`

### Expression Sheet

```text
one [character type], [age], same face and same hairstyle as the selected reference, [outfit anchors], expression sheet, [emotion 1], [emotion 2], [emotion 3], [emotion 4], plain white background, clean comic linework, soft cel shading, Chinese webtoon animation style --ar 16:9 --v 7 --raw --oref [reference] --ow [weight]
```

Optional safe enhancer block:

```text
[optional color block], controlled palette, crisp facial features, detailed but clean
```

### Angle Pack

```text
one [character type], [age], same face and same hairstyle as the selected reference, [outfit anchors], full body angle sheet, front view, 3/4 view, side view, slight low angle portrait, plain white background, clean comic linework, soft cel shading, Chinese webtoon animation style --ar 16:9 --v 7 --raw --oref [reference] --ow [weight]
```

Optional safe enhancer block:

```text
[optional color block], readable silhouette, refined fabric folds, detailed but clean
```

## Midjourney Prompt Modules

### Safe Character Color Blocks

Pick one when helpful:

```text
jade green, controlled palette
ruby red, controlled palette
ivory and coal black, controlled palette
```

### Safe Scene Color Blocks

Pick one when helpful:

```text
emerald green accents
deep red warning glow
off-white and carbon black minimal palette
```

### V7 Parameter Suffixes

Use these as practical defaults:

```text
--v 7 --raw
--v 7 --raw --oref [reference] --ow [weight]
--v 7 --raw --s [value] --c [value]
--v 7 --raw --sref [style reference] --sw [weight]
```

Quick intent guide:

- `Need stronger literal adherence`: lower `--s`
- `Need more artistic push`: raise `--s`
- `Need more variety`: raise `--c`
- `Need style consistency`: use `--sref` and `--sw`
- `Need stronger identity carry in V7`: use `--oref` and `--ow`

Legacy parameters to avoid unless explicitly requested:

- `--hd`
- `--test`
- `--testp`
- `--creative`
- `--upbeta`

## Combined Midjourney Examples

### Character Full-Body Example

```text
one academy girl, age 17, same face and same hairstyle as the selected reference, quiet top-student temperament, slim build, dark uniform blazer with silver trim and pleated skirt, standing straight, solo character, full body, centered composition, plain light gray background, clean comic linework, soft cel shading, Chinese webtoon animation still, jade green accents, controlled palette, readable silhouette, refined fabric folds, precise costume seams --ar 9:16 --v 7 --raw --oref [reference] --ow 300
```

### Scene Master Example

```text
abandoned observatory classroom, circular room with cracked skylight, old desks pushed to the edge, central ritual diagram on the floor, rainy dusk, cold academy mystery world, readable wide composition, clean comic linework, soft cel shading, Chinese webtoon animation still, off-white and carbon black minimal palette, high resolution, intricate details, atmospheric depth, readable foreground midground background --ar 16:9 --v 7 --raw
```

### VFX Keyframe Example

```text
unstable portal flare, ruby red and deep red energy logic, layered smoke and electric filaments, opening above a ceremonial seal in a dark room, readable silhouette, clean comic linework, soft cel shading, Chinese webtoon animation still, layered emissive color, glow falloff, energy filaments, clean negative space --ar 16:9 --v 7 --raw
```

## Banana Pro Edit Patterns

Banana Pro prompts should be shorter than the Midjourney base prompts.

### Outfit-System Unification

```text
保留人物的脸、发型、年龄感、身材比例和气质不变，只调整服装为与[reference character]同一学院体系的[gender]制服。统一[collar / trim / cuffs / skirt or trouser language]，不要改变人物身份和画风。
```

### Scene Merge

```text
保留角色的脸、发型、身材和服装不变，只把人物自然放入这个场景。保持场景的布局、透视、地面高度和光照不变，匹配人物比例、接地关系和阴影，不要改变人物身份和画风。
```

### Prop Replacement

```text
保留场景和人物不变，只把[old prop]替换为[new prop]。保持透视、尺度、接触关系和光照一致，不要改变人物身份、构图和画风。
```

### VFX Refinement

```text
保留人物、场景和构图不变，只调整这个特效的颜色、能量形态和边缘轮廓。保持世界观一致，不要改变人物身份、镜头和背景。
```

### Repo Update Contract

Use this alongside a prompt result when the project already uses repository memory.

```text
asset_id: [stable asset id]
target_path: [repo path]
archive_updates:
  - [series or episode file 1]
  - [series or episode file 2]
status_after_commit: committed / planned
```

### Side-View Head And Foot Repair

```text
把这个角色修正为标准角色设定三视图中的[left/right]-facing pure side view。头部、胸腔、骨盆、双脚全部朝[left/right]，鼻尖朝[left/right]，鞋尖朝[left/right]，不要回头，不要3/4角度。保留人物身份、发型、制服、比例和画风不变。
```

### Front-View Repair

```text
把中间角色改成标准pure front view，头身脚全部正对镜头，左右对称站立，双手自然下垂且可见，不要插袋，不要歪头，不要3/4角度。保留人物身份、服装、比例和画风不变。
```

### Remove Extra View

```text
删除重复的side视图，exactly three views only，最终只保留左侧pure front、中间pure side、右侧pure back，重新整理排版，不要增加额外人物、额外角度或额外列。
```

### Extract One Panel

```text
从这张角色设定板中，只提取中间的[front/side/back]视图角色，保留完整全身、发型、制服、比例和原有画风，去掉其余视图和文字，只输出单个角色，白色干净背景，角色居中。
```

### Reintegrate Repaired Panel

```text
将这张修正后的[left/right]-facing pure side view角色，放回原三视图设定板的中间位置。只替换中间视图，front和back不变，保持同一角色、同一比例、同一背景和同一画风，重新整理为标准三视图。
```

## Short Engineering Phrases

Use these exact fragments when needed:

- `exactly three views only`
- `left pure front, center left-facing pure side, right pure back`
- `head body and feet all face left`
- `nose points left`
- `shoe tips point left`
- `do not look back at the camera`
- `do not turn into a generic template`
- `only adjust the head direction`
- `only adjust the clothing system`
- `preserve scale perspective and lighting`
- `same school/world system`
