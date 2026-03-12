# REACT_FLOW_OFFICIAL_NOTES.md

本项目必须遵守以下 React Flow 官方要点：
- `<ReactFlow />` 是核心组件，支持通过 `nodes`, `edges`, `onNodesChange`, `onEdgesChange`, `onConnect` 进行受控管理。
- `useNodesState()` / `useEdgesState()` 适合原型，生产中可结合更完善的状态管理方案。
- 自定义节点本质上是 React 组件，需要通过 `nodeTypes` 显式注册。
- `Handle` 是连接点，自动连线与手动连线都必须遵守 handle/connection 规则。
- 需要使用内部 hooks（如 `useReactFlow`）时，必须让相关组件位于 `ReactFlowProvider` 之下。
- React Flow 父容器必须有明确宽高，否则无法正常渲染。
- 自定义边可使用 `BaseEdge` 等构建，适合实现可删除边或自动边标记。
- 官方示例中存在基于距离的自动连线思路（proximity connect），可作为自动连线交互参考，但项目中的自动连线仍需通过业务规则校验。
