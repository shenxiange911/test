# titanX 调研过程：数据链 / allocator / upstream / writeback

记录时间：2026-03-12
任务范围：只验证 titanX 的业务数据主链，不做泛化 React Flow 教程
对应正式整合稿：`22_数据主链与业务ID总表_2026-03-12.md`

---

## 1. 本轮调研输入

本轮先读并对齐了以下 titanX 正式文档：
- `01_总开发主文档.md`
- `11_画布交互与ReactFlow实现逻辑.md`
- `14_统一字段Schema总表_2026-03-11.md`
- `15_视频模型与API映射总表_2026-03-11.md`
- `17_图片模型与API映射总表_2026-03-12.md`
- `18_文本分析模型与API映射总表_2026-03-12.md`
- `19_音频模型与API映射总表_2026-03-12.md`

补充对齐资料：
- `contracts/runtime_record_contract.md`
- `contracts/image_generate_contract.md`
- `contracts/video_generate_contract.md`
- `contracts/text_analyze_contract.md`
- 当前代码骨架：`app/src/App.jsx`、`ui/app.js`

---

## 2. 当前已确认锚点

### 2.1 allocator 已有明确产品规则
来自 `01_总开发主文档.md`：
- 节点业务 ID 必须按类型独立编号：`text-01`、`image-01`、`video-01`、`audio-01`
- 删除后复用最小缺失编号
- 当前阶段至少先保证手动创建路径稳定使用同一套 allocator

### 2.2 createNode 总线已经在画布文档中明确
来自 `11_画布交互与ReactFlow实现逻辑.md`：
- 双击空白新建
- 输出点拖拽建节点
- 上传附件建节点
- 右键添加节点
都必须统一走 `createNode()` / `nodeFactory`

这意味着 allocator 不应散落在节点组件或菜单动作里，而应收口到 nodeFactory 一层。

### 2.3 upstream 规则已经不是可选增强，而是主链
来自 `01_总开发主文档.md`：
- 输入输出不能是假数据
- 必须按 edge 真实解析上游内容
- Text → Image、Image → Image、Text/Image → Video、附件 → Gemini Text 都要按真实节点数据流走

结论：`upstreamResolver` 必须是 runtime 主链，而不是后期优化项。

### 2.4 runtime / result / writeback 已有雏形，但层次混杂
当前文档里已经出现：
- `BaseNodeShell`
- `CommonRuntimeState`
- `MultiResultState`
- runtime record JSON
- 各节点 contract 的 `result / runtime / promptSnapshot`

但问题是：
- `status` 既出现在 shell，又出现在 contract 输出语义里
- `provider` / `providerFamily` 还没有统一层级
- `resultState.results[]` 与 contract 的 `result.remoteUrl / result.previewUrl` 还没彻底对齐
- runtime record 目前更偏“执行后日志”，还不是节点内写回主真相

---

## 3. 当前代码与文档差异

### 3.1 当前 app 代码没有数据主链
`app/src/App.jsx` 当前只有：
- React Flow 基础 nodes / edges
- pane click 后创建新节点
- 选中节点 inspector

还没有：
- `businessId allocator`
- `nodeFactory`
- `edgeFactory`
- `upstreamResolver`
- `runtime/result` 写回
- `providerFamily`

### 3.2 当前 ui 原型已有 compile / run 影子，但不是节点主链
`ui/app.js` 里已有：
- `compiledConfig`
- `status`
- `runId`
- `taskId`

说明 titanX 方向不是空想，已经在往“编译 -> 执行 -> 状态写回”走。
但当前问题是它还停留在单页 config 原型，不是节点级主链。

### 3.3 现有 contract 的 runtime_records 目录仍写着 titanLX
`runtime_record_contract.md` 里的保存路径还是：
- `titanLX/项目文档/runtime_records/...`

这对 titanX 当前任务是一个直接冲突点，说明文档体系里还残留旧项目名，需要在正式整合稿里压平为 titanX 口径。

---

## 4. 本轮聚焦问题逐项验证

## 4.1 businessId allocator

### 现有约束
- 必须按类型独立编号
- 删除后复用最小缺失编号
- 手动路径先闭环

### 直接实现风险
如果每次创建都扫全量节点再现算：
- 小规模可以接受
- 但删除/撤销/重做/模板实例化会变得难以验证
- 不利于未来自动路径复用

### 更稳方案
采用“按类型扫描现有 businessId -> 取最小缺失编号”的纯函数 allocator：
- 输入：当前所有 nodes + nodeType
- 输出：新 `businessId`
- 不依赖外部计数器
- 撤销/重做后天然正确
- 模板/复制/导入也能共用

结论：
- 这不是传统“自增序号 store”问题
- 更像图状态上的 deterministic allocator

## 4.2 edge 驱动 upstreamResolver

### 已知产品规则
- 输入输出必须跟 edge 真实走
- 左输入、右输出都通过 edge 构成图关系

### 推荐原则
不在节点 data 里长期缓存“上游文本最终值”作为真相来源。
而是：
1. edge + node result/state 才是真相来源
2. 执行前临时编译出 `resolvedUpstream`
3. 再由 payload builder 使用

