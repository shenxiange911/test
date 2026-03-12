# titanX 项目文档 · 画布交互与 React Flow 实现逻辑

记录时间：2026-03-11
定位：承接 titanX 画布层、分组层、节点创建层、连线层、菜单层的实现总线文档
状态：当前可作为 React Flow 落地主参考，后续新增画布规则优先回写本文件

---

## 1. 文档目的

这份文档不负责描述单个节点字段，而负责回答一个更底层的问题：

**基于 React Flow，titanX 当前已经确认的画布交互，应该如何实现，才能避免后面逻辑散落、重复造轮子、菜单/连线/打组各写一套。**

当前重点覆盖：
- 双击空白新建节点
- 上传附件自动识别节点类型
- 左输入 / 右输出拖拽创建
- 单节点右键菜单
- 多选快捷栏
- 打组 / 解组 / 整组执行 / 创建模板
- 画布右键菜单
- 撤消 / 重做

---

## 2. React Flow 官方能力怎么映射到 titanX

React Flow 官方真正适合 titanX 的能力，不是“现成菜单”，而是：
- 受控 `nodes / edges`
- `onNodesChange / onEdgesChange`
- `onConnect`
- selection 多选
- `parentId` / group node
- 自定义 node / edge
- 浮层 UI（自定义菜单、工具条、快捷栏）

也就是说：
- React Flow 负责画布和图结构
- titanX 自己负责业务交互层

---

## 3. 总体实现分层

当前建议固定拆成 6 层。

### 3.1 画布状态层 `flowStore`
统一维护：
- `nodes`
- `edges`
- `selectedNodeIds`
- `selectedGroupId`
- `contextMenu`
- `creationMenu`
- `pendingConnection`
- `canvasMode`
- `history`

推荐 `canvasMode`：
- `idle`
- `creating-from-canvas`
- `creating-from-output`
- `adding-context`
- `focus-pick`
- `grouping`

原则：
- 所有菜单、快捷栏、模式条都从统一状态生长
- 不在节点组件内部散落一堆局部开关

### 3.2 节点工厂层 `nodeFactory`
所有新建节点统一走同一个工厂：

```ts
createNode({
  type,
  position,
  sourceNodeId?,
  sourceHandle?,
  initialData?,
})
```

工厂必须统一做：
- 分配业务 ID，例如 `text-01` / `image-01`
- 生成 React Flow id
- 根据节点类型填默认 `data`
- 需要时自动建 edge

### 3.3 连线工厂层 `edgeFactory`
统一负责：
- `createEdge()`
- `validateConnection()`
- `createPendingConnection()`

不要让左输入、右输出、空白处拖拽建节点各自写边逻辑。

### 3.4 命令层 `canvasCommands`
统一管理画布命令：
- `undo`
- `redo`
- `paste`
- `upload`
- `addAsset`
- `deleteNode`
- `duplicateNode`
- `copyToClipboard`

### 3.5 分组命令层 `groupCommands`
统一管理：
- `groupSelection()`
- `ungroup(groupId)`
- `moveGroup(groupId)`
- `runGroup(groupId)`
- `createTemplateFromGroup(groupId)`

### 3.6 资产命令层 `assetCommands`
统一管理：
- `createAssetFromNode(nodeId)`
- `createAssetFromSelection(nodeIds)`
- `addSelectionToExistingAsset(nodeIds, assetId)`

---

## 4. 空白画布交互

### 4.1 双击空白新建节点
当前已确认：
- 双击画布空白处，可新建：
  - 文本
  - 图片
  - 视频
  - 音频
  - 图片编辑器

推荐实现：
- 监听 pane 双击
- 用 React Flow 坐标转换为 flow position
- 打开新建节点菜单
- 菜单选择后调用 `createNode()`

示意：

```ts
onPaneDoubleClick(event) => {
  const position = screenToFlowPosition({
    x: event.clientX,
    y: event.clientY,
  })

  openCreationMenu({
    mode: 'from-canvas',
    position,
    allowedTypes: ['text', 'image', 'video', 'audio', 'imageEditor'],
  })
}
```

