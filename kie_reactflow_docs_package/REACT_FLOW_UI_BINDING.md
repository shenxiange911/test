# KIE 结果如何绑定到 React Flow UI，并保存到本地

## 1. 节点 data 结构

每个节点都必须有统一 `data` 结构。

```ts
export type FlowNodeData = {
  title: string;
  provider?: "kie";
  modelKey?: string;
  runState: "idle" | "uploading" | "queued" | "generating" | "success" | "error";
  taskId?: string | null;
  error?: string | null;
  prompt?: string;
  uploads?: Array<{
    kind: "image" | "video" | "audio";
    source: "user" | "kie";
    originalName?: string;
    url: string;
    expiresAt?: string;
  }>;
  result?: {
    kind: "image" | "video" | "audio" | "text";
    urls?: string[];
    previewUrl?: string | null;
    resolution?: string;
    streamUrl?: string | null;
    coverImageUrl?: string | null;
    text?: string;
  } | null;
  providerMeta?: Record<string, unknown>;
};
```

## 2. 运行一个节点的标准流程

### 前端
1. 点击 Run
2. 更新本地节点状态：
```ts
runState = "queued"
```
3. 调你自己的后端：
```ts
POST /api/kie/run-node
```

### 后端
1. 校验节点 schema
2. 解析上游文本 / 上游素材
3. 如需要，先上传文件到 KIE
4. 提交任务到 KIE
5. 记录 `taskId`
6. 返回给前端

### 前端收到响应后
```ts
updateNodeData(nodeId, {
  runState: "generating",
  taskId: res.taskId,
  provider: "kie"
});
```

### 后端收到 callback 或轮询成功后
归一化结果并写回你自己的状态源。

### 前端再更新节点
```ts
updateNodeData(nodeId, {
  runState: "success",
  result: normalizedResult,
  error: null
});
```

## 3. 图片节点如何显示结果

```tsx
function ImageResultPanel({ data }: { data: FlowNodeData }) {
  if (data.runState === "generating") {
    return <div className="p-4 text-sm text-zinc-400">Generating image...</div>;
  }

  if (data.runState === "error") {
    return <div className="p-4 text-sm text-red-400">{data.error}</div>;
  }

  if (data.result?.kind !== "image" || !data.result.urls?.length) {
    return <div className="p-4 text-sm text-zinc-500">No image result</div>;
  }

  return (
    <div className="space-y-3">
      <img
        src={data.result.previewUrl || data.result.urls[0]}
        alt="result"
        className="h-44 w-full rounded-2xl object-cover"
      />
      <div className="flex gap-2">
        <button>Download</button>
        <button>Open</button>
      </div>
    </div>
  );
}
```

## 4. 视频节点如何显示结果

```tsx
function VideoResultPanel({ data }: { data: FlowNodeData }) {
  if (data.result?.kind !== "video" || !data.result.urls?.length) {
    return <div>No video result</div>;
  }

  return (
    <div className="space-y-3">
      <video
        src={data.result.previewUrl || data.result.urls[0]}
        controls
        className="h-52 w-full rounded-2xl object-cover"
      />
      <div className="text-xs text-zinc-400">
        {data.result.resolution || "unknown resolution"}
      </div>
      <div className="flex gap-2">
        <button>Download</button>
      </div>
    </div>
  );
}
```

## 5. 音频节点如何显示结果

```tsx
function AudioResultPanel({ data }: { data: FlowNodeData }) {
  if (data.result?.kind !== "audio" || !data.result.urls?.length) {
    return <div>No audio result</div>;
  }

  return (
    <div className="space-y-3">
      {data.result.coverImageUrl ? (
        <img
          src={data.result.coverImageUrl}
          alt="cover"
          className="h-36 w-full rounded-2xl object-cover"
        />
      ) : null}
      <audio src={data.result.streamUrl || data.result.urls[0]} controls className="w-full" />
      <div className="flex gap-2">
        <button>Download</button>
      </div>
    </div>
  );
}
```

## 6. 如何把 KIE 返回结果塞回 React Flow

推荐只通过一个函数更新：

```ts
type UpdateNodeData = (nodeId: string, patch: Partial<FlowNodeData>) => void;
```

不要在 8 个组件里各自乱改。

```ts
function applyKieTaskSuccess(
  updateNodeData: UpdateNodeData,
  nodeId: string,
  normalized: FlowNodeData["result"],
  taskId: string,
) {
  updateNodeData(nodeId, {
    runState: "success",
    taskId,
    result: normalized,
    error: null,
  });
}
```

## 7. 如何保存到“本地”

“保存到本地”要分三种含义：

### A. 保存到浏览器状态
适合：
- 刷新页面后恢复 UI
- 不适合保存二进制媒体本身

可以存：
- taskId
- result urls
- node config
- layout

推荐：
- localStorage（小）
- IndexedDB（大）

### B. 触发用户下载到电脑
适合：
- 用户手动保存图片 / 视频 / 音频

```ts
export async function downloadInBrowser(url: string, filename: string) {
  const res = await fetch(url);
  const blob = await res.blob();
  const objectUrl = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = objectUrl;
  a.download = filename;
  a.click();

  URL.revokeObjectURL(objectUrl);
}
```

### C. 服务端持久化保存（最推荐）
适合：
- 以后还能再次打开项目
- 给团队成员共享
- 不受 KIE 临时 URL 过期影响

后端流程：
1. 收到 KIE 成功结果
2. 如果是 KIE 内部 URL：
   - 可先调 `POST /api/v1/common/download-url`
3. 服务端再下载二进制
4. 存到：
   - 本地磁盘
   - S3
   - R2
   - OSS
5. 返回你的永久 URL 给前端

## 8. 一个真正可用的保存策略

### 规则
- 节点 UI 里显示的是 `result.previewUrl`
- 但数据库里还要保存：
  - `kieTaskId`
  - `originalTempUrl`
  - `persistedUrl`
  - `persistedAt`

### 例子
```ts
type PersistedMediaRef = {
  taskId: string;
  kind: "image" | "video" | "audio";
  originalTempUrl: string;
  persistedUrl: string;
  persistedAt: string;
};
```

## 9. React Flow + 自动刷新状态

推荐做法：

- 节点运行后：
  - `runState = "generating"`
- 如果用了 callback：
  - 前端每 2 秒拉你自己的任务接口
  - 一旦你后端任务状态变 success，就刷新节点
- 如果用户关闭页面再打开：
  - 从你自己的 DB 恢复 task / result / persistedUrl

## 10. 必须禁止的错误做法

1. 直接把 KIE 原始 JSON response 挂到节点上
2. 在 React 组件里写 KIE API key
3. 把临时 URL 当永久地址
4. 成功回调只改 UI，不落库
5. 每个节点自己发网络请求，不走统一服务层
