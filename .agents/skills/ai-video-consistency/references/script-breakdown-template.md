# Script Breakdown Template

Use this template when the user gives a script, outline, episode draft, or scene list and wants structured planning data before prompt writing.

## Output Shape

- `Project Summary`
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

## Scene List

| Scene ID | Time / Location | Purpose | Main Characters | Key Props / VFX | Continuity Risk |
| --- | --- | --- | --- | --- | --- |
| S01 | | | | | |

## Shot List

| Shot ID | Scene ID | Beat | Camera Intent | Dialogue | Emotion | Required Assets | Difficulty |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SH01 | S01 | | | | | | |

## Character Mention Map

| Character | First Scene | Recurring Scenes | Dialogue Density | Asset Priority |
| --- | --- | --- | --- | --- |
| | | | | |

## Dialogue and Emotion Notes

| Shot ID | Speaker | Dialogue Purpose | Emotion | Lip-Sync Sensitivity |
| --- | --- | --- | --- | --- |
| SH01 | | | | low / medium / high |

## Rules

- Normalize repeated location names to one canonical scene label.
- Normalize repeated character names and aliases.
- Assign stable `Scene ID` and `Shot ID` values before creating prompts.
- Keep one row per shot even if several shots will later be grouped into one Seedance segment.
