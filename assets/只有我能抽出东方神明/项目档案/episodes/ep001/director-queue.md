# EP001 Director Queue

> Generated from `director-queue.yaml`. Do not edit this Markdown manually.

## Queue Rules

- `blocked`：关键资产还未正式落盘，镜头不能进入生成阶段
- `ready`：关键资产已齐，可进入静帧或首尾帧生成
- `in_progress`：镜头正在制作
- `done`：镜头已完成并通过当前轮验收

| Shot ID | Purpose | Asset Gate | Primary Refs | Execution Mode | Queue Status | Next Action | Fallback |
| --- | --- | --- | --- | --- | --- | --- | --- |

## Status Notes

- 项目已 fresh reset，当前没有镜头排产。
