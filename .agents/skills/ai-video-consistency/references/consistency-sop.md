# AI Video Consistency SOP

Use this reference when the user needs the full workflow, not just a prompt.

## Goal

Preserve:
- character identity
- scene identity
- camera continuity
- visual style continuity
- repairability in post

## Core Rule

Do not let one model solve character design, environment design, camera changes, action control, and long-shot continuity at the same time.

## Production Order

1. Lock the character bible.
   - Make a stable hero image first.
   - Add 2 to 4 supporting angles only after the face, body ratio, costume, and material finish are stable.
   - For special shots, create those angles up front instead of hoping the video model will infer them.

2. Lock the style bible.
   - Keep one shared style direction across the whole project.
   - Keep color palette, lighting bias, material language, and rendering feel stable.
   - Do not change aesthetic direction per shot.

3. Lock the scene bible.
   - Build one wide, readable master scene image for each major location.
   - Keep spatial anchors consistent: doors, windows, roads, statues, tables, vehicles, signs, moon, etc.
   - Reuse these anchors when planning later shots.

4. Lock props and signature effects.
   - Define cards, pools, wings, halos, weapons, VFX motifs, and other recurring symbols before dynamic generation.
   - Use the same asset family across episodes.

5. Create the shot plan.
   - Decide which shots come from a `Master Shot`.
   - Decide which shots need separate character/background generation.
   - Decide which shots need layered compositing.
   - Decide where first/last-frame control is necessary.

6. Generate keyframes before video.
   - Validate face, pose, scale, light, and spatial logic on still frames first.
   - Only move to video once the keyframe passes.

## Character Consistency

- Separate character generation from scene generation whenever possible.
- Reuse one approved design instead of regenerating “similar” characters per shot.
- Store a small angle pack for each important character.
- For multi-character scenes, place characters one by one or by region when needed.
- If a character keeps drifting, reduce scene complexity instead of adding more prompt text.

## Scene Consistency

- Use one location master image as the parent of many shots.
- Prefer “big to small” planning: first a master scene, then crop or reinterpret into shot-specific frames.
- If the user needs large camera changes, generate the angle seed first, then merge the character into that angle.
- Do not ask the video model to invent a whole room layout repeatedly.

## Camera Consistency

- Small camera changes can use image editing or controlled video generation.
- Large angle changes should come from prebuilt angle seeds, not free-form prompting.
- Reverse shots work better when each side of the space is explicitly designed.
- Use arrows, boxes, or layout sketches when the image editor supports image-conditioned control.

## Multi-Character Consistency

- Assume wide shots are the hardest place to preserve face and identity.
- Use regional generation or compositing for crowd-heavy frames.
- Keep 6 to 8 reusable student/background templates instead of inventing dozens of unique extras.
- For dense scenes, prioritize the lead character and critical interactions; let nonessential extras be softer.

## Action Consistency

- Use plain prompts only for simple actions.
- Use pose-sequence, multi-frame, motion-reference, or layered planning for complex actions.
- For complex multi-character beats, split action from camera complexity whenever possible.
- If action timing matters, write a timeline, but do not trust the model to obey exact seconds without structure.

## Lip-Sync and Dialogue

- Treat lip-sync as optional, not default, for stylized animation.
- Prioritize dialogue duration, emotional timing, and open/close mouth beats over perfect phoneme sync.
- Generate or lock the audio early so shot durations can be planned around it.

## Post Strategy

- Upscale only the final chosen clips, not everything.
- Use post tools to unify color, contrast, noise, motion feel, and reflections.
- Fix compositing seams in post instead of forcing the generator to solve every lighting edge case.

## Minimum Deliverables For Any Project

- Character lock list
- Scene lock list
- Props and VFX lock list
- Shot list
- Risk list
- Tool routing notes

## Risk Heuristics

High risk:
- many characters in wide shot
- major camera angle changes
- stylized lip-sync
- dense VFX plus dialogue
- layered foreground/background motion

Medium risk:
- two-character dialogue
- repeated environment from multiple angles
- hero prop close-ups

Lower risk:
- single character medium shot
- simple walk, turn, react
- static environment inserts
