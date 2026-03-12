# titanX 调研过程｜group / template 代码映射

记录时间：2026-03-12
范围：基于 `23_Group_Template实现边界总表_2026-03-12.md` 与 `titanX/app` 当前代码，做 Group v1 最小实现路径的代码映射，不改总 schema。

---

## 1. 本轮已读依据

### 1.1 正式文档基线
已读：
- `23_Group_Template实现边界总表_2026-03-12.md`

文档已冻结的关键前提：
- Group 采用“parent-child 为底层 + 视觉框为表现 + group metadata 为业务层”的混合模型
- v1 可做：打组、整组移动、解组、组内单节点继续操作、从 group 创建 template、基础颜色/布局入口
- 不建议 v1 做：自动吸附进组、嵌套 group、高级自动布局、完整组执行编排器

### 1.2 当前实际代码
已读：
- `app/src/App.jsx`
- `app/src/App.css`
- `app/src/components/Inspector.jsx`
- `app/src/components/StatusPanel.jsx`

当前代码事实：
- `ReactFlow` 已接通，但只是单文件 demo：`app/src/App.jsx:36`
- state 只有 `nodes / edges / selected / pendingNodeType`：`app/src/App.jsx:37`、`app/src/App.jsx:38`、`app/src/App.jsx:39`、`app/src/App.jsx:40`
- 只有空白 pane 点击创建节点：`app/src/App.jsx:52`
- 还没有：`nodeTypes`、自定义节点、group node、selection toolbar、group toolbar、template serialize 模块、group commands

正式判断：
- 当前 `titanX/app` 在 group/template 维度，比“输出点建节点”还更空
- 它连 custom node / edge 写入 / command 层都没有，所以 group/template 只能先走“最小壳 + 最小命令 + 最小序列化”路线

---

## 2. 现有代码里，group 从哪里最适合接

## 2.1 第一落点仍然是 `app/src/App.jsx`
当前 `FlowCanvas()` 承担了：
- nodes state：`app/src/App.jsx:37`
- edges state：`app/src/App.jsx:38`
- selection 近似态：`selected`，仅单节点：`app/src/App.jsx:39`
- ReactFlow 渲染：`app/src/App.jsx:94`

这说明：
- 当前唯一能统筹 `nodes + edges + selection + commands` 的地方，还是 `FlowCanvas`
- 如果现在直接谈 group，第一步一定还得从 `App.jsx` 接

但注意：
- `selected` 现在只是单节点，不是多选
- 所以 group v1 第一步不是“加 group node”，而是先把 selection 从单节点面板升级成“真正的多选 + 组命令入口”

## 2.2 第二落点是未来的新建 group 组件
目前没有任何 group 组件。

根据 `23_...` 的混合模型，最少要补两个 UI 壳：
- `GroupNode`：承载 parent-child 底层和组框视觉表现
- `SelectionToolbar` 或 `GroupToolbar`：承载打组 / 解组 / 创建模板入口

这意味着：
- group 不能继续只靠 `App.jsx` 内联对象拼出来
- 它必须有单独组件，至少表达标题、颜色、组框命中区、组级 toolbar

## 2.3 第三落点是未来的新建 serializer 模块
文档已经冻结：
- Template 不是 Group 本体
- Template 是从 Group 派生出来的复用结构

因此 template 导出不能放在：
- `Inspector.jsx`
- `StatusPanel.jsx`
- group 组件内部直接 JSON.stringify 当前 node

必须单独落一个 serializer 模块。

---

## 3. 如果采用混合模型，state 应放哪一层

## 3.1 parent-child 底层状态
最适合仍然放在 React Flow 的 `nodes` / `edges` 主 state。

也就是说：
- group node 本身就是一个 node
- child node 的 `parentNode/parentId` 关系，直接写回 node 结构
- 子节点的相对坐标也留在 node.position

为什么：
- 这是 React Flow 自身最擅长承接的一层
- 整组移动、组内 child 跟随，本质就是图节点关系和相对坐标问题

