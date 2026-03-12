# titanX Group / Template / 父子关系专题调研过程

记录时间：2026-03-12
专题范围：仅验证 Group / Template / 父子关系，不扩散到其他画布功能
结论用途：为 titanX v1 决定“组”和“模板”的实现边界，而不是泛泛介绍 React Flow

---

## 1. 本次调研输入范围

### 1.1 已先读 titanX 正式文档
- `01_总开发主文档.md`
- `11_画布交互与ReactFlow实现逻辑.md`
- `14_统一字段Schema总表_2026-03-11.md`
- `15_视频模型与API映射总表_2026-03-11.md`
- `17_图片模型与API映射总表_2026-03-12.md`
- `18_文本分析模型与API映射总表_2026-03-12.md`
- `19_音频模型与API映射总表_2026-03-12.md`

### 1.2 只验证这些问题
- React Flow 里 group 更适合做视觉框、父子节点、还是混合模型
- 整组移动
- 解组
- 组内单节点继续操作
- 框选后创建模板
- Group 与普通多选的边界
- 哪些能力适合 v1，哪些应后推

### 1.3 代码现状检查
当前 titanX 前端并不是完整画布工程，而是一个 very early prototype：
- 依赖：`reactflow@11.10.0`
- 画布代码：`app/src/App.jsx`
- 现状只有：基础节点展示、点击画布创建节点、Inspector、StatusPanel
- 尚未落地：groupCommands / template serialize / 多选快捷栏 / 解组 / 自动吸附进组 / 组级 toolbar

这点很关键：本专题不能默认 titanX 已有组系统，只能按“现在要怎么设计最少返工”来定边界。

---

## 2. 官方能力定向验证结果

### 2.1 React Flow 对 sub flow / group 的真实底层语义
官方文档 `Sub Flows` 的关键信息：
- `parentId` 的作用首先是“相对父节点定位”
- child node 移动时位置是相对 parent
- parent 移动时 child 会一起移动
- 如果不设置 `extent: 'parent'`，child 仍可被拖出父框
- `group` type 只是一个方便用的 parent 容器节点，本质不是特殊业务工作流实体
- edges connected to child-in-parent 有单独的 z-index/render 行为

这说明：
1. React Flow 原生最适合承接“整组移动 + 子节点相对布局”
2. 但 React Flow 的 group 不是业务意义上的“模板”
3. `parentId` 只解决定位/移动，不自动提供“创建模板 / 组执行 / 解组菜单 / 组内规则”

### 2.2 Selection Grouping 示例透露的上层能力边界
官方 example 文案明确提到：
- 先选中多个节点
- 用 toolbar 的 Group Nodes 按钮分组
- 选中 group 后有 Ungroup 按钮
- group node 可 resize
- group node 会根据 child 自动调整尺寸

但要注意：
- 这是 example / pro capability 方向，不等于 titanX 当前必须照搬所有动态行为
- 它说明“多选 -> group node -> ungroup”这条技术路线可行
- 但并不自动满足 titanX 的“创建模板 / 整组执行 / 与业务 schema 对齐”

### 2.3 Parent Child Relation 示例透露的能力边界
搜索结果描述里明确提到：
- 可以把节点拖入 group 变成 child
- detach 按钮可解除父子关系
- 关键难点是 absolute position 和 parent-relative position 的换算

这说明：
- “拖进组即自动吸附”是可做的
- 但实现难点不在 UI，而在坐标换算、撤销重做、边关系稳定性
- 这部分不是 titanX v1 最小闭环必须项

---

## 3. 与 titanX 当前文档规则的对照

### 3.1 titanX 文档已经明确的产品语义
现有正式文档已把组定义成：
- 工作流逻辑单元
- 模板保存单元
- 批量移动单元
- 可执行单元

并明确要求：
- 打组后仍可继续操作组内单节点
- 选中组框空白处可整组移动
- 打组后支持创建模板
- 支持解组

这意味着 titanX 的 Group 绝对不能退化成纯视觉框。

### 3.2 但也不能把 Group 直接等同于 Template
原因：
- Group 是画布当前实例态
- Template 是从当前局部工作流提炼出来的“可再次实例化结构”
- Group 是编辑中对象
- Template 是序列化产物

