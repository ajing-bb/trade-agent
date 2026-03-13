# Director Queue Template

Use this template when the user wants an orchestration layer for batch generation.

This is the handoff layer where:
- structured shots
- calibrated prompts
- assets
- execution modes
- provider/model routing

all meet in one queue.

## Output Shape

- `Director Queue`
- `Provider / Model Routing`
- `Retry Policy`

## Director Queue

| Shot ID | Scene ID | Purpose | Input Assets | Still Prompt Source | Video Prompt Source | Execution Mode | Provider / Model | First Frame | Last Frame | Status | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SH01 | S01 | | | | | text / image / video / first-last / edit | | | | queued | |

## Provider / Model Routing

| Task Type | Preferred Provider | Preferred Model | Backup | Notes |
| --- | --- | --- | --- | --- |
| character still | | | | |
| scene master | | | | |
| merge edit | | | | |
| execution video | | | | |
| extend / edit | | | | |

## Retry Policy

| Failure Type | Retry Rule | Escalation |
| --- | --- | --- |
| weak still quality | regenerate with same assets | tighten prompt or switch model |
| identity drift | retry with stronger reference control | go back to asset stage |
| camera drift | retry with stronger angle seed | rebuild scene angle first |
| long-shot failure | split into smaller unit | group in post |

## Rules

- One row per planned shot, even if multiple rows later merge into one Seedance segment.
- Keep input asset references explicit.
- Keep still-image generation and video generation as separate columns.
- Always include a fallback path so the queue can be debugged instead of restarted from zero.
