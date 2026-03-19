# MJ V7 Prompt Modules

Curated prompt modules for `Midjourney V7` asset generation in this repo.

Use these modules to strengthen a prompt after the asset identity is already clear.

Do not treat them as mandatory. Pick only the blocks that help the current asset.

## What This Reference Adds

This file fills the gap between:

- `base prompt structure`
- `asset workflow discipline`
- `practical MJ wording for color, finish, and parameter tuning`

It is especially useful when a user shares social-media prompt cheat sheets and asks whether those ideas should be absorbed into this skill.

## V7-Safe Parameter Quick Map

Prefer these for current work:

- `--v 7`
- `--raw`
- `--q 1|2|4`
- `--s 0-1000`
- `--c 0-100`
- `--iw 0-3`
- `--oref [url] --ow [1-1000]`
- `--sref [url or code] --sw [0-1000]`
- `--tile`
- `--no [element]`
- `--draft`

Compatibility reminders:

- `--q 4` is not compatible with `--oref`
- `--draft` is not compatible with `--oref`
- `--oref` is V7-only
- `--tile` is for seamless tiles and usually should not be upscaled
- `--cref` belongs to older V6 / `Niji 6` character-reference workflows

Treat these as `legacy` unless the user explicitly wants an older model:

- `--hd`
- `--test`
- `--testp`
- `--creative`
- `--upbeta`

## Enhancement Modules By Asset Type

### Character Asset Safe Enhancers

Use for face drafts, full-body masters, turnarounds, expression sheets, and angle packs:

- `clean linework`
- `soft cel shading`
- `controlled palette`
- `readable silhouette`
- `crisp facial features`
- `refined fabric folds`
- `precise costume seams`
- `high resolution`
- `detailed but clean`

Avoid or heavily limit these on sheet-generation prompts:

- `photorealistic`
- `35mm`
- `50mm`
- `HDR`
- `leica lens`
- `architectural visualisation`
- `Corona Render`
- `Maxon Cinema 4D`

Reason:

Those words can push the output toward realism, lens distortion, or environment mood when the real task is identity stability and view correctness.

### Scene Master Enhancers

Use more freely for recurring locations and mood-rich environment bases:

- `high resolution`
- `intricate details`
- `cinematic lighting`
- `detailed environment textures`
- `atmospheric depth`
- `readable foreground midground background`
- `architectural detail`
- `scene design`

Use only when the user actually wants a photographic or cinematic base:

- `35mm lens`
- `50mm lens`
- `cinematic`
- `photographic`

### Prop And VFX Enhancers

Good fits:

- `readable silhouette`
- `material contrast`
- `high detail surface`
- `glow falloff`
- `energy filaments`
- `sharp edge highlights`
- `layered emissive color`
- `clean negative space`

## Curated Color Vocabulary

Use color words as interchangeable modules, not as giant lists.

### Green Family

Useful for uniforms, sci-fi screens, magical anomalies, botanical scenes:

- `jade green`
- `emerald green`
- `viridian`
- `olive green`
- `tea green`
- `mint green`
- `apple green`
- `dark green`

### Red Family

Useful for alerts, danger motifs, seals, fire VFX, royal fabrics:

- `ruby red`
- `carmine rose`
- `coral`
- `hibiscus red`
- `dark red`
- `deep red`
- `light red`

### White / Black Family

Useful for uniforms, minimal interiors, ceremonial props, monochrome cards:

- `cream white`
- `ivory`
- `off-white`
- `pearl white`
- `silver white`
- `blush white`
- `coal black`
- `carbon black`
- `brown black`
- `pitch-black`

## Prompt Assembly Rule

Build a stronger MJ prompt with this shape:

```text
[subject identity], [core visual anchors], [outfit or environment anchors], [output type], [optional color block], [optional detail / lighting block] --ar [ratio] --v 7 --raw
```

Do not dump every enhancement word into one prompt.

Preferred cap:

- `1 color block`
- `1 detail block`
- `1 lighting or camera block`

## Ready-Made Suffix Blocks

### Character Base Suffix

```text
controlled palette, high resolution, clean linework, soft cel shading, readable silhouette --v 7 --raw
```

### Character Sheet Suffix

```text
clean linework, soft cel shading, detailed but clean, precise costume seams, plain white background --v 7 --raw
```

### Scene Master Suffix

```text
high resolution, intricate details, cinematic lighting, atmospheric depth, readable foreground midground background --v 7 --raw
```

### Prop Or VFX Suffix

```text
high detail surface, readable silhouette, sharp edge highlights, layered emissive color --v 7 --raw
```

## Parameter Intent Cheatsheet

Use parameters based on intent:

- `Need stronger literal adherence`: lower `--s`
- `Need more artistic push`: raise `--s`
- `Need more variety`: raise `--c`
- `Need faster cheap exploration`: add `--draft`
- `Need tighter identity carry in V7`: add `--oref` and tune `--ow`
- `Need style consistency across assets`: add `--sref` and tune `--sw`
- `Need seamless repeat`: add `--tile`
- `Need to explicitly remove clutter`: add `--no`

Do not combine:

- `--draft` with `--oref`
- `--q 4` with `--oref`

## Repo-Oriented Rule

When writing prompts for this repository:

- keep `identity words` stable across repeated asset generations
- keep `color modules` deliberate and reusable across the same character or world system
- use `scene-only camera jargon` sparingly
- prefer reusable suffix blocks over one-off prompt chaos
