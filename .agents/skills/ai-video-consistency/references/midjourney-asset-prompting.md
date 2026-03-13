# Midjourney Asset Prompting Notes

This file distills the official Midjourney docs relevant to still-image asset creation for video pipelines.

Official references:
- Prompt Basics: https://docs.midjourney.com/hc/en-us/articles/32023408776205-Prompt-Basics
- Image Prompts: https://docs.midjourney.com/hc/en-us/articles/32099348346765-Image-Prompts
- Style Reference: https://docs.midjourney.com/hc/en-us/articles/32180011136653-Style-Reference
- Omni Reference: https://docs.midjourney.com/hc/en-us/articles/34133518858253-Omni-Reference
- Parameter List: https://docs.midjourney.com/hc/en-us/categories/32038931902605-Parameter-List

## What Matters For Asset Work

For asset creation, Midjourney is strongest when the prompt stays concrete and image-like.

Build prompts from:
- subject
- medium / rendering style
- environment
- lighting
- color
- mood
- composition or camera angle

Do not write long instructional paragraphs when you only need a stable still image.

Official Prompt Basics guidance to preserve:
- short and simple prompts usually work best
- choose precise words instead of vague ones
- use specific numbers when count matters
- describe what you want, not what you do not want
- fewer details give more variety; more details give more control

## Prompt Shape

For asset prompts, prefer:

`[subject] + [style/medium] + [materials/clothing/shape] + [lighting] + [background simplicity or environment] + [composition/angle] + [parameters]`

Example skeleton:

`young academy boy, stylized fantasy anime illustration, black short hair, white-and-black school uniform with gold trim, matte fabric, calm determined expression, soft daylight, simple background, medium full body, front view --ar 2:3`

Think in the official seven prompt lenses:
- Subject
- Medium
- Environment
- Lighting
- Color
- Mood
- Composition

Do not force all seven into every prompt; include the ones that matter for the asset.

## Character Asset Guidance

- Keep the first character master prompt simple.
- Avoid cinematic lighting on the master if the image will be reused across many later edits.
- Explicitly describe the features that must stay fixed: hair shape, face shape, clothing silhouette, materials, signature accessories.
- Use a simple background for reusable masters.
- When count matters, specify it directly, for example `one boy`, `three students`, `a pair of wings`.
- Prefer direct visual nouns over abstract instructions.

## Scene Asset Guidance

- For recurring locations, optimize for readable geography rather than beauty-first composition.
- Name the recurring anchors directly in the prompt.
- Use wide aspect ratios for master shots.
- If the user has a layout sketch, use image prompting instead of trying to force the layout through text alone.
- If the scene needs a crowd, specify the scale clearly, for example `six students in foreground` rather than `students everywhere`.

## Image Prompts

Use image prompts when:
- the user has a rough layout sketch
- the user has an approved earlier scene master
- the user needs to preserve prop placement or scene geography

Important behavior:
- image prompts influence composition and visual direction
- they do not act like exact hard constraints
- for layout-sensitive assets, keep the text prompt aligned with the image prompt instead of fighting it
- include in text everything that must appear in the final image, instead of writing “change this image into...”
- crop the source image close to the target aspect ratio for better results

## Style Reference

Use style reference when:
- the project already has one approved style direction
- you want multiple assets to feel like the same show or same visual family

Do not use style reference as a substitute for locking character identity.

Best-practice behavior from the official docs:
- keep the text prompt simple
- avoid piling on conflicting style words
- use text mainly to describe the new content you want to see

## Omni Reference

Use omni reference when:
- the user already has one approved character image
- identity preservation matters more than free variation
- you are building angle packs or emotion packs

Use it carefully:
- it helps identity consistency
- it can still drift under large pose or wardrobe changes
- do not ask it to solve character identity and scene layout problems at the same time
- always combine it with a clear text prompt
- if the new image style differs from the reference, reinforce the desired style in the text prompt
- if stylize or exp-like settings are high, omni weight may need to be raised
- unless there is a strong reason, keep `--ow` under 400 because official guidance warns higher values can get unpredictable

## Parameters

Use parameters as small control levers, not as the main creative instruction.

Useful defaults for asset work:
- `--ar 2:3` or `--ar 3:4` for character masters
- `--ar 16:9` for scene masters
- `--raw` when interpretation is too stylized or too decorative

Keep parameter choices stable within one asset family.

Formatting rules from the official docs:
- put parameters at the end
- leave a space before the first `--`
- do not put punctuation inside the parameter list
- do not continue prompt text after parameters begin

Practical parameter interpretation:
- `--ar` for shape control
- `--iw` to control how strongly image prompts influence the result
- `--sref` for style family consistency
- `--sw` to control style reference strength
- `--oref` and `--ow` for identity-sensitive character or object insertion
- `--raw` when Midjourney is adding too much of its own stylistic flourish
- `--no` only when exclusion is truly necessary; default prompting should focus on what to include

## Prompt Revision Heuristic

If a Midjourney asset prompt fails:
1. shorten the prompt before making it longer
2. replace vague adjectives with precise nouns or specific visual terms
3. add missing count information
4. add only the most important missing lens from the seven prompt lenses
5. only then change reference type or parameter weights

## Practical Rule For Video Pipelines

Midjourney should usually do one of these jobs:
- character base design
- scene master design
- prop / symbol design
- broad style exploration

Do not ask Midjourney alone to solve:
- multi-shot continuity
- exact shot coverage planning
- precise camera blocking
- multi-character spatial continuity over time

Those are workflow problems and should be handled by `$ai-video-consistency` first, then handed to `$seedance` or other execution tools.