## 3.2 视觉框表现层状态
最适合放在 group node data + 轻量 UI state。

拆法建议：
- 常驻业务字段：挂在 group node data
- 临时 UI 态：挂在 `FlowCanvas` 顶层 UI state

例如：
```ts
groupNode.data = {
  groupId,
  title,
  color,
  layout,
  executable,
  templateable,
}
```

而像下面这些临时态不要塞进 node data：
- 当前是否显示 group toolbar
- 当前是否处于 group rename 态
- 当前多选 toolbar 是否打开

这些更适合放：
- `FlowCanvas` 顶层 `useState`
- 或后续 `flowStore`

## 3.3 group metadata 业务层状态
最适合先挂在 group node data。

原因：
- 当前 app 还没有独立的 group registry
- group 的业务身份需要和画布实例绑定
- v1 先把 group 当“特殊 node + 特殊 commands”最省工程量

### 3.4 template metadata 状态
不应直接挂回 group node。

更合适：
- 由 serializer 导出时临时生成
- 若未来有模板库，再写到模板模块/模板存储层

正式结论：
- parent-child：放 React Flow `nodes` 底层
- group metadata：先放 group node data
- 组级临时 UI 态：放 `FlowCanvas` 顶层 state
- template 导出数据：放单独 serializer / template 模块，不放 group node data

---

## 4. 整组移动 / 解组 / 组内单节点操作，对应哪些代码入口

## 4.1 整组移动
当前代码入口最接近的是：
- `onNodesChange`：`app/src/App.jsx:43-45`

虽然现在它只是简单 `applyNodeChanges()`，但从实现路径看：
- group 移动最终仍会通过 React Flow 的节点变更回调进入这条链
- 所以 `onNodesChange` 是 group move 的底层承接口

真正需要补的是：
- group node 组件
- group 被选中时的命中区规则
- React Flow 节点层的 parent-child 关系

正式映射：
- 底层入口：`onNodesChange`
- 交互入口：未来 `GroupNode` 的组框空白区

## 4.2 解组
当前代码里完全没有解组入口，必须新建 command。

最适合新增：
- `ungroupSelection()` 或 `ungroupGroup(groupId)`

P0 建议先放在：
- `FlowCanvas` 内部 command 函数

P1 再抽到：
- `app/src/flow/groupCommands.js`

解组动作本质要做：
1. 找到 group node
2. 找到所有 child nodes
3. 把 child 相对坐标转回画布绝对坐标
4. 移除 `parentNode/parentId`
5. 删除 group node

所以它不适合挂在：
- `Inspector`
- `StatusPanel`
- 纯 CSS 层

## 4.3 组内单节点操作
当前最接近入口是：
- `onNodeClick={(e, node) => setSelected(node)}`：`app/src/App.jsx:98`

这条链说明：
- 单节点操作现在是直接由 ReactFlow 的 node click 进入 Inspector
- 后续即便有 group，child node 仍应保留这一入口

正式映射：
- 组内单节点操作继续沿用 `onNodeClick`
- 但前提是 group node 不要把所有点击事件都吞掉

这也是为什么 `23_...` 强调：
- 点击组框空白区域 = 组操作
- 点击 child 节点 = 单节点操作

---

## 5. template 从 group 导出时，最小序列化结构该挂在哪个模块

## 5.1 不适合挂的位置
不适合放在：
- `GroupNode.jsx`：组件不该负责导出模板定义
- `Inspector.jsx`：这是面板，不是结构序列化层
- `StatusPanel.jsx`
- `App.css`
- 直接塞进 `App.jsx` JSX 里

## 5.2 最适合的新模块
建议新建：
- `app/src/flow/templateSerializer.js`

如果想把 group 命令也拆出来，建议搭配：
- `app/src/flow/groupCommands.js`

职责划分：
- `groupCommands.js`：决定何时打组 / 解组 / 导出模板
- `templateSerializer.js`：决定 group 如何被净化和序列化

