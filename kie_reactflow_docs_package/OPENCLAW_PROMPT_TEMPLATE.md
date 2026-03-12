# OpenClaw 任务提示词模板（KIE + React Flow 项目）

你现在是这个项目的前端 / 全栈代码代理。  
你必须**严格遵守同目录下全部规范文档**，尤其是：

- `KIE_API_INTEGRATION_GUIDE.md`
- `MODEL_MATRIX.md`
- `REACT_FLOW_UI_BINDING.md`
- `STRICT_IMPLEMENTATION_RULES.md`

## 你的强制约束

1. 只能使用这些库：
- React
- TypeScript
- @xyflow/react
- Zod
- shadcn/ui
- 允许使用 TanStack Query（如果你需要）

2. 只能使用白名单模型 key：
- 见 `MODEL_MATRIX.md`

3. KIE API Key 绝不能出现在前端。

4. 你必须实现：
- 手动连线
- 自动连线 patch
- 节点运行
- 任务查询
- callback 验签
- 图片 / 视频 / 音频结果 UI
- 下载逻辑
- 服务端持久化保存逻辑接口

5. 你必须严格区分：
- Market API
- 4o Image API
- Flux Kontext API
- Runway API
- Veo API
- Suno API

6. 你必须先写：
- 类型
- schema
- model registry
- service client
- normalizer
- 然后才写 UI

## 本次任务

请根据这些文档，生成一个可运行的 React Flow 项目骨架，包含：

- Text Node
- Image Node
- Video Node
- Audio Node
- Upload Node
- 手动拖线
- 自动生成 FlowPatch
- KIE server adapters
- 结果面板
- 下载按钮
- callback webhook route

## 输出要求

- 分文件输出
- 先给目录树
- 再给每个文件完整代码
- 不允许省略号
- 不允许伪代码
- 代码必须可直接粘贴运行
