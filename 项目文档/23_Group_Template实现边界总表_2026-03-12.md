# titanX Group / Template 实现边界总表

记录时间：2026-03-12
状态：正式整合稿
适用范围：titanX 当前 Manual-first Baseline 阶段
专题目标：冻结 Group / Template / 父子关系在 v1 的实现边界，避免后续把“多选 / 打组 / 模板 / 整组执行”混成一团

---

## 1. 推荐实现模型

### 1.1 结论先说
**titanX 的 Group 应采用“parent-child 为底层 + 视觉框为表现 + group metadata 为业务层”的混合模型。**

不能选下面两种极端方案：

#### A. 不推荐：纯视觉框模型
如果 Group 只是一个画在外面的框：
- 整组移动需要手动同步所有子节点坐标
- 解组时没有天然父子关系可拆
- 创建模板时还要再次推断“哪些节点属于这个框”
- 后面接整组执行时也没有稳定 group identity

这条路短期看简单，长期返工最大。

#### B. 也不推荐：把 React Flow parent-child 直接当完整业务模型
React Flow 的 `group + parent-child` 只解决：
- 相对定位
- 父移动时子跟随
- 子节点仍是独立节点

它并不自动提供：
- 组颜色
- 组布局
- 创建模板
- 整组执行
- 组级业务校验

所以不能把 React Flow 原生 group 直接当 titanX 的完整 Group 语义。

### 1.2 正确分层

#### 底层结构层
使用：
- `group node`
- child node 挂到 group
- 子节点保留正常 node 行为

这一层负责：
- 整组移动
- 子节点相对布局
- 解组时的坐标还原基础

#### 交互表现层
Group 在 UI 上表现为：
- 可见的组框
- 有颜色
- 有标题
- 有组级 toolbar
- 点击组框空白处可整组选中/移动

这一层负责：
- 用户把它认知成“一个组”
- 与普通多选区分开

#### 业务语义层
Group 额外承载 titanX 业务字段：
- `groupId`
- `title`
- `color`
- `layout`
- `templateable`
- `executable`
- 后续可扩的执行态字段

这一层负责：
- 创建模板
- 整组执行入口
- 与 titanX schema / command 层对齐

---

## 2. v1 可做 / 需包装 / 后推

### 2.1 可直接做
这些能力建议纳入 titanX v1：

#### 1) 多选后显式打组
- 输入：当前 selection nodes
- 动作：创建 group，对选中节点建立父子关系
- 输出：一个持久化 group 实例

#### 2) 整组移动
- 选中组框空白处拖动 group
- 组内 child 一起移动
- 这是 v1 最值得做、且最符合 React Flow 原生能力的一项

#### 3) 解组
- 从 group 中释放 child nodes
- child 恢复画布绝对坐标
- 删除 group node

#### 4) 组内单节点继续操作
- 组内节点仍可被单独选中
- 仍可打开各自 Inspector / 编辑区
- 仍可继续连下游
- 这是 titanX 当前文档已经明确要求的能力

#### 5) 从 group 创建模板
- 只允许从已存在的 group 触发
- 读取 group 内 nodes / edges / 相对布局
- 序列化为局部工作流模板

#### 6) 基础组颜色与布局入口
v1 至少保留并落地：
- 颜色
- 布局：`grid` / `horizontal`

其中布局第一版可以先是最小能力，不必马上上复杂自动排布引擎。

### 2.2 需要包装后做
这些能力适合进入 v1.x / P1，但不要裸接：

#### 1) Group 业务字段层
需要在 group node data 之外补一层业务字段规范，避免后面模板和执行状态塞乱。

#### 2) Template 序列化层
模板不能直接保存当前画布对象原样，需要包装：
- 去掉 selected / dragging / runtime polling 等实例态字段
- 节点位置转成模板基准相对坐标
- group 自身的实例 id 不直接污染模板定义

#### 3) Group toolbar 与多选 toolbar 分离
必须明确：
- 多选态 toolbar
- 组选中态 toolbar

不要共用一套菜单模型，否则后面命令边界会混。

#### 4) 整组执行前校验
现有文档已明确“组内未就绪节点会执行失败”。
但 v1 更稳妥的落法是：
- 先做 preflight 检查
- 给出失败原因
- 不要一上来就做复杂组级调度器

### 2.3 不建议放进 v1
这些能力当前不建议进 titanX v1：

#### 1) 自动吸附进组
包括：
- 节点拖到 group 上自动挂 child
- 拖出 group 自动 detach

这套逻辑的主要复杂度不在 UI，而在：
- absolute / relative 坐标换算
- hover 命中判定
- undo / redo
- 边重算

