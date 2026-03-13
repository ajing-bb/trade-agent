# Calibration Pack Template

Use this template after script breakdown and before asset or video generation.

Purpose:
- turn raw script language into model-friendly structured prompt language
- separate scene, shot, and character calibration so the project is easier to batch and debug

## Output Shape

- `Scene Calibration Pack`
- `Shot Calibration Pack`
- `Character Calibration Pack`

## Scene Calibration Pack

| Scene ID | Environment Upgrade | Lighting Upgrade | Atmosphere Upgrade | Material / Texture Notes | Prompt Notes |
| --- | --- | --- | --- | --- | --- |
| S01 | | | | | |

Use this to enrich:
- architecture
- terrain
- weather
- time-of-day
- mood
- recurring props in the environment

## Shot Calibration Pack

| Shot ID | Framing | Angle | Movement | Composition Goal | Edit Intent | Prompt Notes |
| --- | --- | --- | --- | --- | --- | --- |
| SH01 | wide / medium / close | eye-level / low / high | static / push / pan / orbit | | | |

Use this to translate vague script language into:
- lens logic
- camera distance
- movement control
- transition intent

## Character Calibration Pack

| Character | Look Anchors | Costume Anchors | Expression Target | Action Behavior | Prompt Notes |
| --- | --- | --- | --- | --- | --- |
| | | | | | |

Use this to enrich:
- hair silhouette
- face anchors
- clothing logic
- motion style
- emotional pose

## Rules

- Keep scene calibration reusable across multiple shots in the same location.
- Keep character calibration reusable across multiple scenes.
- Keep shot calibration specific to the actual beat, not generic.
- Do not mix calibration and final execution prompt into one giant paragraph.
