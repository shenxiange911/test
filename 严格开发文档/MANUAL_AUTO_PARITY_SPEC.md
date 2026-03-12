# MANUAL_AUTO_PARITY_SPEC.md

## 核心定位
`titanLX` 从设计之初就不是“先手动，后自动”，而是 **手动与自动并行同构** 的节点系统。

这意味着：
- 用户手动能做的动作，系统自动化也必须能做
- 自动化做完的结果，用户也必须能继续接管修改
- 两者不能是两套系统，而必须共用同一套 schema / state / contract

## 并行同构原则
### 1. 同一套节点模型
手动和自动都必须作用于同一套：
- `nodeId`
- `edgeId`
- `nodeType`
- `node.data`
- `runtime`
- `result`

其中 `nodeId` 必须满足：
- 按类型独立编号（如 `text-01` / `image-01`）
- 删除后复用最小缺失槽位
- 手动与自动共享同一个 allocator

### 2. 同一套动作模型
所有动作都应归一到以下 contract：
- `createNode(nodeType, nodeId, position)`
- `updateNode(nodeId, patch)`
- `connectNodes(edgeId, sourceId, targetId)`
- `removeNode(nodeId)`
- `removeEdge(edgeId)`
- `runNode(nodeId)`
- `analyzeNode(nodeId)`
- `pushDownstream(nodeId)`

实现要求：
- 前端原型中不应把主要行为长期散落在页面组件内部
- 应至少抽出统一 action/operator 层（例如 `flowActions.ts`）
- 手动按钮、自动按钮、后续 orchestrator / skill 都应逐步收敛到同一套 action contract

### 3. 同一套状态模型
无论动作来自：
- 用户点击
- 节点内按钮
- orchestrator
- skill
- adapter

最终都必须写回同一个受控状态源。

## 为什么必须这样设计
如果不是同构并行，而是：
- 手动一套逻辑
- 自动另一套逻辑

那后果会是：
1. 自动化只能猜节点标题或 UI 顺序
2. 状态回写不一致
3. 用户接管后容易把自动化结果弄乱
4. 测试成本翻倍
5. 后期 skill 编排会越来越脆

## 项目开发的强制要求
### 每实现一个功能，必须同步补齐 6 件事
1. **UI 行为**
2. **节点 schema 字段**
3. **状态写回规则**
4. **API / adapter contract**
5. **skill / tool contract**
6. **手动 / 自动共用动作映射**

少任何一项，都不算功能完成。

## 节点必须具备的基础语义
每个核心节点都应逐步统一到四段结构：
1. `Input`
2. `Controls`
3. `Analysis`
4. `Output`

这样手动与自动才能共用同一语义面。

## 功能完成标准
一个功能只有同时满足以下条件，才算完成：
- 用户能手动操作
- 系统能自动操作
- 节点有稳定 ID
- 对应 skill 定义清楚使用什么工具
- 输出能按 nodeId 写回
- 下游节点能按 edgeId / sourceId / targetId 正确接收

## Text Node 示例
### 手动
- 用户输入文本
- 用户上传素材
- 用户点击 Analyze
- 用户把分析结果注入文本框
- 用户把文本输出到下游节点

### 自动
- orchestrator 创建 Text Node
- skill 按 `nodeId` 写入文本
- analysis skill 按 `nodeId` 回写 `summary/generatedText`
- downstream dispatcher 按边关系把文本推到下游

### 统一要求
- 无论手动还是自动，最终都走：
  - `updateNode(nodeId, patch)`
  - `pushDownstream(nodeId)`

## Image Node 示例
### 手动
- 用户上传图片
- 用户手动改 model / ratio / size
- 用户点击 Generate

### 自动
- orchestrator 创建 Image Node
- config skill 自动选择 model / ratio / size
- generate skill 按 `nodeId` 提交任务并回写结果

### 统一要求
- 手动选择参数与自动选择参数，本质都必须落到同一个 `updateNode(nodeId, patch)`

## skill/tool contract 最低标准
每个节点功能至少明确：
- `skillName`
- `toolName`
- `input`
- `output`
- `writebackTarget`
- `retryPolicy`
- `idStrategy`

## 禁止项
- 禁止只做 UI 按钮，不定义自动入口
- 禁止只写“AI 分析”“AI 生成”，不写具体工具
- 禁止按标题/位置猜节点
- 禁止把自动化做成独立于节点状态之外的旁路逻辑

## 推荐落地顺序
### 第一步
先把 Text / Image / Result 三节点做成手动/自动同构的最小闭环。

### 第二步
把 skill/tool binding 做成节点 schema 的正式字段。

### 第三步
把 sidebar 临时自动按钮收敛成 orchestrator action。

### 第四步
把真实 runtime 接到 Generate / Analyze 上。