所以：
- `Group != Template`
- 正确关系是：`Template 从 Group 派生生成`
- 同一组可以不保存成模板
- 模板也不该继续保留当前 groupId / nodeId 原值

### 3.3 与统一字段 Schema 的关系
当前 `14_统一字段Schema总表` 中：
- `NodeGroupDraft` 只有 `groupId / nodeIds / edgeIds / color / layout`
- `WorkflowTemplateDraft` 只有 `templateId / name / nodeIds / edgeIds / nodePositions / groupIds`

这说明目前 schema 还是 draft level，足够做 v1，但还不够支撑高级行为：
- 没有 group runtime status
- 没有 group compiled execution plan
- 没有 template version / source metadata
- 没有 child attach/detach audit fields

结论：
- v1 可以继续沿用 draft schema
- 但不要把“整组执行编排器”塞进第一版 group schema

---

## 4. 代码现状对实现边界的直接影响

### 4.1 当前前端不是“已有组系统待补”，而是“几乎从基础开始”
`app/src/App.jsx` 当前仅有：
- `useState(nodes)`
- `applyNodeChanges`
- 点击画布创建节点
- 节点选中后右侧 Inspector

尚未看到：
- `useEdgesState`
- 统一 flowStore
- 历史栈
- 多选工具栏
- 自定义 group node
- 模板序列化
- 节点工厂 / 边工厂 / groupCommands

因此：
- v1 不适合把“自动进组、动态包裹、自动适配尺寸、拖入拖出吸附”一起上
- 最小落地应该先是“显式打组 / 显式解组 / 显式创建模板”

### 4.2 版本风险：当前依赖是 `reactflow@11.10.0`
调研到的官方新文档里，`parentNode` 已更名为 `parentId`（11.11.0 后口径）。
但当前 titanX package 仍是：
- `reactflow@11.10.0`

这意味着：
- 写正式方案时要避免把新文档 API 名直接当作当前项目已可用事实
- 如果后续直接按 `parentId` 落代码，需先确认依赖升级路径或兼容写法

这个点必须写入风险项，否则后面容易文档先行、代码落地报错。

---

## 5. 针对问题逐项判断

### 5.1 group 更适合做视觉框、父子节点、还是混合模型
判断：**混合模型最合适。**

拆解：
- 只做视觉框：
  - 好处：简单
  - 问题：无法天然获得整组移动；组内节点坐标还是绝对坐标；解组/模板导出还要额外维护影子关系
- 只做 parent-child：
  - 好处：整组移动天然成立
  - 问题：业务上 group 的颜色、布局、创建模板、整组执行等仍需补一层组元数据
- 混合模型：
  - 底层用 `group node + child parent relation` 解决移动与相对布局
  - 上层再给 group 增加 titanX 自己的业务字段：颜色、布局、templateability、execution state

所以最终不是视觉框 or 父子二选一，而是：
- **底层结构选 parent-child**
- **表现层是视觉框**
- **业务层再附加 group metadata**

### 5.2 整组移动
判断：**可直接做。**

原因：
- 这是 React Flow parent-child 的天然强项
- 只要子节点挂到 group 下，移动 group 时 child 会一起动
- 这条能力对 v1 性价比很高，且符合现有 titanX 文档

前提：
- group 必须是真 group node / parent relation，不是只画框

### 5.3 解组
判断：**可直接做。**

实现逻辑：
- 读取 child nodes
- 把相对坐标换回画布绝对坐标
- 移除 `parentId`
- 删除 group node

难点：
- 坐标换算
- undo/redo
- 组内边保持稳定

但总体仍属于 v1 可控范围。

### 5.4 组内单节点继续操作
判断：**可直接做。**

原因：
- React Flow 的 child node 仍是正常 node，不是被焊死成 group 内不可编辑对象
- 只要不把 group UI 做成整块遮罩，就能继续选中 child、编辑、连接下游

需要产品约束：
- 点击 group 空白处 = 选中组并整组拖动
- 点击 child 本体 = 进入 child 的普通节点操作
- 两者焦点必须分离，否则很容易互相抢事件

### 5.5 框选后创建模板
判断：**需要包装后做。**

原因：
- React Flow 只负责 nodes/edges selection，不负责 template 概念
- titanX 的模板不是截图保存，而是局部工作流结构化导出
- 需要额外处理：
  - node/edge 过滤
  - 业务 ID 去实例化
  - 相对布局标准化
  - group metadata 序列化
  - 模板命名/分类/版本

