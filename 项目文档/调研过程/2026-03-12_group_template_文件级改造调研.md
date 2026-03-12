# titanX Group / Template 文件级改造调研

记录时间：2026-03-12
目标：把 Group v1 路径图继续拆到文件、导出、状态、命令函数级别，为后续真正改代码做施工蓝图
范围限制：只针对 `titanX/app`，不改 schema，不直接改代码

---

## 1. 当前代码基础判断

### 1.1 当前 app 的文件密度极低
当前和本专题直接相关的源文件只有：
- `app/src/App.jsx`
- `app/src/components/Inspector.jsx`
- `app/src/components/StatusPanel.jsx`

这意味着：
- 现在不是“如何把现有复杂系统接 Group”
- 而是“如何用最少文件，把 Group v1 的骨架先补对”

### 1.2 文件级改造的原则
本轮不建议一上来创建太多抽象层。
P0 最小文件层级建议控制为：
- 改 2 个旧文件
- 新增 3~4 个新文件

目标是：
- `App.jsx` 不再继续膨胀成巨型单文件
- 但也不把 prototype 过早拆成过度工程化目录树

---

## 2. App.jsx 需要承担哪些最小 flow shell 职责

### 2.1 仍然是唯一 flow 容器
P0 阶段 `App.jsx` 仍应是唯一持有画布顶层状态的容器。

最小职责必须包含：
- 持有 `nodes`
- 持有 `edges`
- 持有 `selection`
- 持有 `toolbarMode`
- 持有 `activeInspectorTarget`
- 持有 `pendingNodeType`
- 注册 `nodeTypes`
- 把 UI 操作转发给 command 模块

### 2.2 它应该做什么
`App.jsx` 在 P0 应承担：
- 初始化 `nodes / edges`
- 接 `onNodesChange / onEdgesChange`
- 接 `onSelectionChange`
- 处理 `onNodeClick / onPaneClick`
- 根据当前 selection 决定 toolbar 显示逻辑
- 调用 `groupSelection()`
- 调用 `ungroup()`
- 调用 `createTemplateFromGroup()`
- 把 inspector target 传给 `Inspector`

### 2.3 它不应该做什么
`App.jsx` 不应直接实现：
- 打组坐标换算
- 解组坐标换算
- 模板序列化细节
- group node 内部 UI 结构

这些都要外移，否则 `App.jsx` 很快会再次失控。

### 2.4 建议新增的最小 state
P0 最小建议：
- `nodes`
- `edges`
- `selection`
- `toolbarMode`
- `activeInspectorTarget`
- `pendingNodeType`
- 可选：`lastTemplateDraft`

其中：
- `selection` 建议保存 `{ nodes, edges }`
- `toolbarMode` 建议最少三态：`default | multi-select | group-selected`
- `activeInspectorTarget` 建议保存统一对象，而不是只保存 node

例如：
```ts
{
  type: 'node' | 'group' | 'selection' | 'none',
  nodeId?: string,
  groupId?: string
}
```

---

## 3. GroupNode.jsx 需要暴露哪些 props / data 字段

### 3.1 这个文件的定位
`GroupNode.jsx` 是“表现层节点”，不是命令层，不是模板层。

它要负责：
- 把结构上的 group node 渲染成可识别组框
- 提供标题、颜色、空白区命中
- 为组操作按钮提供挂点

### 3.2 最小 props
基于 React Flow custom node 约定，最小需要使用这些 props：
- `id`
- `data`
- `selected`
- `dragging`

如果后续要挂 group 操作按钮，建议 `data` 中预留回调入口，但 P0 可以只先显示，不必真的透传完整 command。

### 3.3 data 最小字段
建议 `data` 至少包含：
```ts
{
  kind: 'group',
  groupId: string,
  title: string,
  color?: string,
  layout?: 'grid' | 'horizontal',
  templateable?: boolean,
  executable?: boolean
}
```

### 3.4 P0 不建议塞进 data 的内容
不要塞：
- 当前 selection 结果
- runtime result
- template draft
- Inspector UI 展开态
- 临时 hover 状态

这些都不是 group node 的稳定业务字段。

### 3.5 最小 UI 职责
P0 阶段 `GroupNode.jsx` 至少做：
- 渲染标题
- 渲染颜色边框 / 背景
- 渲染组选中态
- 提供空白区域视觉

P0 可以先不做：
- 完整 toolbar
- 布局切换按钮
- 组内统计标签

---

## 4. groupCommands.js 里至少需要哪些导出函数

### 4.1 这是最核心的结构模块
P0 的 Group v1 能不能少返工，主要看这个文件有没有把“结构变化”和“坐标变化”集中起来。

