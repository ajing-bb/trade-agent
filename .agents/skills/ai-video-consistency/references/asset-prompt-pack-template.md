# Asset Prompt Pack Template

Use this template when the user needs still-image prompts for asset creation before video generation.

Default target: Midjourney-style asset prompting. If the user names another image model, adapt the same asset pack but swap syntax and parameters.

## Midjourney Prompt Rules

When the target is Midjourney, shape each asset prompt with these defaults:
- keep it short and image-like
- lead with the subject
- add only the visual details that matter for consistency
- use specific counts when number matters
- describe what should appear instead of listing many negatives
- place all parameters at the end

Preferred order:

`subject + medium/style + identity/material details + environment/background + lighting/color/mood + composition/angle + parameters`

## Output Sections

Produce these sections when the user is building a project:

1. `Character Asset Prompts`
2. `Scene Asset Prompts`
3. `Prop / VFX Asset Prompts`
4. `Repair / Merge Prompts`

## Character Asset Prompts

Use one row per character asset need.

| Asset | Purpose | Prompt | Reference Strategy | Parameters | Notes |
| --- | --- | --- | --- | --- | --- |
| Hero final look | Stable base design | `[one character], [medium/style], [face + hair anchors], [clothing silhouette], [material], [simple background], [soft stable lighting], [front or 3/4 composition]` | use style reference or omni reference only if the user already has approved refs | `--ar 2:3` or `--ar 3:4`, optionally `--raw` | keep background simple; avoid cinematic lighting if this is the long-term master |
| Angle pack | Side / 3/4 / low angle / high angle | same character description + explicit angle + same wardrobe + same material language + same background simplicity | prefer omni reference for identity-sensitive character packs | aspect ratio by shot use; keep parameter family stable | only make angles the project actually needs |
| Emotion pack | Emotion variants | same identity lock + one emotion + one camera distance + same style words | use same style ref as base | keep params stable across variants | change expression, not identity |

## Scene Asset Prompts

| Asset | Purpose | Prompt | Reference Strategy | Parameters | Notes |
| --- | --- | --- | --- | --- | --- |
| Master shot | Parent image for many shots | `[location], [clear spatial layout], [major anchors], [time/weather], [project style], [readable wide composition]` | use image prompt if there is a layout sketch | usually `--ar 16:9` or project frame | prioritize readable geography over dramatic flourish |
| Angle seed | Large camera change anchor | same scene + explicit angle + preserved anchors + same key props | use scene master as image prompt if available | match target shot ratio; use `--iw` only when needed | create only when free prompting would drift |
| Reverse side | Dialogue or coverage | opposite side of same location + same anchors from new direction + same mood | use scene master or rough layout sketch | target dialogue ratio | keeps reverse shots believable |

## Prop / VFX Asset Prompts

| Asset | Purpose | Prompt | Reference Strategy | Parameters | Notes |
| --- | --- | --- | --- | --- | --- |
| Hero prop | Recurring item | `[single prop], [material], [shape], [ornament], [readable front or 3/4 view], [plain background]` | use style ref if it must match the project | simple aspect ratio | keep silhouette obvious |
| Card / symbol | Repeating system artifact | `[single card or sigil], [graphic motif], [energy feel], [front-facing design], [clean background]` | none unless the project already has a system bible | simple ratio | avoid clutter |
| Signature VFX frame | Key look dev | `[effect], [color logic], [energy texture], [clear context], [readable silhouette]` | use project refs if effect must match world design | shot-appropriate ratio | define the motif before animation |

## Repair / Merge Prompts

Use these when the user already has assets and needs targeted still-image fixes before video.

| Situation | Prompt Pattern | Notes |
| --- | --- | --- |
| Put character into scene | `place [character] into [scene], preserve [scene anchors], match scale, perspective, and lighting` | use when character and scene are already approved separately |
| Fix angle drift | `same location from [angle], preserve [anchors], preserve [prop positions], preserve [style]` | use with an existing scene image |
| Fix material / identity | `same character, preserve face / hair / costume / silhouette, refine [problem area]` | list what must not drift |
| Fix prop placement | `keep [scene], add [prop] at [location], maintain scale and contact with surface` | useful before video generation |

## Parameter Guidance

Use parameters conservatively and keep them stable across a family of assets.

Common defaults:
- character master: `--ar 2:3` or `--ar 3:4`
- scene master: `--ar 16:9`
- `--raw` when the model is over-stylizing and you need more literal interpretation
- style reference / omni reference only after one asset is already approved

When using Midjourney references:
- `--iw` only when image prompt strength needs explicit control
- `--sref` and `--sw` for show-level style consistency
- `--oref` and `--ow` for identity-sensitive assets such as recurring characters or hero props

Do not vary parameters wildly inside one asset family unless the user is intentionally exploring style branches.