### 4.2 画布空白处右键菜单
当前已确认菜单项：
- 上传
- 添加资产
- 添加节点
- 撤消
- 重做
- 粘贴

推荐实现：
- pane context menu 单独维护
- 不和节点右键菜单共用一套 actions

建议结构：

```ts
contextMenu = {
  kind: 'pane',
  position,
  actions: ['upload', 'addAsset', 'addNode', 'undo', 'redo', 'paste']
}
```

---

## 5. 上传附件自动识别节点类型

当前已确认：
- 上传附件后，系统会自动识别并归入对应节点类型

推荐实现：

### 5.1 先做附件类型识别
```ts
function detectAttachmentNodeType(file) {
  // image -> image
  // video -> video
  // audio -> audio
  // text/pdf -> text or analyze
}
```

### 5.2 再统一走节点工厂
```ts
const nodeType = detectAttachmentNodeType(file)
createNode({
  type: nodeType,
  position,
  initialData: { fileRef: file.id },
})
```

原则：
- 右键上传
- 拖拽上传
- 粘贴上传
都复用同一套识别逻辑

---

## 6. 左输入 / 右输出拖拽创建逻辑

这部分是 titanX 画布的核心，不适合直接套普通 `onConnect` 语义。

### 6.1 当前产品规则
- 左输入口：添加上下文
- 右输出口：引用当前节点生成下游
- 拖到空白区域后，不直接建边，而是先弹菜单
- 菜单选择后，系统自动建节点 + 自动建边

### 6.2 推荐状态结构
```ts
pendingConnection = {
  sourceNodeId,
  sourceHandle,
  side: 'left' | 'right',
  flowPosition,
}
```

### 6.3 标准流程
1. 从 handle 开始拖拽
2. drop 到空白区域
3. 记录 `pendingConnection`
4. 弹出创建菜单
5. 选择节点类型
6. `createNode()`
7. `createEdge()`

### 6.4 左右菜单必须分开
当前已确认：
- 左输入菜单：
  - 文本生成
  - 图片处理
- 右输出菜单：
  - 文本生成
  - 图片生成
  - 视频生成
  - 图片编辑器

所以不能写成一个固定菜单。

建议：

```ts
getAllowedNodeTypes({ nodeType, handleSide, nodeState })
```

---

## 7. 单节点右键菜单

当前已确认单节点右键菜单至少包含：
- 编辑
- 创建资产
- 复制
- 粘贴
- 副本
- 删除
- 复制到剪贴板

推荐实现：
- 节点右键菜单本质上是节点命令面板
- 所有动作统一走命令层，不要在 UI 里直接改状态

示意：
- `editNode(nodeId)`
- `createAssetFromNode(nodeId)`
- `duplicateNode(nodeId)`
- `deleteNode(nodeId)`
- `copyNodeToClipboard(nodeId)`

说明：
- `副本` = 画布内复制节点
- `复制到剪贴板` = 导出文本/引用/可分享内容

---

## 8. 多选与快捷栏

当前已确认：
- 按住鼠标拖动可框选多个节点
- 框选后会出现顶部快捷栏
- 当前至少有：
  - 上传
  - 创建资产
  - 打组

推荐实现：
- 利用 React Flow selection
- 当 `selectedNodeIds.length > 1` 时，显示 floating toolbar

```ts
const multiSelectionActive = selectedNodeIds.length > 1
```

原则：
- 多选不是视觉状态
- 多选是一等命令入口
- 多选态和单节点态应进入不同命令面板，不要共用同一菜单模型

### 8.1 创建资产 / 添加到现有资产
当前截图已确认：
- `创建资产` 与 `添加到现有资产` 是两个独立面板流程
- `添加到现有资产` 面板当前至少包含：
  - tab：`创建资产` / `添加到现有资产`
  - 分类筛选：`全部 / 人物 / 场景 / 物品 / 风格 / 音效 / 其他`
  - 结果列表区
  - `添加` 按钮
- `创建资产` 面板当前至少包含：
  - 封面预览
  - 名称输入
  - 分类下拉
  - `创建` 按钮

