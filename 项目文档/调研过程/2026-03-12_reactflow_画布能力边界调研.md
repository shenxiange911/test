# React Flow 画布能力边界调研 - 过程稿

调研时间：2026-03-12
调研目标：验证 React Flow 是否适合承载 titanX 已确认的画布交互需求

---

## 1. 调研范围

titanX 当前已确认的画布交互需求：
1. group node（打组/解组）
2. 框选后工具条
3. 右键菜单（节点右键 + 画布右键）
4. 鼠标附近创建节点
5. picking mode（焦点拾取模式）
6. 点击空白关闭编辑器
7. 节点局部展开编辑区（下方编辑框）
8. viewport 缩放/平移下的菜单与节点定位

---

## 2. 官方文档核心发现

### 2.1 Group Node 原生支持

**官方文档来源**：
- https://reactflow.dev/learn/layouting/sub-flows
- https://reactflow.dev/examples/grouping/sub-flows

**核心能力**：
- React Flow 原生支持 `parentId` 字段（v11.11.0 前叫 `parentNode`）
- 子节点 position 相对父节点定位
- 父节点移动时子节点自动跟随
- 可设置 `extent: 'parent'` 限制子节点不能拖出父节点
- 支持 `type: 'group'` 作为便捷父节点类型（无 handle）

**关键约束**：
- **节点数组顺序要求**：父节点必须出现在子节点之前，否则处理不正确
- 子节点不是真正的 DOM 子元素，只是逻辑关联
- 边的 z-index 行为：连接到有 parent 的节点的边会渲染在节点上方

**titanX 对齐结论**：
- ✅ 可直接用于打组
- ⚠️ 需要自己实现"框选后打组"的逻辑
- ⚠️ 需要自己实现"解组"逻辑
- ⚠️ 需要自己维护节点数组顺序

---

### 2.2 框选后工具条

**官方文档来源**：
- https://reactflow.dev/examples/grouping/selection-grouping（Pro 示例）
- https://reactflow.dev/examples/nodes/node-toolbar

**核心能力**：
- React Flow 提供 `<NodeToolbar>` 组件
- 可通过 `isVisible` 控制显示
- 可通过 `position` 控制位置（top/right/bottom/left）
- 可通过 `align` 控制对齐（start/center/end）
- 自动跟随节点位置和 viewport 变化

**titanX 对齐结论**：
- ✅ `NodeToolbar` 可用于单节点工具条
- ⚠️ 多选工具条需要自己实现：
  - 监听 `onSelectionChange`
  - 计算多选节点的中心或边界
  - 渲染自定义浮层组件
  - 手动处理 viewport 变化时的位置更新

**官方 Pro 示例确认**：
- selection-grouping 示例展示了"框选后出现 Group Nodes 按钮"
- 这是 Pro 示例，说明官方认为这是高级场景
- 但核心逻辑仍需自己实现

---

### 2.3 右键菜单

**官方文档来源**：
- https://reactflow.dev/examples/interaction/context-menu

**核心能力**：
- 提供 `onNodeContextMenu` 事件
- 提供 `onPaneContextMenu` 事件
- 事件参数包含 `event.clientX/clientY`
- 需要自己实现菜单组件和定位逻辑

**官方示例代码关键点**：
```javascript
const onNodeContextMenu = useCallback((event, node) => {
  event.preventDefault();
  const pane = ref.current.getBoundingClientRect();
  setMenu({
    id: node.id,
    top: event.clientY < pane.height - 200 && event.clientY,
    left: event.clientX < pane.width - 200 && event.clientX,
    right: event.clientX >= pane.width - 200 && pane.width - event.clientX,
    bottom: event.clientY >= pane.height - 200 && pane.height - event.clientY,
  });
}, [setMenu]);

const onPaneClick = useCallback(() => setMenu(null), [setMenu]);
```

**titanX 对齐结论**：
- ✅ 事件钩子原生支持
- ⚠️ 菜单组件需要自己实现
- ⚠️ 防止菜单超出屏幕的逻辑需要自己写
- ⚠️ 关闭菜单的逻辑需要自己写（通常监听 `onPaneClick`）

---

### 2.4 鼠标附近创建节点

**官方文档来源**：
- https://reactflow.dev/api-reference/types/react-flow-instance

