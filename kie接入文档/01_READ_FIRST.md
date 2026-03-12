# 01_READ_FIRST

## 目标

本项目要做的是一个 **TapNow-like 媒体工作流节点系统**，前端采用 React Flow，
节点类型包含至少：

- Text Node
- Image Node
- Video Node
- Audio Node
- Image Editor Node
- Upload Node

每个节点都可以：

- 手动编辑参数
- 手动连线
- 被 OpenClaw 自动创建
- 被 OpenClaw 自动连接
- 独立运行
- 刷新 / 重新生成
- 在成功后把图片、视频、音频结果展示到节点 UI
- 在成功后保存到本地

## 绝对禁止

- 禁止把 KIE API Key 放到浏览器代码里
- 禁止前端直接调用 `https://api.kie.ai/...`
- 禁止把 KIE 返回地址直接当永久地址存数据库
- 禁止跳过 webhook 验签
- 禁止没有 schema 校验就把接口结果写入节点状态
- 禁止在节点 React 组件里直接写 `fetch('https://api.kie.ai/...')`
- 禁止把 React Flow `nodes` / `edges` 当作非受控内部状态黑盒处理

## 最小技术栈

- React + TypeScript
- `@xyflow/react`
- Node.js / Next.js API routes 或独立后端服务
- Zod 或同等级 schema 校验
- 后端持久化：本地磁盘 / 对象存储
- Webhook endpoint
- Polling fallback

## 最小后端职责

后端必须至少提供：

- 提交 KIE 任务
- 记录 `taskId`
- 接收 webhook
- 轮询补偿
- 下载生成结果
- 保存本地文件
- 更新工作流节点状态
