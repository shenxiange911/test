# 08_ACCEPTANCE_CHECKLIST

## A. 安全

- [ ] KIE API Key 仅存在服务端
- [ ] 前端代码中没有 `api.kie.ai`
- [ ] webhook 已做 HMAC 验签
- [ ] 保存本地必须经过服务端
- [ ] 上传文件类型已校验

## B. React Flow

- [ ] 使用受控模式
- [ ] `nodes` / `edges` 在外部状态管理
- [ ] `nodeTypes` 已集中注册
- [ ] 手动连线可用
- [ ] 自动连线可用
- [ ] 非法连线会被拦截

## C. KIE 创建任务

- [ ] gpt4o-image 可创建任务
- [ ] flux-kontext 可创建任务
- [ ] runway-video 可创建任务
- [ ] veo31-video 可创建任务
- [ ] suno-audio 可创建任务
- [ ] market-generic 可创建任务

## D. 结果查询

- [ ] callback 可收
- [ ] polling 可补偿
- [ ] taskId 会持久化
- [ ] detail endpoint 可查询
- [ ] 失败任务会写 errorMessage

## E. UI 展示

- [ ] 图片能显示
- [ ] 视频能播放
- [ ] 音频能播放
- [ ] 失败状态有提示
- [ ] refresh 能更新现有任务
- [ ] regenerate 会创建新任务
- [ ] save local 可落盘

## F. 本地保存

- [ ] 能下载图片到本地
- [ ] 能下载视频到本地
- [ ] 能下载音频到本地
- [ ] 存储路径按 workflow/node/run 组织
- [ ] localPath 会写回 runtime

## G. OpenClaw 自动化

- [ ] 能自动创建 5 个初始节点
- [ ] 能自动连线 text -> image/video/audio
- [ ] 能根据 family 生成 payload
- [ ] 没有 registry 的模型不会乱猜
