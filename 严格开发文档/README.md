# titanLX 严格开发文档

> 说明：本目录是 titanLX 的**主规范目录**。  
> 当前实现状态、未完成事实与一票否决项，请优先结合 `../项目文档/IMPLEMENTATION_REDLINES.md` 阅读。  
> 不要把本目录中的目标能力、完整 schema、长期规划误读成“当前代码已经全部实现”。

## 当前版本目标
基于 React Flow 构建 TitanLX 节点式工作流原型，严格对齐参考图与官方文档。

## 当前阶段最重要的产品目标
1. 节点默认态是紧凑缩略卡片，而不是长表单节点
2. 编辑区在节点主体外部下方独立展开，而不是节点主体继续拉长
3. Text -> Image / Image -> Image / Image -> Text 真实互联，upstream 真传递
4. 点击 Generate 后真实返回图片并显示在节点中

---

## 记忆锚点

### [ANCHOR-UI-001] 节点交互总原则
- 节点必须保持 **缩略图/摘要卡片常驻**。
- 只有当用户 **点击节点缩略图** 时，才在节点主体 **外部下方独立展开编辑区**。
- `selected` 状态不能直接作为编辑器开关。
- 点击画布空白处关闭当前编辑区。

### [ANCHOR-UI-002] Image Node 编辑区结构
- 选中并打开 Image Node 编辑区后，编辑区必须包含：
  - 模型型号（下拉）
  - 比例（下拉）
  - 大小（下拉）
  - 当前输入文本（textarea）
  - 上游图片输入预览
  - 上游文本输入预览
- 模型/比例/大小都属于编辑区内容，不属于默认卡片态。

### [ANCHOR-UI-003] Image Node 摄像机控制区
- 图片节点编辑区里必须包含“摄像机控制 / 相机控制”区域。
- 该区域属于 **节点下方独立展开编辑区** 的一部分，不是默认卡片态，不是节点外独立右侧面板。
- 当前阶段至少包含：
  - 摄像机型号
  - 镜头型号
- 可继续预留：
  - 焦段
  - 光圈

### [ANCHOR-DATA-001] 上下游数据绑定
- 下游节点输入不能是假数据。
- Image Node 必须通过 edges 真实读取上游节点输出：
  - 上游 Text Node → 注入文本
  - 上游 Image Node → 注入图片 URL
- 任何节点输入/输出显示，都必须来源于真实 node data 与 edge 关系。

### [ANCHOR-RUNTIME-001] 图片生成必须真实接 KIE
- 禁止再使用 mock 图、picsum、占位生成图冒充结果。
- Image Generate 必须走真实请求链。
- 成功后必须把结果 URL / 结果图写回 React Flow 节点 data。

### [ANCHOR-UX-001] 输出点新建节点规则
- 点击节点输出点/输出按钮时，弹出“新建节点”菜单。
- 新节点必须生成在 **鼠标附近**。
- 菜单至少支持当前可用下游类型。
- 新建后自动建立 edge。

### [ANCHOR-UI-004] 默认态必须是卡片态，不得回退成长表单态
- TextNode / ImageNode 默认态必须是紧凑缩略卡片/摘要卡片。
- 默认态不得直接展示完整编辑表单。
- 默认态不得直接展示参数区、长文本编辑器、完整 customPrompting、完整模板区。
- 如果默认态肉眼看上去仍然是“大表单节点”，视为未完成。

### [ANCHOR-UI-005] 编辑区必须是节点下方独立展开层
- 编辑区必须在节点主体 **外部下方独立展开**。
- 不能只是同一节点主体向下拉长。
- 必须肉眼一眼看出“缩略卡片”和“编辑区”是两层结构。

### [ANCHOR-DATA-002] 三种核心互联方向必须真实可用
- Text -> Image 必须真实可连、可删、可传 upstream。
- Image -> Image 必须真实可连、可删、可传 upstream。
- Image -> Text 必须真实可连、可删、可传 upstream。
- 不能只在代码中存在 handle / connectionRules 而没有产品行为验证。

### [ANCHOR-RUNTIME-002] Image Generate 最低可交付标准是节点中显示真实结果图
- 点击 Generate 后，必须发起真实请求。
- 成功时必须把真实返回图片显示在节点中。
- 失败时必须把明确错误信息显示在节点状态/节点内容中。
- 只有状态变化、没有结果图显示，不算完成。

### [ANCHOR-MODEL-001] 模型字段必须分层，禁止 agent 自发明字段
- 节点 UI / schema 层只能使用 titanLX 统一业务字段。
- KIE / provider 官方字段只能出现在 adapter / payload builder / server client。
- 新增模型前必须先补 `model-registry.ts` 与文档，不允许先在 UI 或 payload 里临时猜字段。
- 涉及字段治理时，主规范以 `严格开发文档/MODEL_PARAMETER_GOVERNANCE.md` 为准，KIE 细则以 `kie接入文档/11_FIELD_MAPPING_SOURCE_OF_TRUTH.md` 为准。

---

## 当前架构新增结论（2026-03-10）
### [ANCHOR-PROMPT-001] 每个可提示词节点都必须保留用户自定义注入层
- 该能力不是 UI 附加小输入框，而是正式 schema 字段。
- 手动输入与自动编排必须写入同一套 `customPrompting` 字段。
- 只要 `customPrompting.enabled === true` 且字段非空，执行前编译阶段必须强制并入最终 prompt。
- 禁止出现 UI 可编辑但 runtime 未实际使用的假接入。

### [ANCHOR-PROMPT-002] 模板系统属于节点正式能力，不是临时 prompt 收藏夹
- 模板保存的是节点 `operator-facing` 可复用配置，而不是运行时日志。
- 模板至少支持 `local`、`type`、`project` 三种作用域。
- 模板载入必须支持 `fill_empty`、`merge`、`replace` 三种合并模式。
- 模板与结果快照分离：模板用于复用，结果快照用于追踪本次执行证据。

### [ANCHOR-PROMPT-003] 编译提示词必须可预览、可写回、可追踪
- 节点编辑区应提供 `Compiled Prompt Preview` 只读视图。
- Analyze / Generate 之后应保留本次执行的 prompt snapshot / template snapshot / compiledPromptHash。
- 后续排查结果差异时，必须能追溯这次执行到底使用了哪些上游上下文、模板片段和用户自定义内容。

---

## 使用本目录时的阅读建议
- UI / 形态问题：优先读 `UI_DESIGN_RULES.md`
- 当前阶段验收：优先读 `ACCEPTANCE_CHECKLIST.md`
- Schema / 节点字段：优先读 `NODE_SCHEMA_SPEC.md`
- API / writeback：优先读 `API_CONTRACT.md`
- 模型参数字段治理：优先读 `MODEL_PARAMETER_GOVERNANCE.md`
- 当前实现事实与错误示范：回看 `../项目文档/IMPLEMENTATION_REDLINES.md`
