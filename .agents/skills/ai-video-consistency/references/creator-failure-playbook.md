# Creator Failure Playbook

Use this reference when the user asks why AI-video shots keep failing, how to avoid common production traps, or how to recover from unstable outputs.

This file keeps the creator-derived diagnosis practical:
- problem
- likely cause
- preferred fix

## 1. Character Drift Across Shots

Problem:
- the face, costume, or silhouette changes from shot to shot

Likely cause:
- the character was never locked as a reusable asset
- each shot is being regenerated from text instead of from an approved design
- too many models are sharing equal responsibility for the same character

Preferred fix:
- lock one approved master character image first
- add only the angles and expressions the project really needs
- keep one primary image-edit path for character maintenance
- treat prompts as support, not as the identity source

## 2. Scene Geography Breaks During Camera Changes

Problem:
- reverse shots do not feel like the same location
- furniture, props, doors, or windows move unpredictably

Likely cause:
- no master shot existed for the location
- large angle changes were requested from free prompting

Preferred fix:
- build one readable master shot per recurring location
- create angle seeds before heavy video generation
- if the character is not merged yet, change the environment angle first and merge later

## 3. Wide Multi-Character Shots Fall Apart

Problem:
- characters shrink, drift, swap identity, or lose clean detail

Likely cause:
- dense wide shots are being asked to do too much in one pass
- important figures occupy too little of the frame

Preferred fix:
- simplify the frame
- place key characters first
- keep extras soft or reusable
- use region edits, layered composites, or one-character-at-a-time merges

## 4. The Shot Looks Cinematic but Becomes Hard To Reuse

Problem:
- a beautiful master frame creates problems later when reused in new angles or scenes

Likely cause:
- the original character master is too dependent on dramatic lighting
- the model starts treating lighting as part of the identity

Preferred fix:
- keep reusable masters cleaner and more neutral
- reserve heavy cinematic light for shot-specific finals
- separate identity anchors from shot mood

## 5. Prompting Fails To Produce Complex Motion

Problem:
- action beats are wrong even when the prompt is very detailed

Likely cause:
- the motion is structurally complex
- the model is being asked to infer timing, pose, and rhythm from text alone

Preferred fix:
- use keyframes, pose references, skeletal transfer, or motion references
- simplify camera movement while solving the action
- break long sequences into shorter controllable shots

## 6. Lip-Sync Looks Wrong

Problem:
- mouth motion is off, patchy, or breaks the face

Likely cause:
- stylized lip-sync is still unstable
- exact phoneme sync is being treated as the default target

Preferred fix:
- lock audio early
- design shot length around dialogue timing
- prioritize open/close rhythm and emotion over exact phoneme accuracy
- use edit timing and manual fixes for the rest

## 7. Mixed Models Make The Episode Feel Incoherent

Problem:
- shots feel like they come from different productions

Likely cause:
- too many models share equal responsibility
- each model brings its own color, material, or motion bias

Preferred fix:
- choose one primary model per stage
- use secondary models only for clear gaps
- unify the final sequence in post instead of letting every shot drift stylistically

## 8. Video Generation Starts Too Early

Problem:
- the team keeps regenerating full shots because still-image planning was weak

Likely cause:
- assets were not locked before motion work began

Preferred fix:
- lock character, scene, prop, and VFX assets first
- test one representative hard shot before scaling
- move to video only after stills are approved

## 9. 2D Manhua Projects Feel Too 3D or Too Real

Problem:
- line quality drifts
- the look becomes plastic or over-rendered

Likely cause:
- the workflow is borrowing too much from semi-real or 3D pipelines

Preferred fix:
- prioritize silhouette, line shape, flat color blocks, and expression packs
- keep backgrounds readable and stable
- use motion sparingly and let editing, push-ins, and VFX layers carry energy

## 10. Stylized 3D or Clay Projects Lose Material Stability

Problem:
- hair, fabric, clay, or miniature materials drift noticeably in motion

Likely cause:
- material behavior was not tested early
- the project relied on text prompts instead of repeated asset reuse

Preferred fix:
- test material-heavy shots early
- keep the material language in the asset stage, not only in shot prompts
- accept that some hero shots will need stronger post repair

## Minimal Output Shape

When the user asks for debugging help, prefer:
- `Failure Summary`
- `Likely Cause`
- `Preferred Fix`
- `Fallback If Still Unstable`
