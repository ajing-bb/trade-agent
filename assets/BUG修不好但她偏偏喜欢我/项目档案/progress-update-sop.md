# Progress Update SOP

用于保证本项目支持：

- 随时退出 Codex
- 下次继续时快速恢复进度
- 不依赖聊天上下文

## 一句话原则

只要发生了 `定稿 / 落盘 / 状态变化 / 规则变化 / 阻塞变化` 这五类事情中的任意一种，就更新进度。

## Single Source of Truth

以下结构化档案以 `.yaml` 作为唯一事实源：

- `series/series-bible.yaml`
- `series/style-bible.yaml`
- `series/character-bible.yaml`
- `series/character-asset-prompt-pack.yaml`
- `series/scene-bible.yaml`
- `series/scene-asset-prompt-pack.yaml`
- `series/prop-vfx-bible.yaml`
- `series/prop-vfx-asset-prompt-pack.yaml`
- `episodes/ep001/breakdown.yaml`
- `episodes/ep001/continuity-plan.yaml`
- `episodes/ep001/script-normalized.yaml`
- `episodes/ep001/asset-manifest.yaml`
- `episodes/ep001/director-queue.yaml`

对应 `.md` 为脚本生成的只读展示，不应手工编辑。

渲染命令：

```bash
python3 scripts/archive_cli.py render assets/BUG修不好但她偏偏喜欢我/项目档案
```

## Fresh Start 默认顺序

1. 从 `script-normalized.yaml` 开始重新导入剧本
2. 补 `breakdown.yaml`
3. 补 `series/` 中的 style / character / scene / prop-vfx
4. 资产正式落盘后，再更新 `asset-manifest.yaml`
5. 有镜头依赖变化时，再更新 `director-queue.yaml` 和 `continuity-plan.yaml`

## 不算进度更新的内容

- 聊天里讨论过但没落档的结论
- 外部平台里挑中的图但没有保存到仓库
- 临时试过的 prompt
- 口头确认但没有改状态
