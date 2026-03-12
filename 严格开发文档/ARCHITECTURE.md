# ARCHITECTURE.md

> ⚠️ 重要说明  
> 本文档描述的是 titanLX 的**目标架构**与推荐分层，不等于当前代码已经全部按此结构落地。  
> 当前阶段真实已完成 / 未完成，请优先结合：
> - `../项目文档/IMPLEMENTATION_REDLINES.md`
> - `./ACCEPTANCE_CHECKLIST.md`

## 架构目标
实现一个 **OpenClaw 原生可控的媒体工作流画布**，满足：
- 媒体/分析/storyboard/结果节点混合编排
- 用户手动编辑 + OpenClaw 自动编排双模式共存
- 一对多分支作为一等能力
- 节点内真实执行、真实结果回写
- 复用现有 multimedia / storyboard runtime

## 当前阶段优先级说明
当前阶段优先级不是“先把所有分层做漂亮”，而是先保证：
1. 产品形态正确（默认卡片态 + 下方独立编辑区）
2. 节点真实互联可用
3. Image Generate 真返回图片并显示在节点中
4. 然后再继续收动作层、抽 store、补更多节点族

---

## 总体分层（目标架构）

### 1. Canvas UI Layer
目标文件示例：
- `FlowCanvas.tsx`
- `NodePalette.tsx`
- `NodeCard/*.tsx`
- `NodeEditor/*.tsx`
- `ResultPanel.tsx`

职责：
- 渲染节点画布
- 渲染默认卡片态
- 渲染节点下方独立编辑区
- 响应拖拽、连线、删除、选中
- 提供手动操作入口

### 2. Flow State Layer
目标文件示例：
- `flow.store.ts`
- `flow.selectors.ts`
- `history.store.ts`
- `execution.store.ts`
- `template.store.ts`

职责：
- 管理 nodes / edges / selection / viewport
- 管理手动编辑状态与自动编排状态
- 管理节点运行态、分析态、结果态
- 管理模板列表、模板查询、模板合并模式
- 管理撤销重做

### 3. Semantic Node Layer
目标文件示例：
- `node.registry.ts`
- `node.factory.ts`
- `connection.rules.ts`
- `node.capabilities.ts`

职责：
- 定义节点种类与语义
- 定义输入/输出端口和连接规则
- 定义哪些节点可运行、可分析、可写回结果
- 保证画布是“媒体语义画布”而不是通用脚本图

### 4. Control Contract Layer
定义节点控制类型：
- `manual`
- `hybrid`
- `skill`
- `acp`
- `local_runtime`
- `provider_api`
- `result`

职责：
- 明确节点是手动、自动还是混合控制
- 定义每类节点如何映射到 OpenClaw 能力
- 隔离前端语义与底层执行细节
- 明确每个功能对应的 skill/operator/tool contract

### 5. Orchestration Layer
目标文件示例：
- `orchestrator.service.ts`
- `autowire.service.ts`
- `autolayout.service.ts`
- `flow-patch.service.ts`
- `prompt-compiler.service.ts`
- `template.service.ts`

职责：
- 根据用户目标生成节点草案
- 生成候选连线与布局
- 产出合法 `FlowPatch`
- 编译节点最终 prompt
- 管理模板保存、模板载入、模板 merge mode

### 6. Execution Adapter Layer
目标文件示例：
- `execution.registry.ts`
- `storyboard.adapter.ts`
- `multimedia.adapter.ts`
- `result-reader.adapter.ts`

职责：
- 把节点运行请求映射到 OpenClaw skill / ACP / 本地 runtime / provider API
- 对接现有稳定脚本与异步任务系统
- 规范化状态与结果，避免 UI 直接读取底层原始结构

### 7. Runtime Layer
复用既有稳定执行链：
- storyboard 生成脚本
- watcher 轮询
- notifier
- tasks.json / results/*.json

职责：
- 远程任务提交
- 异步状态推进
- 结果落盘
- 通知等副作用

---

## 当前代码与目标架构的关系
当前代码仍处于“原型向稳定分层过渡”阶段。  
当前真实实现更接近：
- `App.tsx` 接线层
- `lib/actions/*`
- `lib/hooks/*`
- `components/nodes/*`
- `components/ui/*`
- `lib/promptCompiler.ts`
- `lib/executionPayloadBuilder.ts`
- `lib/runtimeClient.ts`

因此：
- 本文档中的分层可以作为目标方向
- 不能直接把所有目标层都当成“当前已落地事实”

---

## 手动 / 自动并行设计结论
手动模式与自动模式不是先后关系，而是并行同构关系。

具体要求：
- UI 只是同一套 node/edge contract 的一种入口
- orchestrator / skill / adapter 是另一种入口
- 两者最终都写回同一套状态源
- 手动编辑与自动编排必须共用同一套 `customPrompting` / template / compiledPrompt 机制
- 所有动作都必须按稳定 `nodeId` / `edgeId` 操作

## Prompt / Template 编译原则
- `customPrompting` 属于 operator-facing 正式字段，不是 UI 临时态
- 模板系统保存的是可复用配置，不保存 taskId、provider 原始响应、运行错误
- 生成节点默认编译顺序：上游 context -> 节点主 prompt -> 模板片段 -> `customPrompting.userPrompt` -> 结构化 directives -> provider normalize
- 编译结果应回写 `lastCompiledPrompt`，并在运行后保存 prompt snapshot / template snapshot / compiledPromptHash

## v1 范围约束
- 先做强语义媒体工作流，不做通用 workflow 平台
- 当前最小主线先锁 Text / Image
- 必须先过：默认卡片态、下方独立编辑区、真实互联、真实出图
- 底层必须支持未来 OpenClaw 自动创建与执行，而不是只支持手动拖线