### 原因
如果把上游内容永久复制进下游节点：
- 上游切主结果后容易过期
- 删除边后容易残留脏数据
- manual-first 下用户会误判“为什么已经断开还在生效”

结论：
- 节点里可以缓存 `upstreamSnapshot` 作为执行快照
- 但不能把它当持续真相

## 4.3 节点输入/输出统一数据壳

现有 `BaseNodeShell` 已经表达了 UI/节点共性，但还缺：
- `flow` 层连接信息不该塞在壳里
- `operator-facing` 输入编辑区字段不该和 runtime 混层
- `compiled` 层应该单独存在，不能每次直接拿原始 UI 字段打 provider

因此更合理的 4 层是：
1. `BaseNodeShell`：节点身份与画布态
2. `NodeOperatorState`：用户编辑态输入
3. `NodeRuntimeState`：执行中间态
4. `NodeResultState`：结果与主次切换

## 4.4 result/runtime 写回结构

### 已有共识
执行后必须写回：
- node status
- runtime info
- remote result urls
- preview info
- local artifact path 或索引引用

### 核心判断
writeback 不应只写 runtime_records JSON 文件。
因为：
- 节点 UI 要立刻变更主结果、状态、预览
- runtime_records 只是持久化副本
- 如果只写文件，再回读节点，会让 manual-first 交互很重

### 因此推荐双写
- 第一写：节点内存状态 / 前端 store
- 第二写：runtime_records / metadata JSON

先 self writeback，再 persistence writeback。

## 4.5 providerFamily 放哪一层

从 01 / 15 / 17 / 18 / 19 文档看，provider family 已经是核心运行时分层：
- `kie-jobs-video`
- `veo-family`
- `kie-jobs-image`
- `flux-kontext`
- `gemini-generate-content`
- `elevenlabs-tts`
- `elevenlabs-music`

### 放在 shell 层的问题
- 用户并不直接编辑它
- 会污染节点 UI 层
- 当用户切模型时，family 其实应从 modelRegistry 推导

### 放在 runtime 层的问题
- payload builder 在 runtime 之前就需要它
- provider adapter 选择不能等到 runtime 结果才知道

### 更合理位置
放在 `compiled config` 层，节点只保留 `model` / `mode` / `subtype` 这类 operator-facing 输入。
执行前通过 registry/compiler 得出：
- `providerFamily`
- `providerModel`
- `adapterKey`

必要时 runtime 层再复制一份已执行快照，便于追查。

结论：
- 真正主归属：compiled-config-level
- runtime 里保留执行快照副本
- shell 层不直接挂为用户可编辑字段

## 4.6 manual-first 下最小数据闭环

最小闭环不需要先做：
- 自动执行工作流
- agent 批量编排
- 全局缓存同步

最小闭环只需要：
1. 创建节点时分配稳定 `businessId`
2. 用户手动编辑当前节点输入
3. 执行前根据 edge 解析上游主结果/文本
4. 编译出统一 payload
5. 选中 provider adapter 执行
6. 写回 node.runtime + node.result
7. 落 runtime record JSON
8. 下游节点能继续从该结果解析上游

---

## 5. 本轮结论压缩

## 5.1 可直接做
- `businessId allocator` 作为 nodeFactory 纯函数
- `upstreamResolver` 作为执行前编译步骤
- `BaseNodeShell / runtime / result` 三层明确拆开
- `writeback` 先写节点，再写 runtime record
- `providerFamily` 放 compiled config 层，并在 runtime 留快照

## 5.2 需要包装后做
- `upstreamSnapshot`：只能作为执行快照，不能取代 edge 真相
- `runtime_records`：只能做持久化副本，不能做 UI 主真相
- `subtype='digital-human'`：可保留产品语义，但不能代替 provider routing

## 5.3 不建议放进 v1
- “下游节点长期保存上游最终文本/URL副本” 作为真相
- 把 `providerFamily` 直接暴露进 UI 表单
- 为 allocator 维护一个独立全局计数器而不基于当前 nodes 求值
- 先引入复杂全局状态库讨论，而不先冻结数据层级

## 5.4 推荐最小实现方案
- `nodeFactory.allocateBusinessId(nodes, nodeType)`
- `upstreamResolver.resolve(nodeId, nodes, edges)`
- `compileExecutionPlan(node)` -> `compiledConfig`
- `dispatchByProviderFamily(compiledConfig)`
- `applyNodeWriteback(nodeId, executionResult)`
- `persistRuntimeRecord(nodeId, executionResult)`

## 5.5 风险点 / 踩坑点
- `runtime_record_contract.md` 仍残留 titanLX 路径，需要在 titanX 正式文档里覆盖矫正
- 现有 `CommonRuntimeState` 太薄，不足以表达 retry/failStage/writeback timing
- 现有 `MultiResultState` 与 contract 的 `result.remoteUrl/previewUrl` 需要统一，不然会双真相
- 视频/图片/文本/音频对 upstream 的依赖不同，resolver 必须按 nodeType 分支，而不是全节点统一硬拼
- manual-first 很容易偷懒把“当前 UI 文本”直接发给 provider，跳过 compiled config；这会导致后续 provider family、prompt compiler、runtime record 全都对不上
