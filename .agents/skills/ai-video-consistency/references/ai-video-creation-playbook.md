# AI Video Creation Playbook

Use this reference when the user asks broad questions like “AI 视频怎么做”, “怎么少踩坑”, “工具怎么选”, or wants a concise strategic summary before project breakdown.

This playbook distills the recurring, high-confidence patterns from the Xiaohongshu creator research and folds them into a reusable workflow.

## Core Thesis

The main job is not “full automation”. The main job is preserving:
- character consistency
- scene consistency
- shot logic
- editability in post

Prefer:
- controllability before automation
- consistency before spectacle
- test clips before full production

## Default Production Order

1. Lock the visual direction.
   - Decide whether the project is 2D manhua, stylized 3D, clay, miniature realism, or semi-real CG.
   - Do not mix incompatible styles inside one episode unless that contrast is deliberate.

2. Lock characters.
   - Create one approved hero image first.
   - Then add only the angles and emotions the project actually needs.
   - Keep face anchors, hair silhouette, costume silhouette, material language, and color anchors stable.

3. Lock scenes.
   - Build one readable master shot per recurring location.
   - Keep spatial anchors explicit.
   - Reuse the master shot when planning later coverage.

4. Lock props and VFX.
   - Define recurring cards, pools, statues, wings, weapons, halos, and signature effects before animation.
   - Reuse the same visual family across scenes and episodes.

5. Test representative shots.
   - Test one difficult scene before scaling.
   - Validate look, motion, scene logic, and repairability before building the rest.

6. Generate keyframes before video.
   - Lock stills first.
   - Only move to video after the still frame is approved.

7. Finish with post.
   - Use post to unify color, sharpness, compositing edges, reflections, and pacing.
   - Do not expect the generator to solve every final-pixel problem.

## Tool Routing

Treat tools as stages, not as one-model magic.

- Midjourney: strong for concepting, design exploration, scene masters, and base asset generation.
- Banana / Banana 2 / nano-banana: strong for refinement, material tuning, angle edits, and controlled image changes.
- Kontext: useful for controlled edits, identity-preserving changes, and merge-heavy workflows, but do not force it to solve every large angle jump.
- Seedance: use after the consistency plan exists; good for execution prompts, multimodal references, first/last-frame prompts, extension, and edits.
- Vidu: stronger on expressive action and motion intensity, but may trade away some clean detail.
- Jimeng: often steadier for general animation shots and first/last-frame stability.
- Veo: useful for environment layers, atmospheric motion, and support shots rather than being the only character-performance engine.
- Sora-like storyboarding models: good for cinematic shot ideas and cut-feel, but do not rely on them to rescue weak asset planning.
- MiniMax / 11Labs: audio first when timing matters; 11Labs-class tools often handle subtle emotion better.
- Topaz / AE / editor: still part of the core pipeline, not optional cleanup.

## Shot Planning Rules

- Do not ask one model to solve character design, scene layout, multi-character blocking, camera changes, long continuity, and VFX timing all at once.
- Prefer big-to-small planning: master shot first, coverage second.
- For layout-sensitive scenes, use sketches or image references instead of over-explaining in text.
- Use still-image validation before video generation.
- Break long sequences into short controllable shots.

## Character Consistency Rules

- Generate characters separately from scenes whenever possible.
- Reuse one approved design instead of regenerating “similar” people every time.
- Build angle packs only for needed views.
- For 2D manhua projects, prioritize clean line shape, silhouette, color blocks, and expression packs over realistic texture.
- For 3D or stylized CG, test material drift early because texture instability becomes obvious in motion.

## Scene and Camera Rules

- A recurring location needs a master shot.
- Large camera changes should come from prebuilt angle seeds, not free prompting.
- Reverse shots work better when both sides of the space are designed.
- If a video model can orbit the environment, use it to collect angle seeds, then extract or rebuild the needed frames.
- If the character is not in the scene yet, change the scene angle first and merge the character later.

## Multi-Character Rules

- Crowds and wide shots are the fastest way to lose consistency.
- Use reusable background-character templates instead of inventing every extra.
- For dense frames, place important characters first and let nonessential extras stay soft.
- If positioning matters, composite or region-edit instead of demanding a perfect one-shot generation.
- For many-character scenes, splitting into foreground and background layers is often more stable than generating one flattened frame.

## Motion Rules

- Simple motion: prompt directly.
- Complex motion: use keyframes, motion references, pose sequences, layered builds, or first/last-frame control.
- Do not expect exact second-by-second obedience from timeline text alone.
- When action timing really matters, simplify camera complexity and add more structural control.

## Lip-Sync and Dialogue

- Stylized 2D lip-sync is still weak in many pipelines.
- Prioritize dialogue timing, emotion, and mouth open/close beats over perfect phoneme accuracy.
- Lock or generate the audio early when dialogue timing affects shot length.
- Treat precise lip-sync as a special-case effort, not the default production assumption.

## Post Strategy

- Upscale only selected finals.
- Unify shots in post instead of trying to overfit prompts.
- Fix compositing seams, lighting edges, and reflective interactions in AE or the editor when needed.
- Save heavy cleanup for chosen shots, not for every experiment.

## High-Probability Pitfalls

- Starting with video generation before assets are stable.
- Re-designing the same character in every shot.
- Letting each scene drift into a different style family.
- Doing wide multi-character scenes too early.
- Expecting long-shot continuity without angle seeds or first/last-frame planning.
- Treating prompt length as a substitute for production structure.
- Trusting lip-sync quality too early in stylized animation.

## Minimal Advice To Give Users

When the user asks for a concise summary, compress to:

1. Lock the character.
2. Lock the scene.
3. Lock recurring props and effects.
4. Test one hard scene.
5. Generate stills before motion.
6. Use video models for execution, not for inventing the whole project.
7. Finish the consistency problem in post when generation alone is not enough.

## Recommended Output Shape For Broad Requests

- `Workflow Summary`
- `Tool Routing`
- `Consistency Rules`
- `Common Pitfalls`
- `Next Build Step`
