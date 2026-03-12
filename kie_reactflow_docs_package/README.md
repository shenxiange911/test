# KIE API 接入规范包（React Flow / OpenClaw / TapNow-like 节点系统）

这个包是给 **AI 代码代理（例如 OpenClaw）** 直接喂食用的，目标是让它基于 **KIE 官方文档**，为你的 **React Flow 节点系统** 正确接入：
- 图片生成 / 图片编辑
- 视频生成
- 音频 / TTS / 音乐
- 上传文件
- 回调验签
- 统一查询任务
- 将结果绑定到 React Flow UI
- 下载 / 缓存 / 保存媒体到本地

## 目录

- `README.md`
- `KIE_API_INTEGRATION_GUIDE.md`
- `MODEL_MATRIX.md`
- `REACT_FLOW_UI_BINDING.md`
- `STRICT_IMPLEMENTATION_RULES.md`
- `OPENCLAW_PROMPT_TEMPLATE.md`
- `SOURCE_APPENDIX.md`
- `templates/kie.types.ts`
- `templates/kie.server.client.ts`
- `templates/kie.webhook.ts`
- `templates/kie.result.normalizer.ts`
- `templates/reactflow-kie-adapter.tsx`
- `templates/save-media.ts`

## 必须遵守的总原则

1. **浏览器端绝不直接调用 KIE API**
   - `Authorization: Bearer <KIE_API_KEY>` 只能放在服务端。
   - React Flow 前端只调用你自己的后端 `/api/kie/...`。

2. **React Flow 必须使用受控模式**
   - `nodes`
   - `edges`
   - `onNodesChange`
   - `onEdgesChange`
   - `onConnect`

3. **所有 KIE 结果先做统一归一化，再更新节点 UI**
   - 图片统一变成 `result.kind = "image"`
   - 视频统一变成 `result.kind = "video"`
   - 音频统一变成 `result.kind = "audio"`

4. **生产环境优先用 callback，不要只靠轮询**
   - 轮询只作为 fallback。
   - 回调必须做 HMAC 验签。

5. **生成结果要尽快缓存或下载**
   - Market 通用任务结果链接通常要尽快下载。
   - 4o / Flux / Suno 等也有各自保留期。
   - 不要把“临时 URL”当永久存储。

## 推荐技术栈

- React 18+
- TypeScript strict
- `@xyflow/react`
- Tailwind / shadcn/ui
- Zod
- TanStack Query（可选）
- Next.js Route Handlers / Node.js Express 任一服务端

## 你应该怎样喂给 OpenClaw

先把整个目录一次性喂给它，然后追加 `OPENCLAW_PROMPT_TEMPLATE.md` 里的任务提示词。

生成时间：2026-03-09