**核心能力**：
- 提供 `screenToFlowPosition(clientPosition)` 方法
- 可将屏幕坐标转换为 flow 坐标
- 通过 `useReactFlow()` hook 或 `onInit` 获取实例

**titanX 对齐结论**：
- ✅ 坐标转换原生支持
- ⚠️ 双击空白、右键菜单、拖拽创建等触发逻辑需要自己实现
- ⚠️ 创建节点菜单需要自己实现

**推荐实现**：
```javascript
const { screenToFlowPosition } = useReactFlow();

const onPaneDoubleClick = (event) => {
  const position = screenToFlowPosition({
    x: event.clientX,
    y: event.clientY,
  });
  // 打开创建菜单或直接创建节点
};
```

---

### 2.5 Picking Mode（焦点拾取模式）

**官方文档来源**：
- 未找到官方 "picking mode" 专用 API
- 相关能力散落在交互配置中

**titanX 需求回顾**：
- 进入焦点编辑后，画布进入 picking mode
- 提示"点击其他节点以提取元素"
- 点击节点后写回参考图/标签
- 退出按钮

**React Flow 可用能力**：
- `onNodeClick` 事件
- `elementsSelectable` 可控制是否可选中
- `nodesDraggable` 可控制是否可拖拽
- `panOnDrag` 可控制是否可平移

**titanX 对齐结论**：
- ⚠️ 需要自己实现 mode 状态机
- ⚠️ 需要自己实现模式提示 UI
- ⚠️ 需要在 picking mode 下：
  - 禁用默认选中行为（或复用选中但改变视觉）
  - 监听 `onNodeClick` 提取数据
  - 显示退出按钮
  - 退出后恢复正常交互

**推荐实现**：
```javascript
const [canvasMode, setCanvasMode] = useState('idle'); // 'idle' | 'picking'

<ReactFlow
  onNodeClick={canvasMode === 'picking' ? onPickNode : onNormalNodeClick}
  elementsSelectable={canvasMode !== 'picking'}
  ...
/>
```

---

### 2.6 点击空白关闭编辑器

**官方文档来源**：
- https://reactflow.dev/api-reference/react-flow

**核心能力**：
- 提供 `onPaneClick` 事件
- 事件在点击画布空白处时触发

**titanX 对齐结论**：
- ✅ 事件钩子原生支持
- ⚠️ 需要自己维护"当前打开的编辑器"状态
- ⚠️ 需要在 `onPaneClick` 中关闭编辑器

**已知坑点**：
- GitHub issue #5563：`selectionOnDrag=true` 时 `onPaneClick` 不触发（v12.9.0 bug）
- 如果 titanX 使用 `selectionOnDrag`，需要注意这个问题
- 临时方案：条件性禁用 `onPaneClick` 或使用其他事件

---

### 2.7 节点局部展开编辑区

**titanX 需求回顾**：
- 节点本身保持缩略图/摘要卡片
- 点击节点后，下方出现独立编辑框
- 编辑框不是节点内部展开，而是画布上的独立浮层

**React Flow 可用能力**：
- 自定义节点组件
- `<Panel>` 组件（固定位置浮层）
- 自己实现的绝对定位浮层

**titanX 对齐结论**：
- ⚠️ 下方编辑框不适合用 `NodeToolbar`（位置不对）
- ⚠️ 不适合用 `<Panel>`（Panel 是固定位置，不跟随节点）
- ✅ 推荐方案：
  - 自己实现绝对定位的编辑框组件
  - 监听节点选中状态
  - 使用 `flowToScreenPosition` 计算节点屏幕位置
  - 将编辑框定位到节点下方
  - 监听 viewport 变化更新位置

**关键 API**：
```javascript
const { flowToScreenPosition } = useReactFlow();
const screenPos = flowToScreenPosition({ x: node.position.x, y: node.position.y });
```

---

### 2.8 Viewport 缩放/平移下的菜单与节点定位

**官方文档来源**：
- https://reactflow.dev/learn/concepts/the-viewport
- https://reactflow.dev/api-reference/types/react-flow-instance

**核心能力**：
- `onMove` / `onMoveStart` / `onMoveEnd` 事件
- `getViewport()` 获取当前 viewport
- `screenToFlowPosition` / `flowToScreenPosition` 坐标转换
- `NodeToolbar` 自动跟随 viewport