推荐实现：
- 多选快捷栏里的 `创建资产` 统一打开资产面板
- 资产面板内部再切 `创建资产` / `添加到现有资产`
- 两个流程共用同一份 selection payload，而不是各自重新抓取选中节点

---

## 9. 打组逻辑

### 9.1 当前已确认的组能力
- 多选后支持打组
- 打组有组颜色
- 打组有组布局
- 打组可整组执行
- 打组可创建模板
- 打组可解组
- 打组时仍可操作组内单节点
- 选中组框空白处可整组移动

### 9.2 组不是纯视觉框
组当前已经确认有 4 重语义：
- 工作流逻辑单元
- 模板保存单元
- 批量移动单元
- 可执行单元

### 9.3 React Flow 推荐落法
不要只画一个框。
推荐用：
- group node
- child node with `parentId`

也就是：
- 新建一个 `group` 节点
- 把子节点改成该 group 的 children
- 子节点位置转成相对坐标

这样天然支持：
- 整组移动
- 组内单节点继续操作
- 解组时再恢复

### 9.4 组数据建议
```ts
interface GroupNodeData {
  bizId: string
  title: string
  colorToken?: string
  layout?: 'grid' | 'horizontal'
  executable?: boolean
  templateable?: boolean
}
```

### 9.5 当前已确认的组颜色与布局
- 组颜色入口：顶部最左侧颜色圆点
- 点击后：弹出背景颜色面板
- 布局当前至少支持：
  - 宫格布局
  - 水平布局

### 9.6 当前已确认的组级快捷栏
至少包含：
- 整组执行
- 创建模板
- 解组

### 9.7 当前已确认的整组执行行为
- `整组执行` 是真实执行入口，不是占位按钮
- 如果组内包含未填写/未就绪节点，整组执行会失败
- 失败后会给出错误提示

---

## 10. 创建模板逻辑

当前已确认：
- 打组创建模板，本质上是打组保存工作流

推荐实现：
1. 读取 group 下全部 nodes / edges
2. 做业务 ID 去环境化
3. 保存相对布局、连接关系、节点 data
4. 写成 workflow template

```ts
createTemplateFromGroup(groupId) => {
  const childNodes = getGroupChildren(groupId)
  const childEdges = getEdgesWithinGroup(groupId)
  return serializeWorkflowTemplate(childNodes, childEdges)
}
```

重点：
- 模板不是截图
- 模板是可再次实例化的结构化工作流

---

## 11. 解组逻辑

推荐统一为命令：

```ts
ungroup(groupId)
```

逻辑：
- 把子节点从 group 释放出来
- 相对坐标转回画布绝对坐标
- 删除 group node

当前已确认：
- 解组后变回独立单节点

---

## 12. 撤消 / 重做

既然画布空白处右键菜单已经确认有：
- 撤消
- 重做

那主图状态必须可历史化。

推荐：

```ts
interface FlowSnapshot {
  nodes: Node[]
  edges: Edge[]
}
```

命令执行后：
- push snapshot
- undo
- redo

否则后面这些操作会很难维护：
- 打组
- 解组
- 批量创建资产
- 菜单创建节点
- 多选操作

---

## 13. 推荐工程模块拆分

### 13.1 `flowStore`
- nodes
- edges
- selection
- history
- menus
- modes

### 13.2 `nodeFactory`
- createNode
- duplicateNode
- detectAttachmentNodeType

### 13.3 `edgeFactory`
- createEdge
- validateConnection
- createPendingConnection

### 13.4 `canvasCommands`
- undo
- redo
- paste
- upload
- addAsset

### 13.5 `groupCommands`
- groupSelection
- ungroup
- moveGroup
- runGroup
- createTemplateFromGroup

### 13.6 `assetCommands`
- createAssetFromNode
- createAssetFromSelection
- addSelectionToExistingAsset

### 13.7 `menus`
- pane context menu
- node context menu
- multi-select toolbar
- group toolbar
- creation menu
- add-context menu

---

## 14. 最重要的工程结论

当前 titanX 画布层最不该重复写的有三样：

### 14.1 节点创建逻辑必须统一
以下入口都应走同一个 `createNode()`：
- 双击新建
- 右键添加节点
- 输出口拖拽创建
- 上传附件自动建节点