## 5.3 最小序列化结构
根据 `23_...`，当前最小版至少应输出：
```ts
{
  templateId,
  name,
  sourceGroupId,
  nodes: [
    {
      localId,
      nodeType,
      data,
      position,
    },
  ],
  edges: [
    {
      source,
      target,
      sourceHandle,
      targetHandle,
    },
  ],
  group: {
    title,
    color,
    layout,
  },
}
```

这里要特别注意：
- `position` 应是 group 内相对坐标
- 不能把 `selected / dragging / runtime` 之类实例态一起导出

---

## 6. 当前 reactflow 版本下，parentId / extent / selection 能否直接承接

## 6.1 版本现实
当前 `app/package.json` 里依赖是：
- `reactflow: ^11.10.0`

这意味着：
- 代码仍是 v11 口径
- 文档侧提到的 `parentId` / 新口径更多来自后续 `@xyflow/react` 文档

## 6.2 是否能承接 parent-child
结论：能承接，但落代码前要统一“当前版本字段口径”。

原因：
- React Flow v11 已有 group / parent-child 方向的能力
- 从实现路径上，parent-child 作为底层模型是可行的
- 但字段名、示例、细节要按当前版本再核一次

正式工程建议：
- 文档先继续用“parent-child 底层模型”表达
- 真开工时，第一步先确认 `reactflow@11.10.0` 下最终采用 `parentNode` 还是当前代码准备升级后再用 `parentId`
- 不要出现“文档写 parentId，代码却半套 parentNode”的混用状态

## 6.3 `extent`
结论：可承接，但不适合 P0 重度使用。

原因：
- `extent='parent'` 这类能力可以约束 child 在 group 内移动范围
- 但 P0 最小目标是打组、整组移动、解组、组内单节点操作
- 现在就把 child movement constraint 做重，收益不高，复杂度会上来

建议：
- P0 可以先不做严格 extent 约束
- P1 再补 child 在 group 内的边界限制

## 6.4 `selection`
结论：React Flow 选择能力能直接承接，但当前 app 代码没有把它真正接出来。

为什么：
- 文档侧已确认 React Flow 有 selection 多选能力
- 当前 `App.jsx` 只维护了单节点 `selected`
- 还没有 `onSelectionChange`、多选 toolbar、选中 ids 结构

正式判断：
- selection API 足够
- 当前缺的是 app 层没有接 selection 状态，不是库不行

---

## 7. 哪些功能适合 P0，哪些必须后推

## 7.1 适合 P0 直接做
### A. 多选节点
先把单节点 `selected` 升级成：
- `selectedNodeIds`
- `selectedGroupId`

### B. 显式打组
最小路径：
- 读取当前多选 nodes
- 生成 group node
- 挂 parent-child
- 更新子节点相对坐标

### C. 整组移动
直接依赖 React Flow 的 parent-child 跟随机制

### D. 解组
做成显式命令

### E. 组内单节点操作继续可用
继续让 child 节点走 `onNodeClick`

### F. 从 group 创建 template
做最小导出，不接模板库 UI 也行

### G. 基础 group data
至少有：
- `title`
- `color`
- `layout`

## 7.2 必须后推
### A. 自动吸附进组
### B. 拖出组自动 detach
### C. 嵌套 group
### D. 复杂 group 布局算法
### E. 严格 child extent 约束
### F. 完整模板库、模板实例化 UI
### G. 完整组执行编排器

---

## 8. 当前 app 太空壳，缺失到什么程度

## 8.1 缺失程度
当前 `titanX/app` 对 group/template 来说，缺失程度比输出建节点更大：
- 缺多选 state
- 缺 selection toolbar
- 缺 custom node / custom group node
- 缺 group command 层
- 缺 template serializer
- 缺 group metadata 持久化入口
- 缺 group 级 UI（颜色、标题、工具条）

## 8.2 最小壳应该从哪里补
最建议从下面 3 个壳开始补：

