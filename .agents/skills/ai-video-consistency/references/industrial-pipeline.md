# Industrial Pipeline

Use this reference when the user wants a production-line workflow rather than isolated prompt advice.

This reference adapts the idea of:
- script
- character
- scene
- director
- Seedance

into a reusable planning pipeline for AI video and AI manhua production.

## Core Idea

The pipeline should behave like a chain:
- script output feeds calibration
- calibration feeds asset creation
- asset creation feeds shot execution
- shot execution feeds multi-shot assembly

The goal is not just “better prompts”.
The goal is reducing manual recopying, ambiguity, and repeated setup work between stages.

## Stage 0: Provider and Model Routing

Before creative work starts, define:
- provider pool
- model routing by task
- retry policy
- batch size
- queue unit

Minimum planning outputs:
- `Provider Pool`
- `Task -> Model Mapping`
- `Retry Policy`
- `Concurrency Notes`

Typical mapping:
- image asset generation -> Midjourney or image-first model
- controlled edits and merges -> Banana / Kontext class tools
- execution video -> Seedance or chosen video model
- upscale / composite / repair -> post stack

## Stage 1: Script Structuring

The system should convert long script text into reusable units:
- scene
- shot
- character
- dialogue
- emotion beat
- camera intent

This is the planning backbone.
Without stable IDs and structured units, later batch routing becomes fragile.

Minimum outputs:
- `Script Breakdown`
- `Scene List`
- `Shot List`
- `Character Mention Map`
- `Dialogue Timing Notes`

## Stage 2: Calibration Pack

This is the “AI second pass” that upgrades raw script text into model-friendly structured prompts.

Calibrate separately:
- scene calibration
- shot calibration
- character calibration

Scene calibration enriches:
- environment
- atmosphere
- light
- material cues
- time-of-day

Shot calibration enriches:
- lens logic
- framing
- angle
- movement
- cut intent

Character calibration enriches:
- appearance anchors
- costume anchors
- action behavior
- expression target

Minimum outputs:
- `Scene Calibration Pack`
- `Shot Calibration Pack`
- `Character Calibration Pack`

## Stage 3: Asset Proofing

Before mass generation, build the reusable visual system.

Typical assets:
- character bible
- scene masters
- prop and VFX bible
- angle seeds
- expression pack

This is where the project becomes reusable instead of prompt-fragile.

Minimum outputs:
- `Character Bible`
- `Scene Master Plan`
- `Asset Prompt Pack`

## Stage 4: Director Queue

This is the orchestration layer.
All prior work should converge here:
- structured shots
- calibrated prompts
- approved assets
- first-frame / last-frame decisions
- per-shot execution mode

Minimum outputs:
- `Director Queue`
- `Shot -> Asset Mapping`
- `Shot -> Prompt Mapping`
- `Shot -> Model Mapping`

Each shot row should answer:
- what is being generated
- with which asset inputs
- by which model
- under which execution mode
- what the retry / fallback path is

## Stage 5: Seedance or Multi-Shot Fusion

Use this stage when the user wants narrative continuity beyond isolated 3-5 second clips.

Possible building blocks:
- image references
- video references
- audio references
- first/last-frame linking
- multi-shot grouping

The job here is not only prompt writing.
The job is choosing which shots should remain separate and which should be grouped into a longer narrative segment.

Minimum outputs:
- `Seedance Handoff`
- `Seedance Multi-Shot Plan`
- `Segment Grouping`

## Recommended Output Order

For industrial requests, respond in this order:
- `Workflow Summary`
- `Provider / Model Routing`
- `Script Breakdown`
- `Calibration Pack`
- `Character Bible`
- `Scene Master Plan`
- `Asset Prompt Pack`
- `Director Queue`
- `Seedance Handoff`

## Working Rule

When the user asks for industrialization, do not stop at “consistency”.
Always also define:
- structure
- mapping
- routing
- queueing
- retry logic
