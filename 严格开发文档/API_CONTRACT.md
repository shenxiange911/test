# API_CONTRACT.md

> 说明：本文件描述 titanLX 的目标 API contract。  
> 当前阶段最关键的不是接口名多完整，而是：**浏览器里点击 Generate 后，节点中真实显示结果图**。  
> `curl` 或后端接口通，只能作为辅助证据，不能替代前端产品行为验收。

## 当前阶段（v1）最重要的接口闭环
### 图片生成闭环
最小闭环必须满足：
1. 前端点击 Generate
2. 发起真实图片生成请求
3. 返回任务状态 / 结果
4. 把结果写回节点
5. 节点中显示真实结果图

如果只有 API 返回 ok / taskId / url，但节点中没有显示真实结果图，当前阶段仍视为未完成。

---

## 1. 自动规划工作流
### POST /v1/orchestrations/plan
输入：
```json
{
  "goal": "做一个带配音的 15 秒产品短片",
  "mode": "hybrid"
}
```

## 2. 自动连线建议
### POST /v1/orchestrations/autowire

## 3. 节点执行
### POST /v1/nodes/run

## 4. 工作流执行
### POST /v1/workflows/run

## 5. 节点分析
### POST /v1/analyze/node

---

## 6. 图片生成（当前阶段重点）
### POST /v1/generate/image

### v1 阶段前端最关心的输入
```json
{
  "projectId": "tlx_demo_001",
  "nodeId": "image-01",
  "nodeType": "imageGenNode",
  "provider": "KIE",
  "prompt": "hero product on a studio surface",
  "compiledPrompt": "...",
  "compiledPromptHash": "sha256:...",
  "model": "nano-banana-2",
  "ratio": "16:9",
  "size": "1K",
  "upstreamText": ["..."],
  "inputImageUrls": ["..."],
  "params": {},
  "templateRefs": [],
  "customPrompting": {},
  "cameraParams": {},
  "skillBinding": {}
}
```

### v1 阶段前端最关心的返回
```json
{
  "ok": true,
  "taskId": "task_123",
  "status": "queued",
  "url": "https://.../image.png",
  "meta": {
    "provider": "kie",
    "model": "nano-banana-2"
  },
  "writeback": {
    "nodeId": "image-01",
    "compiledPromptHash": "sha256:...",
    "promptSnapshot": {
      "templateRefs": [],
      "customPromptingEnabled": true
    }
  }
}
```

### 当前阶段完成标准
不是“接口返回 ok”，而是：
- 节点进入正确状态
- 节点中显示真实返回图片
- 若失败，节点中显示明确错误

---

## 7. 视频生成
### POST /v1/generate/video

## 8. 音频生成
### POST /v1/generate/audio

## 9. 文件上传
### POST /v1/uploads

## 10. 运行时状态读取
### GET /v1/runtime/tasks/:taskId

## 11. 结果读取
### GET /v1/runtime/results/:taskId

### v1 阶段至少应返回
```json
{
  "ok": true,
  "taskId": "task_123",
  "status": "success",
  "artifacts": [
    {
      "kind": "image",
      "localPath": "projects/tlx_demo_001/nodes/image-01/output/result.png",
      "remoteUrl": "https://.../result.png"
    }
  ],
  "snapshots": {
    "promptSnapshot": {},
    "compiledPromptHash": "sha256:..."
  }
}
```

---

## 12. 模板与编译提示词
### POST /v1/templates/save
### POST /v1/templates/load
### POST /v1/nodes/compile-prompt

---

## 模型字段治理规则
- 节点/UI 层只允许使用统一业务字段，例如：`providerFamily`、`model`、`prompt`、`ratio`、`size`、`format`、`inputImages`、`enhance`、`translate`、`fallback`、`cameraParams`。
- payload builder / adapter 才负责把业务字段映射到官方 API 字段，例如：`filesUrl`、`aspectRatio`、`outputFormat`、`inputImage`、`isEnhance`、`enableFallback`、`enableTranslation`、`callBackUrl`。
- 新增模型必须先补 registry 与映射文档，禁止在 action / builder / component 中临时发明字段。
- 字段主规范见：`严格开发文档/MODEL_PARAMETER_GOVERNANCE.md`
- KIE 映射细则见：`kie接入文档/11_FIELD_MAPPING_SOURCE_OF_TRUTH.md`

## 错误格式
```json
{
  "ok": false,
  "code": "INVALID_CONNECTION",
  "message": "imageGenNode cannot connect to imageGenNode with semantic media_flow"
}
```
