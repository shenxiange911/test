# 05_RESULT_BINDING_AND_LOCAL_SAVE

## 目标

把 KIE 返回的图片 / 视频 / 音频稳定地加载到 React Flow 节点 UI，并可靠保存到本地。

## 一、统一结果结构

```ts
type MediaResult =
  | {
      kind: 'image';
      remoteUrl: string;
      previewUrl: string;
      localPath?: string;
      mimeType?: string;
      expiresAt?: string;
    }
  | {
      kind: 'video';
      remoteUrl: string;
      previewUrl: string;
      posterUrl?: string;
      localPath?: string;
      mimeType?: string;
      expiresAt?: string;
    }
  | {
      kind: 'audio';
      remoteUrl: string;
      previewUrl: string;
      imageUrl?: string;
      localPath?: string;
      mimeType?: string;
      expiresAt?: string;
    };
```

## 二、不同 family 的结果解析

### gpt4o-image
优先读取：
- `response.resultUrls[]`

### flux-kontext
优先读取：
- `response.resultImageUrl`

### runway-video
优先读取：
- `data.videoInfo.videoUrl`
- `data.videoInfo.imageUrl` 作为封面

### veo31-video
优先读取：
- `data.info.resultUrls[]`
- 非 16:9 时额外读取 `originUrls[]`
- 读取 `resolution`

### suno-audio
优先读取：
- `response.sunoData[].audioUrl`
- `response.sunoData[].streamAudioUrl`
- `response.sunoData[].imageUrl`

## 三、前端如何绑定到节点 UI

每个节点 runtime 至少包含：

```ts
type NodeRuntime = {
  status: 'idle' | 'queued' | 'running' | 'succeeded' | 'failed' | 'saving' | 'saved';
  latestTaskId?: string;
  latestRunId?: string;
  error?: string | null;
  result?: MediaResult | null;
  updatedAt?: string;
};
```

React Flow 节点组件只读 `node.data.runtime.result`：

- Image Node -> `<img src={result.previewUrl} />`
- Video Node -> `<video src={result.previewUrl} controls />`
- Audio Node -> `<audio src={result.previewUrl} controls />`

## 四、刷新重新获取

### Refresh 的正确流程
1. 前端请求 `/api/workflows/node/:nodeId/refresh`
2. 后端取出 `latestTaskId`
3. 根据 family 调用对应的 detail endpoint
4. 如果完成，归一化并更新 runtime.result
5. 前端重新拉取 workflow 或更新 store

### Regenerate 的正确流程
1. 前端请求 `/api/workflows/node/:nodeId/regenerate`
2. 后端重新 build payload
3. 再次提交 create endpoint
4. 保存新 `taskId`
5. runtime.status -> `queued`

## 五、本地保存规则

### 必须走服务端，不走浏览器直存

原因：
- KIE 某些结果 URL 是临时的
- 4o 图片有专门的 download-url 解决跨域
- Common download-url 会生成短时有效直链
- 浏览器直接下载不稳定，也不利于权限控制

### 统一保存流程
1. 前端点击 Save Local
2. 调你自己的 `/api/workflows/node/:nodeId/save`
3. 后端读取 `node.runtime.result.remoteUrl`
4. 如需直链：
   - 4o 图：先调 `gpt4o-image/download-url`
   - 其他 KIE 结果：可调 `common/download-url`
5. 后端下载字节流
6. 存到本地：
   - `/storage/workflows/{workflowId}/{nodeId}/{runId}/...`
7. 写回 `localPath`
8. 节点 runtime.status -> `saved`

## 六、文件命名建议

```txt
storage/
  workflows/
    wf_001/
      image-1/
        run_001/
          result-1.png
      video-2/
        run_003/
          result-1.mp4
          poster-1.png
      audio-4/
        run_010/
          track-1.mp3
          cover-1.jpg
```

## 七、必须做的容错

- URL 过期 -> 自动重新查详情 / 重取 download-url
- webhook 丢失 -> polling 补偿
- 回调重复 -> 幂等处理
- 下载失败 -> 重试队列
- 保存成功但前端没刷到 -> 允许 Refresh 再同步
