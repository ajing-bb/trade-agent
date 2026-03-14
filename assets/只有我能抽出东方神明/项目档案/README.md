# 只有我能抽出东方神明｜项目档案

这个目录是本项目的长期记忆区，不依赖聊天上下文。

## Canonical 说明

- `canonical` 指仓库里唯一长期有效、后续默认以其为准的标准版本。
- 聊天里的临时讨论、试验 prompt、探索图结论，不自动算 canonical。
- 写入 `assets/只有我能抽出东方神明/项目档案/` 的确认版本，才作为续集、补镜头、重做资产时的默认依据。

## 结构

- `series/`
  - 跨集复用的总设定、角色总表、场景总表、道具与 VFX 总表
- `episodes/ep001/`
  - 当前已导入剧本批次的标准化文本、拆解、连续性方案、导演队列、资产清单

## 当前约定

- 原始剧本来源：`assets/只有我能抽出东方神明/剧本/只有我能抽出东方神明.docx`
- 当前导入范围：`开场 + 第1集 + 第2集 + 第3集`
- `Midjourney` 只负责底图
- `Banana Pro` 统一负责改图、修正规则、抽单格和回拼

## 续集工作流

1. 先读 `series/` 中的总设定和稳定 ID
2. 再读最新 `episodes/` 中的已执行集档案
3. 新续集沿用既有角色 ID、场景 ID、道具/VFX ID
4. 新资产落盘后，先更新 `asset-manifest`，再更新对应 bible

## 新资产落盘后怎么更新

1. 先确认真实落盘路径和稳定 ID。
2. 先更新当前集的 `asset-manifest`。
3. 再按资产类型更新系列档案：
   - 角色图包 -> `series/character-bible`
   - 场景母图 -> `series/scene-bible`
   - 道具、卡牌、法器、异象 -> `series/prop-vfx-bible`
4. 如果新资产改变了全剧统一视觉规则，再更新 `series/style-bible`。
5. 如果新资产影响镜头依赖或执行顺序，再更新对应集的 `director-queue` 或 `continuity-plan`。

只有完成前 3 步，资产才算正式进入 canonical memory。