更合理的路径：
- v1 先要求“先打组，再从 group 创建模板”
- 不建议 v1 直接支持“任意框选立即模板化但不打组”

原因很现实：
- 这样 Group 和 Template 的边界更清晰
- 也少一套“selection 模板导出”的平行逻辑

### 5.6 Group 与普通多选的边界
判断：必须严格区分，不能混。

建议边界：
- 多选 = 临时操作态
  - 用于创建资产 / 打组 / 批量删除 / 批量移动
  - 不持久化
  - 没有业务 ID
- Group = 持久化的局部工作流实例态
  - 有 groupId
  - 有颜色 / 布局 / toolbar
  - 可移动
  - 可解组
  - 可派生模板
  - 后续可承接整组执行

一句话：
- **多选是“选中方式”**
- **Group 是“业务对象”**

### 5.7 哪些能力适合 v1，哪些应后推

#### 可直接做
- 多选后打组
- group node + child relation
- 整组移动
- 组内单节点继续编辑/连接
- 解组
- 从 group 创建模板
- group 颜色
- group 两种布局入口（先支持字段和最小布局应用）

#### 需要包装后做
- group 自动 resize 贴合子节点
- 模板序列化规范化
- group toolbar 与普通 selection toolbar 分离
- 组执行前的就绪检查

#### 不建议放进 v1
- 拖拽节点进入组自动吸附成 child
- 组内自动重排布局引擎
- 任意框选即模板化且不经过 group
- 嵌套 group
- 组级编排执行器 / 并行调度 / 失败回滚
- 跨 group 智能裁剪边、自动重挂边

---

## 6. 推荐最小实现路线（过程判断）

### Phase A：先把组做成真正业务对象
- 多选节点
- 点击“打组”
- 创建一个 `group` 节点
- 子节点写入 parent relation
- group 保存 `color / layout / title`

### Phase B：先保证 3 个核心动作闭环
- 整组移动
- 组内单节点操作
- 解组

### Phase C：再把模板做成 group 的导出能力
- 仅允许从已存在的 group 创建模板
- 导出 group 内 nodes / edges / 相对布局 / 节点 data
- 去除实例态字段（selected / dragging / runtime polling）

这条路线的优点：
- 与 titanX 当前文档一致
- 与 React Flow 原生机制一致
- 与当前代码成熟度匹配
- 后面能平滑长成“整组执行”，不会因为 v1 先偷懒做纯视觉框而返工

---

## 7. 本轮最关键的踩坑提醒

### 7.1 最大误区：把 Group 当成纯视觉框
这样会导致：
- 整组移动要自己算一遍所有子节点位移
- 解组要维护影子关系
- 模板导出时还要重新判断哪些节点属于这个框
- 返工概率很高

### 7.2 第二个误区：把 Template 直接等同于 Group
这样会导致：
- 每个组都被迫模板化
- 画布实例态和模板定义态混在一起
- nodeId / groupId / runtime status 污染模板结构

### 7.3 第三个误区：v1 就上自动吸附进组
这类功能的复杂度集中在：
- 坐标换算
- hover 命中判断
- detach
- undo/redo
- 边的视觉反馈

对当前 titanX 代码成熟度来说，过早。

### 7.4 第四个误区：忽略版本口径
当前代码依赖是 `reactflow@11.10.0`，而最新文档很多地方已使用 `@xyflow/react` / `parentId` 新口径。
如果不先对齐依赖版本，文档方案和代码实现会出现 API 名错位。

---

## 8. 过程稿最终判断

### 8.1 可直接做
- 整组移动
- 解组
- 组内单节点继续操作
- 多选后显式打组
- 从 group 创建模板（第一版）

### 8.2 需要包装后做
- group 业务字段层
- template 序列化
- 组执行前校验
- group toolbar 与 selection toolbar 分离

### 8.3 不建议进 v1
- 自动吸附进组
- 嵌套 group
- 复杂自动布局
- 任意 selection 直接模板化
- 完整组级执行编排器

### 8.4 推荐模型
- **不是纯视觉框**
- **不是只靠多选态**
- **而是“parent-child 为底层 + 视觉框表现 + group metadata 业务层”的混合模型**

这也是本轮正式整合稿的主结论。
