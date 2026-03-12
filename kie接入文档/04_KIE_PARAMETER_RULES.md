# 04_KIE_PARAMETER_RULES

> 定位：本文件只负责记录 **family 参数细则与约束**。  
> 字段归属请看：`../严格开发文档/MODEL_PARAMETER_GOVERNANCE.md`  
> 字段映射职责请看：`11_FIELD_MAPPING_SOURCE_OF_TRUTH.md`

## 一、所有 KIE 接入的共同规则
- 认证统一使用 Bearer Token
- 任务创建成功只代表任务被接受，不代表已经生成成功
- 必须保存 `taskId`
- 必须支持 callback + polling
- 结果必须归一化后再写回节点 runtime

## 二、通用状态模型
前端统一状态：
- `idle`
- `queued`
- `running`
- `succeeded`
- `failed`
- `saving`
- `saved`

服务端统一状态：
- `TASK_CREATED`
- `WEBHOOK_RECEIVED`
- `POLLING`
- `RESULT_READY`
- `RESULT_DOWNLOADED`
- `RESULT_SAVED`
- `FAILED`

## 三、family 级参数规则
### A. gpt4o-image
推荐 UI 业务字段：
- `prompt`
- `ratio`
- `inputImages`
- `enhance`
- `fallback`

严格映射：
- `filesUrl <- inputImages`
- `prompt <- prompt`
- `size <- ratio`
- `callBackUrl <- callbackUrl`
- `isEnhance <- enhance`
- `uploadCn <- false`
- `enableFallback <- fallback`

### B. flux-kontext
推荐 UI 业务字段：
- `prompt`
- `ratio`
- `model`
- `format`
- `inputImages`
- `translate`

严格映射：
- `prompt`
- `aspectRatio`
- `model`
- `outputFormat`
- `inputImage`
- `enableTranslation`
- `callBackUrl`

规则：
- prompt 优先英文，或明确打开 translation
- 没有输入图就走 text-to-image
- 有输入图就走 edit

### C. market-image
统一路由：
- 创建任务：`/api/v1/jobs/createTask`
- 查询任务：`/api/v1/jobs/recordInfo`

规则：
- 所有具体模型必须通过 registry 定义
- 每个 registry 项必须给出：
  - `modelKey`
  - `inputBuilder`
  - `resultParser`
  - `officialDocUrl`
- OpenClaw 不得直接拼出未知模型 payload
- 如果 registry 里没有这个模型，先报错，不要盲猜参数

## 四、节点刷新 / 重新生成规则
每个媒体节点必须有：
- `Run`
- `Refresh`
- `Regenerate`
- `Save Local`

### Run
- 按当前参数创建新任务
- 产生新的 `runId`
- 不覆盖历史运行记录

### Refresh
- 仅查询当前 `latestTaskId` 的最新状态
- 不创建新任务

### Regenerate
- 基于最新参数重新创建新任务
- 旧任务保留历史
- 更新 `latestTaskId`

### Save Local
- 只对成功结果执行
- 不重新生成
- 对远端 URL 调用服务端下载保存
