# 只有我能抽出东方神明｜项目档案

这个目录是本项目的长期记忆区，不依赖聊天上下文。

## Canonical 说明

- `canonical` 指仓库里唯一长期有效、后续默认以其为准的标准版本。
- 聊天里的临时讨论、试验 prompt、探索图结论，不自动算 canonical。
- 写入 `assets/只有我能抽出东方神明/项目档案/` 的确认版本，才作为续集、补镜头、重做资产时的默认依据。
- 当前以下结构化档案以 `YAML single source of truth` 为准，同名 `.md` 为脚本生成的只读展示：
  - `series/series-bible`
  - `series/style-bible`
  - `series/character-bible`
  - `series/character-asset-prompt-pack`
  - `series/scene-bible`
  - `series/scene-asset-prompt-pack`
  - `series/prop-vfx-bible`
  - `series/prop-vfx-asset-prompt-pack`
  - `episodes/ep001/breakdown`
  - `episodes/ep001/continuity-plan`
  - `episodes/ep001/script-normalized`
  - `episodes/ep001/asset-manifest`
  - `episodes/ep001/director-queue`
- 对以上结构化文件，不要手改生成出来的 `.md`；应先改 `.yaml`，再运行：
  - `python3 scripts/archive_cli.py render assets/只有我能抽出东方神明/项目档案`

## 结构

- `series/`
  - 跨批次复用的总设定、角色总表、场景总表、道具与 VFX 总表
- `episodes/ep001/`
  - 当前 fresh start 的标准化文本、拆解、连续性方案、导演队列、资产清单
- `progress-update-sop.md`
  - 每次工作结束前如何判断是否需要更新进度，以及更新顺序

## 当前约定

- 原始剧本来源：`assets/只有我能抽出东方神明/剧本/只有我能抽出东方神明.docx`
- 当前状态：`fresh reset`
- `Midjourney` 只负责底图
- `Banana Pro` 统一负责改图、修正规则、抽单格和回拼
- 对角色资产，优先增加 `Face Draft` 步骤：先用 `Midjourney` 生成脸部或半身定稿，再用它作为最高优面部参考去生成全身定稿
- 所有后续派生资产都基于这个定稿在 `Banana Pro` 中完成，例如：三视图、表情、角度、反打、局部修订、场景反打、道具变体、VFX look-dev 变体
- 后续 `Banana Pro` 提示词默认都要显式写入“请参考当前资产定稿 / 当前人物全身照”，避免模型漂移

## Fresh Start 工作流

1. 先导入 `script-normalized.yaml`
2. 再补 `breakdown.yaml`
3. 再建立 `series/` 下的 style / character / scene / prop-vfx
4. 新资产落盘后，先更新 `asset-manifest`，再更新对应 bible
