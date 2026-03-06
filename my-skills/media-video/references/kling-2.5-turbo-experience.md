
## 2026-03-03 实战经验：蒙面超人 VS 超人项目

### 成功案例
- **P2 - 蒙面超人登场**：推镜效果好，角色动作自然
- **P3 - 超人降临**：拉镜可以，但脚步不够自然

### Prompt 优化
运镜描述要放在最前面：
```
"Slow push in camera movement. Kamen Rider in black and gold armor emerges from smoke. Gold armor gleaming, white scarf blowing. Cinematic 35mm film quality."
```

### 参数配置
- duration: "5" (5秒)
- cfg_scale: 0.5 (默认值)
- negative_prompt: "blur, distort, and low quality"

### 常见问题
1. **脚步不自然** - 降落/行走动作容易出问题，需要在 prompt 中强调 "natural footwork" 或 "smooth landing"
2. **视频下载 403** - 直接用浏览器打开 URL 或在 kie.ai/logs 下载
3. **URL 14天有效期** - 必须立即保存到 JSON 文件

### 运镜类型效果
- Push in（推镜）：✅ 效果好，适合登场/特写
- Pull out（拉镜）：✅ 可用，但注意角色动作
- Static（静止）：待测试
- Tracking（跟踪）：待测试
- Pan（横摇）：待测试