#### 2) 任意框选直接创建模板（不经过 group）
这会让“多选”和“Group”职责重叠，后面一定出现两套导出逻辑。

#### 3) 嵌套 group
会放大：
- 坐标换算
- z-index
- toolbar 焦点
- 模板导出
- 组执行边界

#### 4) 高级自动布局引擎
比如：
- 自动避让
- 智能收缩包裹
- 复杂宫格自适配
- 内容驱动尺寸回流

#### 5) 完整组级执行编排器
当前阶段只需要“整组执行入口 + 就绪校验 + 失败提示”，不需要在 v1 做成平台级 workflow scheduler。

---

## 3. Group 与 Template 的边界

### 3.1 核心定义

#### Group
Group 是**当前画布中的局部工作流实例对象**。

它强调：
- 正在编辑
- 可以拖动
- 可以解组
- 保留当前局部结构
- 是当前画布实例的一部分

#### Template
Template 是**从 Group 派生出来的可复用结构定义**。

它强调：
- 被保存
- 可复用
- 可再次实例化
- 不绑定当前画布实例 id

### 3.2 必须冻结的关系

#### Group 不是 Template
不能把一个组天然当作模板。
原因：
- 很多组只是临时整理，不一定要沉淀
- 组里可能还带当前实例态数据
- 组的存在是编辑行为，不一定是资产行为

#### Template 也不是当前 Group 的“实时镜像”
模板一旦生成，应该是单独的定义对象。
后续组再修改，不应默认同步改写模板。

#### 正确关系
**Template 从 Group 派生生成。**

即：
- 先有 group
- 再显式点击“创建模板”
- 系统导出结构化模板

### 3.3 titanX 语义下的最小边界
在 titanX 当前语义里：
- Group = 打组后的局部工作流
- Template = 从打组结果沉淀出的可复用局部工作流模板

这里的模板不是后端工作流平台那种抽象 DSL 容器，而是：
- 局部节点集合
- 局部连线关系
- 局部默认布局
- 可再次实例化到画布的“工作块”

---

## 4. 与当前 titanX 文档规则的兼容性

### 4.1 与 `01_总开发主文档.md` 的兼容性
本方案与已确认主文档完全一致：
- 支持打组
- 支持整组移动
- 支持解组
- 支持组内单节点继续操作
- 支持创建模板
- 保持 Manual-first，不提前扩成自动化平台级编排

### 4.2 与 `11_画布交互与ReactFlow实现逻辑.md` 的兼容性
这份文档已经建议：
- 用 `group node + child node with parent relation`
- 把 groupCommands 单独抽层
- 统一处理 `groupSelection / ungroup / runGroup / createTemplateFromGroup`

本次整合稿延续这个方向，但更进一步补了边界：
- Group 不是纯视觉框
- Group 也不等于 Template
- Template 应只从 Group 派生

### 4.3 与 `14_统一字段Schema总表_2026-03-11.md` 的兼容性
当前 draft schema 仍可继续使用，但应理解为 v1 minimum schema：

建议维持：
```ts
interface NodeGroupDraft {
  groupId: string
  nodeIds: string[]
  edgeIds: string[]
  color?: string
  layout?: 'grid' | 'horizontal'
}

interface WorkflowTemplateDraft {
  templateId: string
  name: string
  nodeIds: string[]
  edgeIds: string[]
  nodePositions?: Record<string, { x: number; y: number }>
  groupIds?: string[]
}
```

但要加一条解释：
- GroupDraft 是当前实例态的组描述
- WorkflowTemplateDraft 是导出后的复用定义草稿
- 两者不能混用

### 4.4 与当前代码现实的兼容性
当前 `app/src/App.jsx` 仍是 prototype，尚未有 flowStore / groupCommands / template serialize。
因此本方案刻意选择：
- 先做显式打组
- 先做显式解组
- 先做显式从 group 创建模板
- 不把复杂自动吸附进组压进 v1

这和当前代码成熟度匹配，返工最少。

---

## 5. 推荐最小实现方案

### 5.1 v1 的最小闭环
建议把 Group / Template v1 固定成下面这条链：

#### Step 1：多选节点
- 利用 React Flow 现有 selection
- 进入多选 toolbar

#### Step 2：点击“打组”
系统做这些事：
- 新建一个 group node
- 计算 group 覆盖范围
- 把被选中的 nodes 变成 child
- 子节点坐标改成相对 group 坐标
- 写入 group data：`title / color / layout`