### 壳 1：SelectionToolbar
原因：
- 没有多选命令入口，就无从“打组”

### 壳 2：GroupNode
原因：
- 没有 group node，就无从承载 parent-child + 视觉框 + metadata

### 壳 3：templateSerializer
原因：
- 没有独立导出层，template 一定会和 group 实例态混掉

如果要按最小可执行路径排序：
1. 先补多选状态与 `SelectionToolbar`
2. 再补 `GroupNode`
3. 再补 `groupCommands`
4. 最后补 `templateSerializer`

---

## 9. 本轮 7 个必答点的过程结论

### 9.1 group 相关逻辑最适合从哪些文件开始接
- 第一入口：`app/src/App.jsx`
- 第一批新文件：`SelectionToolbar`、`GroupNode`、`groupCommands`、`templateSerializer`

### 9.2 混合模型下 state 分别放哪层
- parent-child：React Flow `nodes`
- group metadata：group node data
- 组级临时 UI 态：`FlowCanvas` 顶层 state
- template 导出结构：独立 serializer 模块

### 9.3 整组移动 / 解组 / 组内单节点操作，各自对应哪些代码入口
- 整组移动：底层走 `onNodesChange`
- 解组：新建 `ungroupGroup()` command
- 组内单节点操作：继续走 `onNodeClick`

### 9.4 template 从 group 导出时，最小序列化结构应该挂在哪个模块
- 最适合挂在 `app/src/flow/templateSerializer.js`

### 9.5 当前 reactflow 版本下，parentId / extent / selection 相关 API 是否能直接承接
- parent-child：能承接，但字段口径要先统一当前版本
- extent：能用，但不适合 P0 重度上
- selection：API 能承接，当前 app 只是还没接出来

### 9.6 哪些功能适合 P0，哪些必须后推
- P0：多选、打组、整组移动、解组、组内单节点操作、导出最小 template
- 后推：自动吸附、嵌套 group、复杂布局、完整模板库、完整组执行编排器

### 9.7 如果 `titanX/app` 当前太空壳，要明确指出缺失程度，并给出从哪个最小壳开始补的路径
- 当前确实太空壳
- 最小起手壳：`SelectionToolbar` -> `GroupNode` -> `groupCommands` -> `templateSerializer`

---

## 10. 新增补强：真实代码入口 + 行号 + 为什么是这里

## 10.1 App.jsx 里哪些现有代码段最适合承接 selection / group / template 入口

### A. `app/src/App.jsx:37-40` — 现有 state 区
现状：
- `nodes`：已有，可直接复用为 group parent-child 结构容器
- `edges`：已有，但目前是只读 state 雏形，必须升级成可写
- `selected`：已有，但只代表单节点选中，是 `activeInspectorTarget` 的雏形
- `pendingNodeType`：已有，可继续保留

为什么是这里：
- 这是当前唯一的 flow shell state 入口
- `selection / toolbarMode / activeInspectorTarget / lastTemplateDraft` 都应紧挨这一段扩出来
- P0 继续放这里是合理的“临时承接”，因为还没有 store

标注：
- **P0 临时承接**：`selection`、`toolbarMode`、`activeInspectorTarget`
- **可直接复用**：`nodes`、`pendingNodeType`
- **需升级而非重写**：`edges`、`selected`

### B. `app/src/App.jsx:43-45` — `onNodesChange`
现状：
- 这里只做 `applyNodeChanges(changes, nds)`

为什么是这里：
- 未来普通节点拖动、group 拖动、child 节点相对位置更新，底层都要回到这条 node change 链
- 它是整组移动的最自然承接口，不需要另造拖拽入口

结论：
- 这是 group move 的**底层入口**
- 这里不应写 group 业务逻辑，但必须保留为所有节点位移的统一回流口

### C. `app/src/App.jsx:52-68` — `handlePaneClick`
现状：
- 空白区域点击时创建普通节点

