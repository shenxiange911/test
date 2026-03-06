# kie.ai API 实战经验

## 查询端点
- ✅ 正确: `recordInfo` (查询任务状态)
- ❌ 错误: `getTask` (不存在)

## 限流规则
- 短时间大量请求会被限流
- **建议间隔**: 10-15秒
- 症状: 返回 waiting 状态但实际已完成

## 文件上传问题
- **上传端点**: kieai.redpandaai.co
- **问题**: 被 Cloudflare 拦截 (403/1010)
- **原因**: 可能是 IP 限制或反爬虫策略
- **临时方案**: 使用文生图模式，避免图生图

## 网络稳定性
- **curl 在 WSL**: 经常超时
- **Python urllib**: 更稳定
- **建议**: 优先用 Python 脚本调用 API

## 实测案例 (2026-03-02)
- 项目: 蒙面超人 VS 超人
- 生成分镜图: 4K (2×3网格), 8.4M
- 拆分后增强: 6张 2K, ~3M each
- 总耗时: ~2小时 (含多次迭代)

## 重要：保存生成结果 URL

### 为什么要保存 URL
- 图片/视频文件太大（几 MB 到几百 MB）
- 上传下载很麻烦
- kie.ai 返回的 URL 可以直接复用
- 方便后续分析、生成视频、分享

### 保存格式
每次生成后，保存到项目目录的 JSON 文件：

```json
{
  "taskId": "xxx",
  "model": "nano-banana-pro",
  "status": "success",
  "resultUrls": [
    "https://file.aiquickdraw.com/xxx.png"
  ],
  "createTime": 1234567890,
  "prompt": "...",
  "params": {...}
}
```

### 文件命名规范
- 参考图: `reference_views/front_task.json`
- 分镜图: `storyboard_task.json`
- 视频: `videos/002_task.json`

### 工具更新
所有生成工具都要自动保存 URL：
- kie_api.py - 基础工具，返回完整响应
- reference_generator.py - 保存每个视图的 URL
- storyboard_generator.py - 保存分镜图 URL
- video_generator.py - 保存视频 URL

## 官方文档（重要）

### 文档地址
- 主站：https://docs.kie.ai/
- 索引：https://docs.kie.ai/llms.txt

### 使用原则
**不要凭想象写参数，一定要先查官方文档！**

每个模型都有完整的 OpenAPI 规范，包括：
- 所有参数及类型
- 默认值
- 参数范围
- 示例代码
- 错误码说明

### 查询方法
1. 访问 https://docs.kie.ai/
2. 搜索模型名称（如 "kling-2.5-turbo"）
3. 查看完整的 API 文档
4. 或使用 web_fetch 抓取文档内容

### 示例
```bash
# 抓取 Kling 2.5 文档
web_fetch https://docs.kie.ai/market/kling/v2-5-turbo-image-to-video-pro

# 抓取 Nano Banana Pro 文档
web_fetch https://docs.kie.ai/market/google/nano-banana-pro
```