### 14.2 连线创建逻辑必须统一
以下行为都应走同一个 `pendingConnection -> createEdge()`：
- 左输入拖拽接入
- 右输出拖拽创建下游
- 菜单确认后自动连线

### 14.3 命令逻辑必须统一
以下入口都应走 command registry：
- 单节点右键菜单
- 多选快捷栏
- 打组快捷栏
- 画布右键菜单

否则后面一定会出现：
- 同一操作不同入口行为不一致
- 撤消重做失效
- 分组与复制逻辑互相打架

---

## 15. 与当前产品文档的关系

这份文档负责：
- 画布层实现总线
- React Flow 逻辑映射
- 交互落地方式

它不替代：
- 节点字段文档
- 节点 schema 文档
- provider contract 文档

推荐搭配查看：
- `titanX/项目文档/01_总开发主文档.md`
- `titanX/项目文档/字段确认/2026-03-11_01_中间功能.md`
- `titanX/项目文档/10_图片节点整合总表_2026-03-11.md`

---

## 16. 当前新增确认 · 视频节点相关画布命令

这轮视频节点补图后，画布层还应追加 3 条实现规则：

### 16.1 视频快照必须是“节点派生命令”
当前已确认：
- 视频节点底部存在快照按钮
- 点击后按当前播放/暂停时刻截图
- 结果直接生成新的图片节点
- 新图片节点与普通图片节点能力一致

推荐实现：
```ts
createImageSnapshotFromVideo({
  sourceVideoNodeId,
  captureTimeMs,
  imageAssetRef,
})
```

要求：
- 统一走 `createNode({ type: 'image' })`
- 自动在源视频节点与新图片节点之间建 edge
- 图片节点写回来源元数据，例如 `sourceVideoNodeId` 与 `captureTimeMs`

### 16.2 视频高清必须是“自动派生增强节点”
当前已确认：
- 点击 `高清` 后，不是原地改当前节点
- 而是自动创建并连接一个视频增强节点
- 增强节点带独立参数区和独立输出口

推荐实现：
```ts
deriveVideoEnhanceNode({
  sourceVideoNodeId,
  position,
})
```

要求：
- 自动创建新节点
- 自动创建 edge
- 下游连接白名单限制为：`text`、`video`
- 所谓视频编辑节点，当前先按 `video` 节点族处理

### 16.3 视频解析结果应先按“结构化结果 + 独立结果框”落地
当前已确认：
- `解析` 会产出镜头级分析结果
- 结果存在 `详细分析列表` 与 `创意图缩略图` 两种视图
- 解析结果会以画布上的独立结果框形式出现
- 该结果框可拖拽、可缩放，内部同时承载图片与文字
- 当前产品还不能直接拆成一组可继续链接的镜头节点

所以第一阶段推荐：
- 先把解析结果写回当前视频节点的结构化字段
- 再生成一个独立的 analysis result panel node / floating panel
- 视图切换只是这些结构化结果的两种展示方式
- 暂不直接自动拆成镜头子节点

建议字段：
```ts
videoAnalysisResult = {
  shots: [],
  viewMode: 'detail-list' | 'creative-thumbnails',
}
```

建议 UI 容器：
```ts
createAnalysisResultPanel({
  sourceVideoNodeId,
  position,
  width,
  height,
})
```

后续再扩：
- `splitShotsToImageNodes()`
- `groupShotsAsStoryboard()`
- `copyShotSummary(shotId)`
- `copyShotPrompt(shotId)`
- `copyShotImage(shotId)`

## 17. 当前最值得优先实现的画布主链路

建议第一阶段先做通：
1. 双击空白新建节点
2. 上传附件自动识别节点
3. 左输入 / 右输出拖拽建节点
4. 单节点右键菜单
5. 多选快捷栏
6. 打组 / 解组 / 整组移动
7. 创建模板
8. 撤消 / 重做
9. 视频节点快照派生图片节点
10. 视频节点高清派生增强节点

然后再补：
- 整组执行的完整 runtime 写回
- 组布局自动排版
- 更强的资产系统整合
- 视频解析结果自动拆镜头节点 / 自动打组
