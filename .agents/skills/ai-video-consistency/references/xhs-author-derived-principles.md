# Xiaohongshu Author-Derived Principles

Use this reference when the user wants creator-derived AI video guidance rather than generic theory.

Source boundary:
- only the creator's own post bodies
- the creator's own top comments
- the creator's own visible reply threads

Do not treat general audience comments as primary evidence.

## Stable Workflow The Creator Repeats

- lock character design first
- lock empty environment shots next
- merge character and environment into storyboard stills
- drive motion after the stills are stable
- finish with voice, edit, grade, and repair

The repeated reasoning:
- hand-built storyboards still matter
- model temporal memory is short
- models do not truly understand 3D space
- once the project includes narrative continuity, multi-camera coverage, or many characters, full automation is not a safe assumption

## Asset-First, Not Prompt-First

The creator consistently treats the problem as an asset workflow:
- character assets first
- scene masters next
- recurring props and VFX next
- shot execution later

This means the fix for drift is usually better assets or better structure, not just longer prompts.

## Big-To-Small Shot Logic

For complex projects, the creator often prefers:
- build one full `Master Shot`
- then cut usable shots out of that parent image

Why:
- keeps relative character placement more stable
- keeps scene geography more stable
- makes multi-camera continuity easier

## Multi-Character and Multi-Camera Caution

Creator-derived warnings:
- wide shots with many small characters are fragile
- large angle changes drift easily
- dense scenes do not reliably one-shot well

Preferred fixes:
- separate character and scene generation whenever possible
- change the environment angle before merging the character
- use region-based or one-character-at-a-time merges for dense scenes
- composite in post when strict placement matters

## Tool View

The creator does not use one tool for everything.

- Midjourney: concepting and base design
- nano-banana / Banana 2: refinement, merge work, material tuning, identity-preserving image changes
- Kontext: controlled edits and consistency support, but not a miracle for large angle jumps or dense multi-subject scenes
- S2 / Sora-like storyboarding: useful as a reference-frame storyteller or shot ideation engine; not a drop-in replacement for a full image-first workflow
- Vidu: stronger action feel, but can lose clean detail
- Jimeng: steadier general execution
- Veo: often more useful for environment or support layers than as the sole actor-performance engine

## SD2 / S2 Continuity Tactics

Source note:
- title: `用 SD2 制作AI动画，痛并快乐着～`
- url: `https://www.xiaohongshu.com/explore/69b7c79b000000001b002e69`
- extracted from the creator's post body on 2026-03-16

The creator frames SD2's main value in three areas:
- keep state continuity more stable across cuts
- stitch space more plausibly when multiple scene angles are provided
- allow multi-modal reference use for more original shot design

### Midpoint-Frame Method

Use one relatively static midpoint frame for a sequence when the user needs both continuity and shot freedom.

The frame should usually carry:
- full scene geography
- character blocking
- pose state
- lighting state

Prompting logic:
- describe what happens before that midpoint near the start of the prompt
- describe what happens after that midpoint near the end of the prompt
- bind different reference elements around the shared midpoint state

This is not a claim that the midpoint must become a literal storyboard shot. It is a continuity anchor.

### Hidden Continuity Card

The creator explicitly notes that the midpoint frame can be a helper card instead of a visible shot.

To reduce the chance that the helper frame leaks into the final clip:
- call it with a very different shot size
- call it with a different camera angle
- call it with a different composition

This makes the model more likely to use the image for continuity guidance instead of copying it as the visible first frame.

### Tail-Frame Planning

When extension is likely, the creator prefers building a dedicated tail frame.

Preferred rule:
- create a planned end-state frame instead of relying on extracted video frames

Why:
- extracted frames tend to be low quality
- regenerating from them can introduce color shift or deformation

### Shot Bridging

For clip-to-clip continuity, the creator suggests feeding the previous-shot state.

Preferred order:
- use a panoramic state frame from the previous shot if available
- otherwise extract a frame only as a fallback
- explicitly restate pose, action, and blocking in the prompt

If the handoff still fails:
- rebuild the linking shot manually
- or insert a cutaway so the edit stops demanding a perfect direct continuation

### Lock Scene, Not Person

When the character is already in continuous motion, the creator warns against over-constraining later shots with literal first/last character frames.

Preferred pattern:
- reference the scene or background for the next shot
- describe framing, angle, and shot size for the new shot
- explicitly tell the model to continue the previous shot's character action when needed

This keeps motion more fluid when the scene changes but the action should continue.

### One Image Still Beats Many Words

The creator's conclusion remains asset-first:
- precise continuity still benefits from image anchors
- text alone does not replace visual structure
- multi-reference image-driven expansion stays more reliable than pure free prompting

## Motion Control View

The creator's practical rule:
- simple motion can come from prompts
- complicated motion needs structure

Common structural methods mentioned:
- skeletal transfer
- multi-frame interpolation / keyframe planning
- line-art or ordered action references

The repeated implication:
- multi-character action and precise beats usually need keyframes, references, layers, or post fixes

## Lip-Sync View

This is one of the creator's clearest repeated positions:
- stylized 2D lip-sync is still weak
- face detection and local redraw often break the shot
- exact phoneme sync should not be treated as the default production target

Preferred workflow:
- lock audio early
- design shot duration around dialogue timing
- prioritize open/close mouth rhythm and emotional timing
- fix the rest with edit timing or manual work

## Post Is Core, Not Cleanup

The creator consistently treats post as part of the main workflow:
- Topaz for chosen finals
- AE or equivalent for compositing, reflection fixes, layer repair, and cleanup
- editor for pacing and sound

The implied rule:
- AI generation speeds the pipeline up
- it does not eliminate traditional post tools or human judgment

## Repeat Warnings

- do not make the character master too cinematic in lighting if you need it as a reusable long-term reference
- do not distribute equal responsibility across many models in one project
- test difficult shots early before scaling
- treat “one frame is salvageable” as enough reason to extract and continue in another workflow

## How To Apply This Reference

When the user wants creator-derived guidance, prefer outputs like:
- `Creator Workflow Summary`
- `Creator Tool Routing`
- `Creator Pitfalls`
- `Project Adaptation`

Adapt the creator's principles to the user's target style, for example:
- 2D manhua
- stylized 3D
- semi-realistic CG

Do not pretend the creator's exact tool mix is universal; preserve the deeper production logic instead.