为什么是这里：
- 这是当前唯一的“往图里新增节点”的统一入口
- 未来即使引入 group/template，也仍然是创建普通业务节点的主入口
- 它不承接 group 逻辑本身，但会和 selection / toolbarMode 存在行为边界

结论：
- 这里适合继续复用为“普通节点创建入口”
- 不适合塞 groupSelection / createTemplateFromGroup

### D. `app/src/App.jsx:73-79` — 现有 `canvas-toolbar`
现状：
- 顶栏只展示标题和 `toolbarTitle`

为什么是这里：
- 这是最适合挂 `toolbarMode` 的现成顶层视觉入口
- P0 可以先在这里临时承接：默认提示 / 多选提示 / group 选中提示

标注：
- **P0 临时承接**：toolbar 文案与 group/selection 入口按钮
- P1 再拆出独立 `SelectionToolbar` / `GroupToolbar`

### E. `app/src/App.jsx:81-91` — 现有 `node-toolbar`
现状：
- 节点库按钮区

为什么是这里：
- 这个区域当前已经是主要操作条
- P0 最省事的做法，是在这一区域右侧或下方临时插入“打组 / 解组 / 创建模板”按钮

标注：
- **P0 临时承接**：selection/group 操作入口
- 不建议把它当最终 toolbar 形态

### F. `app/src/App.jsx:94-104` — `ReactFlow` 渲染入口
现状：
- `nodes={nodes}`
- `edges={edges}`
- `onNodesChange={onNodesChange}`
- `onNodeClick={(e, node) => setSelected(node)}`
- `onPaneClick={handlePaneClick}`

为什么是这里：
- 这是未来接入 `onEdgesChange`、`onSelectionChange`、`nodeTypes`、group node 渲染的唯一主入口
- 也是 selection、group、template 事件链真正接线的地方

### G. `app/src/App.jsx:98` — `onNodeClick`
现状：
- 只做 `setSelected(node)`

为什么是这里：
- 这是当前组内单节点操作的现成入口
- future child node 继续复用这里进入 Inspector
- 所以它应升级成设置 `activeInspectorTarget`，而不是被 group 逻辑替代

### H. `app/src/App.jsx:107-108` — `Inspector` / `StatusPanel` 挂载点
现状：
- `<Inspector node={selected} />`
- `<StatusPanel />`

为什么是这里：
- `selected` 向 `activeInspectorTarget` 升级后，这里就是新的 target 分发口
- `StatusPanel` 也是最合适挂 last template draft / 当前模式摘要的位置

---

## 10.2 哪些位置适合新增 groupCommands 接线

### A. `app/src/App.jsx:43-45` 附近
建议作用：
- 保持 `onNodesChange` 原样
- 不直接在这里调用 `groupCommands`

为什么：
- 这是底层变化流，不是业务命令入口
- 如果把 group 命令掺进这里，后面普通拖动和组拖动容易互相污染

结论：
- **不适合直接接 groupCommands**
- 这里只保留底层 node change 回流

### B. `app/src/App.jsx:81-91` 附近
建议作用：
- 这是 P0 最适合新增 `groupSelection()`、`ungroup()`、`createTemplateFromGroup()` 按钮与调用的位置

为什么：
- 这里已经是用户操作区
- 复用当前工具按钮区，改动最小
- 能直接根据 `toolbarMode` 条件渲染 group 相关动作

标注：
- **P0 临时承接**：groupCommands 接线区

### C. `app/src/App.jsx:94-104` 之前或 props 构造区
建议作用：
- 在 `return` 之前新增：
  - `handleGroupSelection()`
  - `handleUngroup()`
  - `handleCreateTemplateFromGroup()`

为什么：
- 这些 handler 会同时读 `nodes / edges / selection / activeInspectorTarget`
- 它们属于容器命令调用层，最适合先和 `FlowCanvas` 顶层 state 放在同一作用域

标注：
- **P0 临时承接**：命令调用 handler
- command 具体实现仍应放新文件 `groupCommands.js` / `templateCommands.js`

---