### 4.2 至少需要的导出函数
建议最小导出：

#### `groupSelection(params)`
职责：
- 接收当前选中 nodes / edges
- 创建 group node
- 计算 group bounds
- 把 child 转成 parent-relative
- 返回新的 `nodes / edges / groupId`

#### `ungroup(params)`
职责：
- 找到 group 和 child members
- child 坐标转回绝对坐标
- 移除 parent relation / extent
- 删除 group node
- 返回新的 `nodes / edges`

#### `collectGroupMembers(groupId, nodes, edges)`
职责：
- 收集某 group 下的 child nodes
- 收集组内 edge
- 为模板导出复用

#### `computeGroupBounds(nodes)`
职责：
- 基于选中节点计算 group 框范围
- 统一 padding 策略

#### `toRelativeNodePosition(node, groupBounds)`
职责：
- 把绝对坐标转换成 group 相对坐标

#### `toAbsoluteNodePosition(node, groupNode)`
职责：
- 解组时把相对坐标还原成画布绝对坐标

### 4.3 可选但建议一并留口
- `buildGroupNode(groupBounds, options)`
- `getGroupChildNodes(groupId, nodes)`
- `getGroupInternalEdges(groupId, nodes, edges)`

这些函数即使 P0 不全部暴露，也适合内部先拆出来。

---

## 5. templateCommands.js 里至少需要哪些导出函数

### 5.1 这个文件是 Group -> Template 的边界文件
它必须承担“导出态净化”职责。

### 5.2 至少需要的导出函数

#### `createTemplateFromGroup(params)`
职责：
- 输入 `groupId / nodes / edges`
- 调 `collectGroupMembers()`
- 调内部序列化逻辑
- 输出最小 template draft

#### `serializeGroupToTemplateDraft(groupNode, childNodes, childEdges)`
职责：
- 生成最终 template draft 对象
- 写入 `templateId / name / groupMeta / nodes / edges / nodePositions`

#### `stripRuntimeFields(node)`
职责：
- 删掉 React Flow 实例态字段
- 防止直接 dump node 原对象

#### `buildRelativeNodePositions(childNodes)`
职责：
- 导出模板内的相对坐标映射

### 5.3 可选但建议预留
- `normalizeTemplateNode(node)`
- `normalizeTemplateEdge(edge)`
- `buildTemplateName(groupNode)`

P0 如果不做模板命名面板，至少也要有默认命名生成逻辑。

---

## 6. selection / toolbar / activeInspectorTarget 各自建议放哪层

### 6.1 selection
建议放：`App.jsx` 顶层 UI state

原因：
- 它由 React Flow 回调产生
- 它是容器级交互状态
- 不应写回 nodes/edges 数据本体之外的业务字段

### 6.2 toolbar
建议放：`App.jsx` 顶层 UI state

更具体地说：
- 不必保存完整 toolbar 配置对象
- 只保存 `toolbarMode`
- 由 `selection` 推导显示内容

### 6.3 activeInspectorTarget
建议放：`App.jsx` 顶层 UI state

原因：
- Inspector 只是消费方
- target 应由容器统一决定
- 不能让 `Inspector.jsx` 自己推断整个画布状态

### 6.4 不建议放的位置
以下都不建议放：
- `GroupNode.jsx`
- `groupCommands.js`
- React Flow node.data

因为这些都是短生命周期 UI 状态，不是结构数据。

---

## 7. 哪些状态继续留在 React Flow nodes/edges，哪些不要塞进去

### 7.1 应继续留在 nodes/edges 的内容
这些属于结构态，必须留在 React Flow graph 中：
- node id
- edge id
- node type
- node position
- group node style width/height
- child 的 parent relation
- child 的 `extent: 'parent'`
- group node.data 的稳定业务字段（title / color / layout 等）

### 7.2 不要塞进 nodes/edges 的内容
这些应留在容器/UI态，不要写入 graph 数据：
- 当前多选结果
- toolbar 当前模式
- 当前 inspector 目标
- 弹窗开关
- 临时 hover / focus UI 状态
- 导出的 template draft 缓存

### 7.3 也不要直接写回 node.data 的内容
即便看起来和 group 有关，也不要先塞进去：
- 当前模板导出结果
- 当前组执行结果
- 当前运行错误列表
- 当前 inspector 展开折叠状态

P0 先保持 data 干净，后面才不容易污染模板。

---

## 8. P0 阶段每个文件最小需要新增什么

