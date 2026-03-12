# AI_CODING_RULES.md

本文件是 OpenClaw 的最高优先级开发规则。

## 强制要求
- 必须使用 TypeScript
- 必须使用 React 函数组件与 Hooks
- 必须使用 `@xyflow/react`
- 必须使用受控模式：`nodes`, `edges`, `onNodesChange`, `onEdgesChange`, `onConnect`
- 必须为每个节点类型定义 schema、默认值工厂、UI 组件、执行器映射
- 必须为所有 API 入参和回参定义类型
- 必须有 `idle | running | success | error` 四态
- 必须支持手动连线与自动连线两种模式
- 必须保留用户手动修改的优先权，自动编排不得覆盖用户显式编辑内容，除非用户确认

## 禁止项
- 禁止使用旧包名 `react-flow-renderer`
- 禁止在节点组件内部直接裸写 `fetch`
- 禁止把 nodes / edges / selection / viewport 拆成多个相互冲突的数据源
- 禁止使用 `any`
- 禁止单文件堆积全部业务逻辑
- 禁止跳过连接校验直接插入非法边
- 禁止未经过 schema 校验就把 OpenClaw 输出写入画布
- 禁止在 render 阶段创建大对象或闭包导致高频重渲染

## 输出要求
每次生成代码时，OpenClaw 必须同时输出：
1. 变更文件列表
2. 数据结构说明
3. 手动模式说明
4. 自动模式说明
5. 风险点与待验证项

## 实现策略
- React Flow 视图层只负责渲染与交互
- Flow store 负责 nodes / edges / selection / history / orchestration state
- API client 负责所有网络请求
- Orchestrator 负责把用户任务转成 flow patch
- Validator 负责校验自动生成的节点和连线是否合法