## 10.3 哪些现有节点渲染入口未来最适合插入 GroupNode

### A. `app/src/App.jsx:94-104` — `ReactFlow` 组件本体
这是唯一正确的挂载入口。

未来应在这里增加：
- `nodeTypes={nodeTypes}`

为什么：
- 当前 titanX/app 还没有任何 custom node 注册点
- GroupNode 作为 React Flow custom node，只能从这里注入

### B. `app/src/App.jsx:25-34` — `initialNodes / initialEdges`
这里不是直接插 `GroupNode` 的入口，但会成为最小测试 group node 的预置数据入口。

为什么：
- 如果要快速验证 GroupNode 是否渲染，最省事的方法就是先在 `initialNodes` 里插一个 `type: 'group'` 的测试节点
- 所以它是测试态的辅助入口，不是正式接线入口

标注：
- **P0 临时承接**：调试/验证 GroupNode 用
- 正式业务 group 节点仍应由 `groupSelection()` 创建

---

## 10.4 哪些 state 现在已经在 App.jsx 里有雏形，哪些是完全缺失

### 已有雏形
- `nodes`：`app/src/App.jsx:37`
- `edges`：`app/src/App.jsx:38`，但还只是只读
- `selected`：`app/src/App.jsx:39`，可视为 `activeInspectorTarget` 的极简雏形
- `pendingNodeType`：`app/src/App.jsx:40`

### 完全缺失
- `selection`（多选 nodes/edges 容器）
- `toolbarMode`
- `selectedGroupId`
- `activeInspectorTarget` 统一结构
- `lastTemplateDraft`
- `nodeTypes`
- `onEdgesChange`
- `onSelectionChange`

正式判断：
- titanX/app 目前只有单节点编辑雏形
- 凡是 Group v1 所需的容器级状态，基本都还缺失

---

## 10.5 哪些建议只是“新建文件”，哪些其实应该先复用现有代码

### 应先复用现有代码
- `nodes` state：复用 `app/src/App.jsx:37`
- `pendingNodeType`：复用 `app/src/App.jsx:40`
- `handlePaneClick`：复用 `app/src/App.jsx:52-68` 作为普通节点创建入口
- `onNodeClick`：复用 `app/src/App.jsx:98` 作为 child 单节点操作入口，但升级成 target router
- `canvas-toolbar` / `node-toolbar`：复用 `app/src/App.jsx:73-91` 作为 P0 临时操作入口

### 必须新建文件
- `app/src/components/nodes/GroupNode.jsx`
- `app/src/flow/groupCommands.js`
- `app/src/flow/templateCommands.js`

### 可先不新建，P0 临时承接
- `SelectionToolbar.jsx`
- `GroupToolbar.jsx`

原因：
- 这两个 toolbar 在 P0 可以先临时挂在现有 `node-toolbar`
- 只要别把核心命令逻辑写死在 JSX 里即可

---

## 10.6 哪些落点只是权宜之计，属于 P0 临时承接

### `app/src/App.jsx:73-91`
- 现有 toolbar 区用来承接多选/组操作
- **P0 临时承接**

### `app/src/App.jsx:39`
- 用 `selected` 过渡到 `activeInspectorTarget`
- **P0 临时承接**

### `app/src/App.jsx` 内部直接声明 `handleGroupSelection` / `handleUngroup` / `handleCreateTemplateFromGroup`
- 只负责调用 command 模块
- **P0 临时承接**

### `app/src/App.jsx:25-34`
- 在 `initialNodes` 中临时插测试 group node 验证渲染
- **P0 临时承接**

这些都不是最终设计，但对于当前 prototype 来说是最短可执行路径。

---

## 10.7 新增补强：未来最容易冲突的接缝在哪里

本轮要特别补的不是“功能点”，而是未来哪几条线最容易互相顶牛。

### A. Group 线 vs 输出点建节点线
冲突点：
- `handlePaneClick` 当前只负责空白区创建普通节点：`app/src/App.jsx:52-68`
- 未来如果同时引入多选态 / group 态 / template 态，空白区点击语义会变复杂