#### Step 3：组成为独立业务对象
组级 toolbar 至少有：
- `整组执行`
- `创建模板`
- `解组`

#### Step 4：允许两种组内交互并存
- 点击 group 空白区域：选中整个 group / 整组拖动
- 点击 child 节点：操作单节点

#### Step 5：创建模板
只允许从 group 触发：
- 读取 group 下 nodes / edges
- 去实例态字段
- 保存相对布局
- 生成 template draft

#### Step 6：解组
- child 坐标还原为画布绝对坐标
- 移除 parent relation
- 删除 group node

### 5.2 v1 最小数据建议

#### Group node data
```ts
interface GroupNodeData {
  groupId: string
  title: string
  color?: string
  layout?: 'grid' | 'horizontal'
  executable?: boolean
  templateable?: boolean
}
```

#### Template payload（最小版）
```ts
interface WorkflowTemplateDraft {
  templateId: string
  name: string
  sourceGroupId?: string
  nodePositions: Record<string, { x: number; y: number }>
  nodes: Array<{
    nodeType: string
    data: unknown
  }>
  edges: Array<{
    source: string
    target: string
    sourceHandle?: string
    targetHandle?: string
  }>
}
```

注意：
- `sourceGroupId` 仅作来源追踪，不代表模板继续绑定当前 group
- 模板里不应继续保存当前运行时状态、selected 状态、polling 状态

### 5.3 v1 命令层建议
建议在画布命令体系中单独固定：
- `groupSelection()`
- `ungroup(groupId)`
- `runGroup(groupId)`
- `createTemplateFromGroup(groupId)`

不要让这些逻辑散落在：
- toolbar 按钮内部
- group node 组件内部
- Inspector 内部

否则后面 undo/redo 和菜单多入口很容易打架。

---

## 6. 风险与返工点

### 6.1 最大风险：错误选型成纯视觉框
后果：
- 整组移动要自己维护所有子节点
- 模板导出时仍需额外做成员归属判断
- 解组没有天然父子关系可拆
- 后面补整组执行也缺 group identity

这是最该避免的返工点。

### 6.2 版本风险：当前代码依赖仍是 `reactflow@11.10.0`
而新的官方文档和口径已经转向：
- `@xyflow/react`
- `parentId`

因此正式落代码前必须先确认：
- 是先升级依赖
- 还是先按当前版本兼容实现

否则文档写 `parentId`，代码里实际还在旧口径，会直接造成实现偏差。

### 6.3 坐标换算风险
所有下列动作都依赖准确坐标转换：
- 打组
- 解组
- 组内拖动
- 后续拖入/拖出组

如果这层不集中封装，后面非常容易出现：
- child 位置偏移
- 解组后节点跳位
- undo 后错位

### 6.4 焦点与事件冲突风险
需要尽早冻结规则：
- 点击 group 空白区域
- 点击 child 节点
- 拖 group
- 拖 child

如果 group 遮罩处理不好，会出现：
- child 不能选中
- group 总是抢事件
- Inspector 和 toolbar 状态混乱

### 6.5 模板污染实例态风险
如果创建模板时直接保存当前画布 node JSON，容易把这些脏字段带进去：
- `selected`
- `dragging`
- 临时 runtime
- 当前结果态
- 局部 UI 展开态

模板必须经过净化和标准化，不能直接 dump 画布对象。

### 6.6 过早上高级自动行为的返工风险
这些能力都很诱人，但现在不适合 v1：
- 自动吸附进组
- 自动 detach
- 嵌套 group
- 智能布局
- 完整组执行编排器

如果现在硬上，会把 titanX 从 Manual-first 直接拖进“画布平台基础设施工程”，不划算。

---

## 7. 最终冻结结论

### 7.1 可直接做
- 多选后打组
- 整组移动
- 解组
- 组内单节点继续操作
- 从 group 创建模板
- 组颜色
- 基础组布局入口

### 7.2 需要包装后做
- Group 业务字段层
- Template 标准化序列化
- Group toolbar 与 selection toolbar 分离
- 整组执行前就绪校验

### 7.3 不建议放进 v1
- 自动吸附进组
- 任意 selection 直接模板化
- 嵌套 group
- 高级自动布局
- 完整组级执行编排器

### 7.4 推荐最小实现方案
**先把 Group 做成真正的局部工作流实例对象，再把 Template 作为从 Group 派生出来的复用结构。**

也就是：
- 多选只是临时操作态
- Group 才是持久化的画布业务对象
- Template 是从 Group 显式导出的复用定义

这条边界最符合 titanX 当前语义，也最不容易在 v1 后返工。
