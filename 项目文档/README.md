# titanX 项目文档总索引

## 文档根路径
统一项目文档目录：
`/home/liudehua/.openclaw/workspace/titanX/项目文档`

## 当前版本定位
**titanX 当前阶段为 Manual-first Baseline。**
当前目标只有一个：先完成**手动可执行节点工作台最小闭环**。

当前阶段验收范围：
- 手动建节点
- 手动连线
- 上游真实传递
- 手动编辑参数
- 手动触发 Generate / Analyze
- 真实执行
- 结果显示
- runtime 记录写回

**自动化暂不纳入本阶段验收**，包括但不限于：
- skillBinding 主链路
- agent 自动驱动节点
- 自动批量跑工作流
- 自动替换节点输入
- 完整自动化 tool / skill contract 闭环

## 当前阅读优先级
1. `IMPLEMENTATION_REDLINES.md`
2. `01_总开发主文档.md`
3. `02_节点体系与Schema总表.md`
4. `03_ImageNode_KIE_Schema_Contract.md`
5. `04_VideoNode_KIE_Schema_Contract.md`
6. `05_TextNode_Gemini_Schema_Contract.md`
7. `06_AudioNode_Schema_Contract.md`
8. `09_实现进度追踪.md`
9. `15_视频模型与API映射总表_2026-03-11.md`
10. `17_图片模型与API映射总表_2026-03-12.md`
11. `18_文本分析模型与API映射总表_2026-03-12.md`
12. `19_音频模型与API映射总表_2026-03-12.md`

## 当前阶段最重要的项目文档
### A. 当前状态 / 红线
1. `IMPLEMENTATION_REDLINES.md`
   - 当前阶段真正已完成什么
   - 当前阶段真正未完成什么
   - 一票否决项
2. `09_实现进度追踪.md`
   - 当前阶段的手动闭环推进状态
3. `08_当前开发锚点_清上下文后先看这里.md`
   - 当前接手时先读的最小锚点

### B. 项目说明 / 规则
4. `01_总开发主文档.md`
5. `02_节点体系与Schema总表.md`
6. `03_ImageNode_KIE_Schema_Contract.md`
7. `04_VideoNode_KIE_Schema_Contract.md`
8. `05_TextNode_Gemini_Schema_Contract.md`
9. `06_AudioNode_Schema_Contract.md`

### C. API 调研 round1 整合
10. `15_视频模型与API映射总表_2026-03-11.md`
11. `17_图片模型与API映射总表_2026-03-12.md`
12. `18_文本分析模型与API映射总表_2026-03-12.md`
13. `19_音频模型与API映射总表_2026-03-12.md`

### D. 当前仍需要的最小 Contracts
14. `contracts/image_generate_contract.md`
15. `contracts/video_generate_contract.md`
16. `contracts/text_analyze_contract.md`
17. `contracts/runtime_record_contract.md`

### E. 审计 / 参考
18. `审计报告/titanLX_项目文档深度扫描审查报告_2026-03-11.md`

## 维护规则
- 当前主文档只服务于 **手动闭环开发**
- 自动化、skill 化、agent 驱动只可作为后续方向备注，不得写成当前阶段已完成或当前阶段必做
- 当文档与实际实现冲突时，以 `IMPLEMENTATION_REDLINES.md` 与最新手动实测结果为准
- 没有浏览器行为证据，不得写 PASS
- 有代码/文件证据但无手动实测时，只能写“仅代码/文件证据通过”
- 新增正式文档后，必须同步更新本索引
