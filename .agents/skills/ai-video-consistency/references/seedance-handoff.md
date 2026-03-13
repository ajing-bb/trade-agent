# Seedance Handoff

Use this reference when the project will be executed in `$seedance`.

## What Seedance Can Help With

After the consistency plan exists, `$seedance` is useful for:
- writing first/last-frame prompts
- writing multi-modal reference prompts with `@图片N`, `@视频N`, `@音频N`
- controlled shot execution
- multi-shot grouping and segment planning
- video extension
- video editing prompts
- sound and pacing prompts

## What Seedance Should Not Be Asked To Solve Alone

Do not rely on `$seedance` alone to:
- invent the stable final character design
- invent the full spatial layout of recurring locations
- preserve a dense multi-character world without prebuilt assets
- guarantee consistent special-angle shots without angle references
- rescue poor asset planning with longer prompts

## Handoff Checklist

Before writing Seedance prompts, make sure you already have:
- locked character reference images
- locked scene or master-shot reference images
- fixed props/VFX references
- shot purpose and shot timing
- decision on whether the shot uses plain text, image references, video references, or first/last frames
- decision on whether several shots should remain separate or merge into one Seedance segment

## Routing Rules

- If the user only has a script: use `$ai-video-consistency` first.
- If the user already has character and scene assets and wants prompt writing: use `$seedance`.
- If the user wants a long narrative episode: use `$ai-video-consistency` first, then `$seedance` shot by shot.
- If the user asks how to keep continuity in Seedance: explain the continuity plan first, then write the prompt.

## Suggested Output For A Combined Workflow

1. `Character Assets`
2. `Scene Assets`
3. `Shot Intent`
4. `Seedance Mode`
   - text only
   - image referenced
   - video referenced
   - first/last frame
   - multi-shot grouped segment
   - extend/edit
5. `Seedance Prompt`
6. `Segment Grouping` when several shots will be fused into one longer narrative clip

## Common Mapping

- stable dialogue shot -> image references + clear timing
- large camera transition -> first/last frame or prebuilt angle seed
- effect-heavy reveal -> image reference for identity, prompt for effect timing
- repeated recurring location -> scene master image + shot-specific character reference
- long sequence -> break into short shots; do not push all continuity burden into one long generation
- multi-shot narrative moment -> group only the shots that share tight continuity, stable look, and compatible timing