## 8.1 `app/src/App.jsx`
P0 最小新增：
- `edges` 变成可写 state
- `selection` state
- `toolbarMode` state
- `activeInspectorTarget` state
- `onEdgesChange`
- `onSelectionChange`
- `nodeTypes` 注册 `group`
- 调 `groupSelection()` 的入口
- 调 `ungroup()` 的入口
- 调 `createTemplateFromGroup()` 的入口
- 给 `Inspector` 改传 `target`，而不是只传 `node`

## 8.2 `app/src/components/Inspector.jsx`
P0 最小新增：
- props 从 `node` 升级为 `target`
- 能区分：普通节点态 / group 态 / none 态
- group 态先只显示只读字段：title / color / layout / actions 占位

P0 不必马上做：
- 多选态表单
- 模板命名 UI
- 复杂 group 设置编辑

## 8.3 `app/src/components/StatusPanel.jsx`
P0 最小新增：
- 可选显示最近一次 template draft 状态
- 或至少显示“当前 selection / 当前 group”摘要

如果不做也可以，但它是最适合挂 debug 输出的位置。

## 8.4 `app/src/components/nodes/GroupNode.jsx`
P0 最小新增文件内容：
- 默认导出 `GroupNode`
- 使用 `data.title / data.color / data.layout`
- 渲染可见组框和标题
- 渲染组选中态样式

## 8.5 `app/src/flow/groupCommands.js`
P0 最小新增文件内容：
- 导出 `groupSelection`
- 导出 `ungroup`
- 导出 `collectGroupMembers`
- 导出 `computeGroupBounds`
- 导出 `toRelativeNodePosition`
- 导出 `toAbsoluteNodePosition`

## 8.6 `app/src/flow/templateCommands.js`
P0 最小新增文件内容：
- 导出 `createTemplateFromGroup`
- 导出 `serializeGroupToTemplateDraft`
- 导出 `stripRuntimeFields`
- 导出 `buildRelativeNodePositions`

---

## 9. 推荐的文件创建顺序和落地顺序

### 9.1 第一顺序：先改 `App.jsx`
原因：
- 它先成为 flow shell，后面新文件才有接入点

### 9.2 第二顺序：创建 `groupCommands.js`
原因：
- 先把结构变换算法稳定下来
- 不要先画 UI 再回头补结构

### 9.3 第三顺序：创建 `GroupNode.jsx`
原因：
- 当 group 结构能生成后，再补 visual shell 才不会做空壳 UI

### 9.4 第四顺序：创建 `templateCommands.js`
原因：
- Group 能生成后，Template 导出才有真实输入

### 9.5 第五顺序：改 `Inspector.jsx`
原因：
- 等 `activeInspectorTarget` 明确后再接最稳

### 9.6 第六顺序：再决定是否补 `StatusPanel.jsx`
它更适合作为调试和反馈位，不是 P0 主链核心。

---

## 10. 哪些点最容易因为 prototype 结构导致返工

### 10.1 最大返工点：把 `App.jsx` 当最终业务归宿
如果 P0 直接把：
- 打组
- 解组
- 模板导出
- inspector 路由
全都写死在 `App.jsx`，后面一定炸。

### 10.2 第二返工点：GroupNode 里直接写解组/模板导出算法
这会导致：
- UI 与结构耦合
- 后续换 toolbar 位置时逻辑难迁移

### 10.3 第三返工点：selection / toolbar / inspector target 写进 node.data
这是 prototype 最容易犯的错。
一旦写进去：
- 模板导出会带脏状态
- 节点复制会带 UI 污染
- 组和模板边界被打烂

### 10.4 第四返工点：模板直接 dump nodes
如果不经过 `templateCommands.js` 的净化层，后面模板结构一定污染实例态字段。

### 10.5 第五返工点：没先确定 parent relation 写法
当前版本虽兼容 `parentNode / parentId`，但如果项目代码里到处手写不同口径，后面升级版本时很容易出隐性 bug。

---

## 11. 过程稿最终结论

### 11.1 App.jsx 的最小 shell 职责
- 托管 flow state
- 托管 selection / toolbar / inspector target
- 挂 command 入口
- 注册 nodeTypes

### 11.2 GroupNode.jsx 的最小职责
- 只做表现层 group node
- 暴露并消费稳定 group data 字段
- 不写结构算法

### 11.3 groupCommands.js 的最小职责
- 统一处理打组 / 解组 / 成员收集 / 坐标换算

### 11.4 templateCommands.js 的最小职责
- 统一处理 Group -> Template draft 导出与净化

### 11.5 文件级最优落地顺序
- 先 `App.jsx`
- 再 `groupCommands.js`
- 再 `GroupNode.jsx`
- 再 `templateCommands.js`
- 最后 `Inspector.jsx`

这就是 P0 阶段最不容易返工的文件级改造路径。