最容易冲突的接缝：
- 当前准备创建节点时点击 pane
- 当前处于多选态时点击 pane
- 当前 group 选中时点击 pane

结论：
- `handlePaneClick` 未来必须受 `toolbarMode` / `pendingNodeType` 双重约束
- 这是 Group 线和普通建节点线的第一冲突面

### B. Group 线 vs 状态机线
这里的“状态机线”指当前画布容器状态流：
- `selected`
- `pendingNodeType`
- future `selection`
- future `toolbarMode`
- future `activeInspectorTarget`

最容易冲突的接缝：
- 单节点选中 -> 多选态 -> group 选中态 的切换规则
- `onNodeClick` 是否覆盖 `onSelectionChange`
- Inspector 是看 node、看 group，还是看 selection

结论：
- `selected` 不能继续单独存在为唯一选择状态
- 必须升级成更明确的 target router，否则 group/selection 迟早打架

### C. Group 线 vs 数据主链线
这里的数据主链指：
- `nodes`
- `edges`
- future template draft

最容易冲突的接缝：
- groupSelection 改写 child 坐标
- ungroup 还原 child 坐标
- template 导出又要读取相对坐标

这三条链共用同一批数据，但读写意图不同：
- 画布编辑态要绝对+相对混用
- 解组要回绝对坐标
- 模板要只拿相对坐标净化输出

结论：
- `groupCommands.js` 和 `templateCommands.js` 的边界必须非常清楚
- 否则最先出问题的不是 UI，而是坐标口径混乱

### D. Group 线 vs 输出点连线 / 边系统
当前虽然 app 里 edges 很简单：`app/src/App.jsx:31-34`、`app/src/App.jsx:38`
但未来 group 后最容易顶牛的是：
- group 内 child 连外部节点
- 解组后 edge 是否还能稳定指向原 child
- template 导出时哪些 edge 算组内边，哪些算跨组边

结论：
- 当前 edges 还没进入复杂期，但 group/template 一上来，这条线马上会变成高风险接缝
- 所以 `collectGroupMembers(groupId, nodes, edges)` 必须尽早稳定，不然后面边界判断会反复返工

---

## 11. 本轮 7 个必答点的过程结论

### 11.1 group 相关逻辑最适合从哪些文件开始接
- 第一入口：`app/src/App.jsx`
- 第一批新文件：`SelectionToolbar`、`GroupNode`、`groupCommands`、`templateSerializer`

### 11.2 混合模型下 state 分别放哪层
- parent-child：React Flow `nodes`
- group metadata：group node data
- 组级临时 UI 态：`FlowCanvas` 顶层 state
- template 导出结构：独立 serializer 模块

### 11.3 整组移动 / 解组 / 组内单节点操作，各自对应哪些代码入口
- 整组移动：底层走 `onNodesChange`
- 解组：新建 `ungroupGroup()` command
- 组内单节点操作：继续走 `onNodeClick`

### 11.4 template 从 group 导出时，最小序列化结构应该挂在哪个模块
- 最适合挂在 `app/src/flow/templateSerializer.js`

### 11.5 当前 reactflow 版本下，parentId / extent / selection 相关 API 是否能直接承接
- parent-child：能承接，但字段口径要先统一当前版本
- extent：能用，但不适合 P0 重度上
- selection：API 能承接，当前 app 只是还没接出来

### 11.6 哪些功能适合 P0，哪些必须后推
- P0：多选、打组、整组移动、解组、组内单节点操作、导出最小 template
- 后推：自动吸附、嵌套 group、复杂布局、完整模板库、完整组执行编排器

### 11.7 如果 `titanX/app` 当前太空壳，要明确指出缺失程度，并给出从哪个最小壳开始补的路径
- 当前确实太空壳
- 最小起手壳：`SelectionToolbar` -> `GroupNode` -> `groupCommands` -> `templateSerializer`
