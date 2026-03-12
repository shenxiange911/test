# STATE_MANAGEMENT_RULES.md

## 单一事实来源
以下状态必须集中管理，不能出现多套相互冲突的数据源：
- `nodes`
- `edges`
- `selection`
- `viewport`
- `history`
- `orchestrationState`
- `executionState`
- `resultIndex`

## 状态分层

### 1. FlowState
负责画布基础状态：
- nodes
- edges
- viewport
- selectedNodeIds
- selectedEdgeIds
- hoveredNodeId?
- hoveredEdgeId?

### 2. OrchestrationState
负责自动编排状态：
- planning: boolean
- autoWiring: boolean
- applyingPatch: boolean
- autoLayouting: boolean
- lastSummary?: string
- lastPatch?: FlowPatch
- lastError?: string

### 3. ExecutionState
负责节点执行状态：
- nodeId -> status
- nodeId -> runtime
- nodeId -> result
- nodeId -> error
- activeTaskIds

### 4. ResultState
负责结果聚合：
- resultIndex
- latestArtifactsByNode
- branchSummaries

## 更新规则
- 手动连线：只能通过 `onConnect`
- 手动删边：只能通过 edge action / 标准删除入口
- 删除节点：必须同步删除关联 edges
- 自动连线：必须先运行 `validateEdgeCandidate`
- 自动 patch：必须先通过 schema validator
- 自动 patch 不得直接覆盖用户显式编辑字段，除非用户确认
- 结果写入：只能通过 `applyNodeResult(nodeId, result)`
- runtime 状态写入：只能通过 `applyNodeRuntime(nodeId, runtime)`
- resultIndex 更新必须通过统一 reducer / action

## 推荐 store 切分
- React Flow：受控画布状态入口
- Zustand：业务状态与命令动作
- TanStack Query：网络请求缓存与轮询

## 推荐动作集合
- `createNode(type, position)`
- `updateNodeData(nodeId, patch)`
- `removeNode(nodeId)`
- `connectNodes(connection)`
- `removeEdge(edgeId)`
- `applyFlowPatch(patch)`
- `runNode(nodeId)`
- `runWorkflow(entryNodeId?)`
- `analyzeNode(nodeId)`
- `applyNodeResult(nodeId, result)`
- `applyNodeRuntime(nodeId, runtime)`
- `rebuildResultIndex()`

## 自动编排保护规则
- patch 进入 store 前必须完成 schema 校验
- addEdges 前必须完成连接规则校验
- layout 只能调整位置，不得篡改节点语义数据
- 自动生成节点默认标记 `AI Draft`
- 用户手动改过的字段应保留 `userEdited` 元信息，供 patch merge 时保护

## 一对多分支要求
- 单节点多下游连接是合法的一等能力
- branch summary 不能只靠 UI 临时拼接，必须可从 store 稳定生成
- ResultNode 应从上游分支读取聚合结果，而不是自己保存一套独立真相
