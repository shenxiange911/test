# multimedia_super_skill

一个“母 Skill + 多子 Skill + 工具层”的多媒体全流程框架（可扩展）。

目标：把 **用户需求 → 理解(可选 Gemini) → 剧本 → 参考图 → 整张分镜图 → 拆分分镜 → 修复放大(香蕉2) → 单镜头视频 → 剪辑拼接 → 配乐/配音/字幕 → 成片** 跑通。

> 默认全部工具为 **mock**，不依赖外部模型/服务也能跑通流程（产物是占位文件）。  
> 你只需要把 `tools/*.py` 里的 `mode=api/command` 实现补齐，就能接入自己的工具链。

---

## 目录结构

```
multimedia_super_skill/
  run.py                # 母 skill 一键入口
  core/                 # 框架核心（协议、计划、输入识别、调度）
  tools/                # 工具适配层（ffmpeg/banana2/gemini/图生视频…）
  skills/               # 子技能（每个都可单独运行，也可被母 skill 调用）
  config/               # 配置（示例 + 本地私密配置）
  outputs/              # 自动生成的运行产物（gitignore）
```

---

## 快速开始（跑通全链路）

### 1) 安装依赖
```bash
pip install -r requirements.txt
```

### 2) 直接运行（全 mock）
```bash
python run.py --user-need "做一个咖啡广告，15秒，高级感" --input ./demo.jpg
```

输出会在：
- `outputs/run_<id>/artifacts/`（分镜图、拆分帧、音频、字幕等）
- `outputs/run_<id>/summary.json`（全流程索引）
- `outputs/run_<id>/plan.json`（可复现执行计划）

---

## 输入类型支持

母 skill 会先做输入识别（`inputs.detect`）：

- 本地图片/视频路径
- 图片直链 URL（会下载到 outputs/.../inputs/）
- 视频直链 URL（会下载到 outputs/.../inputs/）
- YouTube 链接（标记为 youtube，直接交给 Gemini file_uri）

命令示例：
```bash
python run.py --user-need "参考这个视频风格做广告：https://youtube.com/watch?v=xxxx" --input https://example.com/product.jpg
```

---

## Gemini 理解（可选）

Gemini 理解做成了独立 skill：`media.understand_gemini`

- YouTube：走 `file_data.file_uri`（稳定）
- 本地图片/视频：走 `inline_data` base64（可能会超时）

### 配置 Gemini

把 `config/api.example.json` 复制为 `config/api.json`（此文件被 gitignore）：

```bash
cp config/api.example.json config/api.json
```

编辑 `config/api.json`：

```json
{
  "gemini": {
    "apiKey": "YOUR_API_KEY",
    "baseUrl": "https://api.vectorengine.ai",
    "model": "gemini-2.5-pro"
  }
}
```

> ⚠️ 不要把真实 apiKey 提交到 GitHub。

### 跳过理解阶段
如果你只是想跑通生成链路：
```bash
python run.py --user-need "..." --skip-understand
```

---

## 子 Skill 单独运行（调试/扩展用）

每个 `skills/*.py` 都是一个独立 CLI。

例如：只做输入识别
```bash
python skills/inputs_detect.py --text "这里有个视频 https://youtube.com/watch?v=xxxx" --no-download
```

只做分镜拆分：
```bash
python skills/storyboard_split.py --sheet outputs/run_xxx/artifacts/storyboard_sheet.png --cols 3 --rows 2
```

---

## tools/ 工具说明（你最关心的）

- `tools/http.py`：统一 HTTP 请求/超时/重试（给所有 api 工具用）
- `tools/gemini_client.py`：Gemini 通用调用器（generateContent）
- `tools/gemini_youtube.py`：YouTube URL 分析（file_uri）
- `tools/gemini_local.py`：本地图片/视频分析（inline_data base64）
- `tools/ref_image_search.py`：参考图检索（mock/api）
- `tools/storyboard_gen.py`：生成整张分镜图（mock/api）
- `tools/banana2.py`：修复+放大（mock/command/api）
- `tools/image2video.py`：图生视频（mock/command/api）
- `tools/ffmpeg.py`：拼接、加音轨、烧字幕（auto/mock）
- `tools/subtitle.py`：把脚本文本转 SRT

---

## 如何新增一个子 Skill（扩展指南）

### 1) 新建文件 `skills/my_new_skill.py`
```python
from core.registry import register
from core.contracts import SkillResult, Artifact

@register("my.new_skill")
def run(ctx, params):
    # do something
    return SkillResult(ok=True, artifacts=[Artifact(type="text", value="hello")], data={"hello":"world"})
```

### 2) 在 `run.py` 顶部 import 它（让注册生效）
```python
from skills import my_new_skill
```

### 3) 在母 skill 的 plan 中加入 step（可选）
或直接 `run_skill("my.new_skill", ctx, {...})`

---

## 常见扩展点

- `skills/video_preprocess.py`：本地视频压缩/裁剪，减少 Gemini 超时
- `skills/video_fetch.py`：对非直链页面（抖音/B站等）抓取到 mp4 再处理
- `skills/storyboard_metadata.py`：生成严格结构化分镜 JSON（给剪辑/字幕对齐用）
- `tools/*`：接入你自己的 API（把 mode=api 的 NotImplemented 补齐）

---

## 许可证
按需添加（MIT/Apache-2.0 等）
