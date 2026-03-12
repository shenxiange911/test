# 07_OPENCLAW_EXECUTION_RULES

## OpenClaw 的职责

OpenClaw 不是“自由发挥写代码”，而是按本规范执行。

它可以做：

- 创建节点
- 自动连线
- 选择默认 family
- 选择默认 model
- 根据节点类型构建 payload
- 生成后端 adapter
- 生成 React Flow UI 组件

它不能做：

- 猜测未知 KIE 参数
- 未经 registry 直接增加 modelKey
- 在前端直接调用 KIE
- 跳过 webhook 验签
- 绕过受控 React Flow 状态

## 每次写代码前必须检查

1. 当前节点类型是否在 registry 中定义
2. 当前 family 是否有 adapter
3. 当前 model 是否有官方 doc url
4. 当前节点所需字段是否能映射到 family payload
5. 当前结果是否有 normalizer
6. 当前节点是否支持 refresh / regenerate / save local

## OpenClaw 生成代码的顺序

1. 定义类型
2. 定义 schema
3. 定义 model registry
4. 定义 adapter
5. 定义 normalizer
6. 定义 workflow service
7. 定义 React Flow node UI
8. 接入按钮事件
9. 接入 refresh / regenerate / save local
10. 写测试 / checklist

## adapter 规则

每个 family 单独一个 adapter，不允许大一统 mega adapter。

例如：

- `gpt4oImageAdapter`
- `fluxKontextAdapter`
- `runwayVideoAdapter`
- `veo31VideoAdapter`
- `sunoAudioAdapter`
- `marketTaskAdapter`

## normalizer 规则

每个 family 单独 normalizer，返回统一结果结构：

- `normalizeGpt4oImageResult`
- `normalizeFluxKontextResult`
- `normalizeRunwayResult`
- `normalizeVeo31Result`
- `normalizeSunoResult`
- `normalizeMarketResult`

## polling 规则

- 创建任务后，如果没有 callback 或 callback 暂未到达，允许 polling
- polling 间隔建议：
  - 图片：10~15 秒
  - 视频：20~30 秒
  - 音频：15~20 秒
- 必须有最大轮询次数
- 到上限后状态转 `failed` 或 `timeout`

## webhook 幂等规则

重复 callback 不得重复创建文件，不得重复覆盖 run 记录。
处理流程必须幂等。
