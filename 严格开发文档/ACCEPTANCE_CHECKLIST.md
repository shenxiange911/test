# ACCEPTANCE_CHECKLIST.md

> ⚠️ 当前阶段以**浏览器产品行为验收**为最高标准。  
> `curl`、`build`、代码审查都只是辅助证据，不能替代浏览器中的真实产品行为。

## H. 一票否决项（先看这里）
以下任一项不满足，本轮直接判失败：
- [ ] 默认态仍是大表单节点
- [ ] 编辑区未在节点主体外部下方独立展开
- [ ] Text / Image 任一核心连接方向无法真实互联
- [ ] 点击 Generate 后没有真实返回图片并显示在节点中
- [ ] 只做代码结构验证，没有产品行为验证

---

## A. 当前阶段（v1）最小技术验收
- [ ] 使用 `@xyflow/react`
- [ ] 画布父容器有明确宽高
- [ ] 使用受控模式管理 `nodes/edges`
- [ ] TypeScript type-check 通过
- [ ] npm run build 通过

## B. 当前阶段（v1）UI 与交互验收
- [ ] TextNode 默认态不是完整长表单
- [ ] ImageNode 默认态不是完整长表单
- [ ] 默认态是紧凑缩略图 / 摘要卡片
- [ ] 点击节点缩略图后，编辑区在节点主体外部下方独立展开
- [ ] 点击空白处关闭编辑区
- [ ] 可以创建 Text / Image 节点
- [ ] 可以拖拽节点
- [ ] 可以手动连线
- [ ] 可以删除连线
- [ ] 可以删除节点
- [ ] 删除节点时不会残留孤立边

## C. 当前阶段（v1）互联与数据流验收
- [ ] Text -> Image 可连、可删、可传 upstream
- [ ] Image -> Image 可连、可删、可传 upstream
- [ ] Image -> Text 可连、可删、可传 upstream
- [ ] 输出按钮/输出锚点可创建下游节点
- [ ] 创建下游节点后自动建边成功
- [ ] 下游节点可见 upstream 文本输入
- [ ] 下游节点可见 upstream 图片输入
- [ ] 多上游汇入一个下游时聚合正确
- [ ] 删除后业务 ID 复用最小缺失编号

## D. 当前阶段（v1）执行闭环验收
- [ ] 执行前会编译最终 prompt
- [ ] Preview 改变后，执行输入也随之改变
- [ ] API 错误有 UI 呈现
- [ ] 节点运行状态可刷新
- [ ] Image Generate 点击后返回真实图片
- [ ] 返回图片真实显示在节点中
- [ ] 若生成失败，节点中可见明确错误信息
- [ ] 结果写回包含 prompt snapshot / compiledPromptHash
- [ ] runtime records 有明确写入出口

## E. 当前阶段（v1）报告要求
每个关键验收项必须明确标注：
- [ ] 已实测通过
- [ ] 仅代码审查通过
- [ ] 未验证

---

## F. 后续扩展 / 未来阶段（不是当前主线阻塞项）
- [ ] 模板保存 / 载入 / 合并模式选择
- [ ] 完整 template snapshot / template resolver
- [ ] skill binding 动态路由
- [ ] video / audio / result 全族节点落地
- [ ] run workflow / resultIndex / 更多 orchestration 能力
- [ ] 完整 lint / 单元测试体系
