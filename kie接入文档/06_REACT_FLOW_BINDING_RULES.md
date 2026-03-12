# 06_REACT_FLOW_BINDING_RULES

## 严格模式

必须使用 React Flow 受控模式。

最小结构：

```tsx
const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

<ReactFlow
  nodes={nodes}
  edges={edges}
  onNodesChange={onNodesChange}
  onEdgesChange={onEdgesChange}
  onConnect={onConnect}
  nodeTypes={nodeTypes}
/>
```

## 节点 data 推荐结构

```ts
type FlowNodeData = {
  title: string;
  config: Record<string, unknown>;
  runtime: NodeRuntime;
  upstream?: {
    text?: string;
    imageUrls?: string[];
    audioUrls?: string[];
    videoUrls?: string[];
  };
};
```

## 手动连接规则

允许：

- Text -> Image
- Text -> Video
- Text -> Audio
- Upload -> Image Editor
- Image -> Video
- Image -> Image Editor
- Audio -> Video
- Upload -> 任意媒体节点

不允许：

- Video -> Text
- Audio -> Text
- 任意节点自己连自己
- 同一个 sourceHandle -> 同一个 targetHandle 重复边（除非业务明确允许）

## 自动连接规则（给 OpenClaw）

OpenClaw 自动编排时输出 `FlowPatch`：

```ts
type FlowPatch = {
  addNodes?: Array<...>;
  addEdges?: Array<...>;
  updateNodes?: Array<...>;
  removeNodes?: string[];
  removeEdges?: string[];
};
```

应用流程：

1. 校验 patch schema
2. 校验节点类型是否支持
3. 校验连接规则
4. 只要 patch 有一条非法 edge，整个 patch 拒绝
5. 拒绝时返回精确错误原因

## 节点媒体展示规则

### Image Node
- 大图预览区
- 输出图缩略图
- 保存按钮
- 刷新按钮
- 重新生成按钮

### Video Node
- `video` 预览
- 如果有 poster，先显示 poster
- 成功后显示时长 / 分辨率

### Audio Node
- `audio controls`
- 如果 KIE 返回 cover image，可一起显示
- 显示 title / duration / tags

## UI 刷新规则

- 提交任务后立即设置 `runtime.status = queued`
- 收到 webhook / refresh 成功后再切到 `running | succeeded | failed`
- UI 不直接依赖 KIE 原始状态字符串
- 必须通过 adapter 映射到统一 runtime

## 必须支持的按钮

每个媒体节点至少有：

- Run
- Refresh
- Regenerate
- Save Local

不要省略。