**titanX 对齐结论**：
- ✅ `NodeToolbar` 自动处理 viewport 变化
- ⚠️ 自定义浮层（右键菜单、编辑框）需要：
  - 监听 `onMove` 更新位置
  - 或在每次渲染时重新计算位置
  - 或在 viewport 变化时关闭浮层

**推荐策略**：
- 右键菜单：viewport 变化时关闭（简单）
- 编辑框：监听 `onMove` 更新位置（复杂但体验好）

---

## 3. 交互配置能力

### 3.1 选择模式

**官方文档来源**：
- https://reactflow.dev/learn/concepts/the-viewport
- https://reactflow.dev/api-reference/react-flow

**默认行为**：
- pan: pointer drag
- zoom: pinch or scroll
- select: shift + pointer drag

**设计工具模式**（类 Figma）：
- `panOnScroll={true}`
- `selectionOnDrag={true}`
- `panOnDrag={false}`
- pan: scroll, middle/right mouse drag, space + pointer drag
- zoom: pinch or cmd + scroll
- select: pointer drag

**titanX 对齐结论**：
- ✅ 可配置为设计工具模式
- ⚠️ 需要决定 titanX 的默认交互模式
- ⚠️ `selectionOnDrag` 有已知 bug（#5563）

---

### 3.2 Lasso Selection

**官方文档来源**：
- https://reactflow.dev/examples/whiteboard/lasso-selection

**核心能力**：
- 官方提供示例但不是内置组件
- 需要自己实现 Lasso 组件
- 可配合 `selectionMode="partial"` 支持部分选中

**titanX 对齐结论**：
- ⚠️ 如果需要 lasso 选择，需要自己实现或复用官方示例代码
- ⚠️ 不是 v1 必需功能

---

## 4. 关键约束与踩坑点

### 4.1 节点数组顺序
- **约束**：父节点必须在子节点之前
- **影响**：打组/解组时需要重新排序
- **推荐**：维护一个 `sortNodesByParent` 工具函数

### 4.2 事件冲突
- **问题**：`selectionOnDrag` 会阻止 `onPaneClick`（v12.9.0 bug）
- **影响**：点击空白关闭编辑器可能失效
- **临时方案**：
  - 不使用 `selectionOnDrag`
  - 或使用 `onPaneMouseDown` 替代
  - 或等待官方修复

### 4.3 自定义浮层定位
- **问题**：自定义浮层不会自动跟随 viewport
- **影响**：右键菜单、编辑框在缩放/平移后位置错误
- **推荐方案**：
  - 简单浮层：viewport 变化时关闭
  - 复杂浮层：监听 `onMove` 更新位置

### 4.4 坐标系转换
- **问题**：屏幕坐标 vs flow 坐标容易混淆
- **影响**：菜单定位、节点创建位置错误
- **推荐**：
  - 创建节点：用 `screenToFlowPosition`
  - 定位浮层：用 `flowToScreenPosition`
  - 统一在一个地方处理转换

### 4.5 NodeToolbar 限制
- **问题**：`NodeToolbar` 只能用于单节点
- **影响**：多选工具条需要自己实现
- **推荐**：
  - 单节点工具条：用 `NodeToolbar`
  - 多选工具条：自己实现浮层

---

## 5. 与 titanX 产品规则逐条对照

### 5.1 双击空白新建节点
- **titanX 需求**：双击画布空白处，打开新建节点菜单
- **React Flow 支持**：✅ 可通过 `onPaneDoubleClick` + `screenToFlowPosition` 实现
- **需要自己做**：菜单组件、节点工厂

### 5.2 上传附件自动识别节点类型
- **titanX 需求**：上传附件后自动创建对应节点
- **React Flow 支持**：✅ 可通过 `addNodes` 实现
- **需要自己做**：文件类型识别、节点工厂

### 5.3 左输入/右输出拖拽创建
- **titanX 需求**：从节点 handle 拖拽创建新节点
- **React Flow 支持**：✅ 可通过 `onConnectEnd` 实现
- **需要自己做**：判断是否连接到现有节点、创建菜单

