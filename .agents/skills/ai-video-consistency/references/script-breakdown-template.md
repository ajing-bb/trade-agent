# Script Breakdown Template

Use this template when the user gives a script, outline, episode draft, or scene list and wants structured planning data before prompt writing.

## Output Shape

- `Project Summary`
- `Manual Review Summary`
- `Scene List`
- `Shot List`
- `Character Mention Map`
- `Dialogue and Emotion Notes`

## Project Summary

| Field | Value |
| --- | --- |
| Project Type | short, episode, promo, manhua, stylized CG |
| Target Style | 2D manhua, stylized 3D, semi-real CG, other |
| Primary Theme | |
| Core Continuity Risks | |
| Recommended Production Unit | shot, scene, segment |

## Manual Review Summary

| Scope | Target | Review Flags |
| --- | --- | --- |
| shot | SH01 | high_difficulty, strong_vfx |

## Scene List

| Scene ID | Time / Location | Purpose | Main Characters | Key Props / VFX | Continuity Risk | Review Flags |
| --- | --- | --- | --- | --- | --- | --- |
| S01 | | | | | | location_binding_needed |

## Shot List

| Shot ID | Scene ID | Beat | Camera Intent | Dialogue | Emotion | Required Assets | Difficulty | Review Flags |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SH01 | S01 | | | | | | | high_difficulty |

## Character Mention Map

| Character | First Scene | Recurring Scenes | Dialogue Density | Asset Priority | Review Flags |
| --- | --- | --- | --- | --- | --- |
| | | | | | generic_extra_candidate |

## Dialogue and Emotion Notes

| Shot ID | Speaker | Dialogue Purpose | Emotion | Lip-Sync Sensitivity |
| --- | --- | --- | --- | --- |
| SH01 | | | | low / medium / high |

## Rules

- Normalize repeated location names to one canonical scene label.
- Normalize repeated character names and aliases.
- Assign stable `Scene ID` and `Shot ID` values before creating prompts.
- Keep one row per shot even if several shots will later be grouped into one Seedance segment.
- Add `Review Flags` when a row is heuristic, unresolved, or likely to need manual production cleanup.
