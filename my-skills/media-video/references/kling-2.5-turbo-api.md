# Kling 2.5 Turbo Image to Video Pro API

## 端点
```
POST https://api.kie.ai/api/v1/jobs/createTask
```

## 认证
```
Authorization: Bearer YOUR_API_KEY
```

## 模型名称
```
kling/v2-5-turbo-image-to-video-pro
```

## 请求参数

### 必需参数
| 参数 | 类型 | 说明 |
|------|------|------|
| model | string | 固定值: `kling/v2-5-turbo-image-to-video-pro` |
| input.prompt | string | 视频生成提示词，最大 2500 字符 |
| input.image_url | string | 起始帧图片 URL（必需） |

### 可选参数
| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| callBackUrl | string | - | 回调 URL，任务完成时接收通知 |
| input.tail_image_url | string | "" | 结束帧图片 URL |
| input.duration | string | "5" | 视频时长: "5" 或 "10" 秒 |
| input.negative_prompt | string | "blur, distort, and low quality" | 负面提示词，最大 2496 字符 |
| input.cfg_scale | number | 0.5 | CFG 引导强度，范围 0-1，步长 0.1 |

## 请求示例

```json
{
  "model": "kling/v2-5-turbo-image-to-video-pro",
  "input": {
    "prompt": "Slow push in on masked rider in black and gold armor, cinematic lighting",
    "image_url": "https://file.aiquickdraw.com/xxx.png",
    "tail_image_url": "",
    "duration": "5",
    "negative_prompt": "blur, distort, and low quality",
    "cfg_scale": 0.5
  },
  "callBackUrl": "https://your-domain.com/callback"
}
```

## 响应示例

```json
{
  "code": 200,
  "msg": "success",
  "data": {
    "taskId": "task_kling_1765184408908"
  }
}
```

## 查询任务状态

```
GET https://api.kie.ai/api/v1/jobs/recordInfo?taskId={taskId}
```

## 状态码

| 代码 | 说明 |
|------|------|
| 200 | 成功 |
| 401 | 认证失败 |
| 402 | 余额不足 |
| 404 | 资源不存在 |
| 422 | 参数验证失败 |
| 429 | 请求限流 |
| 455 | 服务维护中 |
| 500 | 服务器错误 |
| 501 | 生成失败 |
| 505 | 功能已禁用 |

## 运镜提示词技巧

### 镜头运动
- Push in: "Slow push in camera movement"
- Pull out: "Pull out camera movement"
- Pan: "Pan camera movement from left to right"
- Static: "Static camera, locked shot"
- Tracking: "Smooth tracking shot following subject"

### 速度控制
- Slow: "Slow, smooth camera movement"
- Fast: "Fast, dynamic camera movement"
- Slow motion: "Slow motion effect"

### 角度
- Low angle: "Low angle shot, looking up"
- High angle: "High angle shot, looking down"
- Eye level: "Eye level camera angle"