### 5.4 单节点右键菜单
- **titanX 需求**：右键节点显示菜单
- **React Flow 支持**：✅ `onNodeContextMenu` 原生支持
- **需要自己做**：菜单组件、定位逻辑、防超出屏幕

### 5.5 多选快捷栏
- **titanX 需求**：框选多个节点后显示工具条
- **React Flow 支持**：⚠️ 需要自己实现
- **需要自己做**：监听 `onSelectionChange`、计算位置、渲染浮层

### 5.6 打组/解组
- **titanX 需求**：框选后打组、选中组后解组
- **React Flow 支持**：✅ `parentId` 原生支持
- **需要自己做**：打组逻辑、解组逻辑、节点排序

### 5.7 画布右键菜单
- **titanX 需求**：右键空白处显示菜单
- **React Flow 支持**：✅ `onPaneContextMenu` 原生支持
- **需要自己做**：菜单组件、定位逻辑

### 5.8 撤消/重做
- **titanX 需求**：支持撤消/重做
- **React Flow 支持**：❌ 不提供内置 undo/redo
- **需要自己做**：历史栈、快照管理、恢复逻辑

### 5.9 焦点拾取模式
- **titanX 需求**：进入 picking mode，点击节点提取数据
- **React Flow 支持**：⚠️ 需要自己实现模式切换
- **需要自己做**：mode 状态机、提示 UI、交互禁用/启用

### 5.10 点击空白关闭编辑器
- **titanX 需求**：点击画布空白处关闭当前编辑器
- **React Flow 支持**：✅ `onPaneClick` 原生支持
- **需要自己做**：编辑器状态管理
- **已知坑**：`selectionOnDrag` 会阻止事件（v12.9.0 bug）

### 5.11 节点下方编辑框
- **titanX 需求**：选中节点后下方出现编辑框
- **React Flow 支持**：⚠️ 需要自己实现
- **需要自己做**：编辑框组件、定位逻辑、viewport 跟随

---

## 6. 总结

### 6.1 React Flow 原生支持的能力
- ✅ Group node（`parentId`）
- ✅ 节点/画布右键事件
- ✅ 坐标转换（`screenToFlowPosition` / `flowToScreenPosition`）
- ✅ 单节点工具条（`NodeToolbar`）
- ✅ 点击空白事件（`onPaneClick`）
- ✅ Viewport 事件（`onMove` 等）
- ✅ 交互配置（`panOnDrag` / `selectionOnDrag` 等）

### 6.2 需要自己包装的能力
- ⚠️ 右键菜单组件
- ⚠️ 多选工具条
- ⚠️ 打组/解组逻辑
- ⚠️ Picking mode 状态机
- ⚠️ 节点下方编辑框
- ⚠️ 撤消/重做
- ⚠️ 节点工厂
- ⚠️ 创建菜单

### 6.3 已知风险点
- ⚠️ `selectionOnDrag` 阻止 `onPaneClick`（v12.9.0 bug）
- ⚠️ 节点数组顺序要求（父节点必须在前）
- ⚠️ 自定义浮层不自动跟随 viewport
- ⚠️ 坐标系转换容易混淆

### 6.4 titanX v1 建议
- ✅ 可以基于 React Flow 实现所有已确认交互
- ⚠️ 需要自己实现约 50% 的交互逻辑
- ⚠️ 建议先实现核心交互，高级功能（lasso、undo/redo）可 P1
- ⚠️ 需要建立统一的状态管理层（flowStore）
- ⚠️ 需要建立统一的命令层（canvasCommands）

---

## 7. 参考资料

### 7.1 官方文档
- https://reactflow.dev/
- https://reactflow.dev/api-reference/react-flow
- https://reactflow.dev/api-reference/types/react-flow-instance
- https://reactflow.dev/learn/layouting/sub-flows
- https://reactflow.dev/learn/concepts/the-viewport

### 7.2 官方示例
- https://reactflow.dev/examples/interaction/context-menu
- https://reactflow.dev/examples/nodes/node-toolbar
- https://reactflow.dev/examples/grouping/selection-grouping
- https://reactflow.dev/examples/grouping/sub-flows
- https://reactflow.dev/examples/whiteboard/lasso-selection
- https://reactflow.dev/examples/interaction/interaction-props

### 7.3 已知问题
- https://github.com/xyflow/xyflow/issues/5563
