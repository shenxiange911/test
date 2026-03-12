# MODEL_PARAMETER_GOVERNANCE.md

> 版本：2026-03-10 终版收口  
> 定位：titanLX 当前阶段关于“模型字段、业务字段、API 参数映射”的主规范。

## 1. 当前阶段范围（v1）
当前阶段只要求 image 相关 family 进入主线：
- `gpt4o-image`
- `flux-kontext`
- `market-image`

以下 family 属于后续扩展/未来阶段，不得误读为当前全部已落地：
- `runway-video`
- `veo31-video`
- `market-video`
- `suno-audio`
- `market-audio`

## 2. 结论先行
模型参数规范必须分成两层：
1. **titanLX 统一业务字段层**
2. **family / model API 映射层**

禁止让节点 UI 直接持有原始 KIE 各模型私有字段。

## 3. 文档优先级
涉及模型字段、参数映射时，优先级固定如下：
1. `严格开发文档/MODEL_PARAMETER_GOVERNANCE.md`（定义字段治理与阶段范围）
2. `kie接入文档/11_FIELD_MAPPING_SOURCE_OF_TRUTH.md`（定义字段映射职责边界）
3. `kie接入文档/04_KIE_PARAMETER_RULES.md`（定义 family 参数细则）
4. `kie接入文档/03_KIE_MODEL_FAMILIES_AND_UI_MAPPING.md`
5. 各模型官方文档

## 4. 统一业务字段原则
### 4.1 节点/UI 层允许使用的字段
对 Image Generate 当前阶段，统一业务字段只允许使用：
- `providerFamily`
- `model`
- `prompt`
- `ratio`
- `size`
- `format`
- `inputImages`
- `enhance`
- `translate`
- `fallback`
- `templateRefs`
- `customPrompting`
- `cameraParams`

### 4.2 节点/UI 层禁止直接出现的字段
以下字段只能出现在 adapter / builder / server client：
- `filesUrl`
- `callBackUrl`
- `uploadCn`
- `enableFallback`
- `outputFormat`
- `aspectRatio`
- `inputImage`
- `enableTranslation`
- `imageUrls`
- `seeds`
- `waterMark`

## 5. family 级最小字段集合
### 5.1 gpt4o-image
业务字段：
- `providerFamily = 'gpt4o-image'`
- `model = 'gpt4o-image'`
- `prompt`
- `ratio`
- `inputImages`
- `enhance`
- `fallback`

### 5.2 flux-kontext
业务字段：
- `providerFamily = 'flux-kontext'`
- `model`
- `prompt`
- `ratio`
- `format`
- `inputImages`
- `translate`

### 5.3 market-image
业务字段：
- `providerFamily = 'market-image'`
- `model`
- `prompt`
- `ratio`
- `size`
- `format`
- `inputImages`
- `templateRefs`
- `customPrompting`
- `cameraParams`

硬规则：
- registry 没定义，不能接
- builder 没写清，不能接
- officialDocUrl 没填，不能接

## 6. model-registry.ts 的最低要求
每个模型 registry 项必须包含：
- `uiLabel`
- `family`
- `modelKey`
- `kind`
- `officialDocUrl`
- `adapter`
- `inputMode`
- `uiFields`
- `defaults`
- `inputBuilder`
- `resultParser`

新增模型时，必须先补 registry，再允许 UI 暴露。

## 7. 新增字段审批流程
以下情况必须先更新文档，再允许改代码：
- 在节点 schema 中添加新字段
- 在 runtime 中添加新状态字段
- 在 customPrompting 中添加新配置字段
- 在 model registry 中加入新的业务字段映射

审批流程：
1. 先在本文档说明新增字段的用途
2. 判断是否属于统一业务字段
3. 若是，更新 `NODE_SCHEMA_SPEC.md`
4. 若否，通过 registry / params / adapter 扩展
5. 同步更新 11 / 04 等映射文档
6. 最后才允许修改代码

## 8. 一票否决项
以下任一出现，直接判失败：
- agent 自己发明未经文档批准的新业务字段
- UI 层直接写原始 KIE 私有字段
- 未经过 registry 就在 payload builder 里临时拼未知模型参数
- 报告中说“支持某模型”，但给不出字段来源和映射依据
