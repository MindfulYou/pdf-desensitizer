# Changelog / 更新日志

## [1.1.0] - 2026-06-22

### 中文

#### 变更

- 将工具重构为保留 PDF 原版式的脱敏器。
- 用基于文字坐标的 redaction 和马赛克遮罩替代“抽取文本后重新生成 PDF”的旧方案。
- 将识别、脱敏、报告、命令行入口拆分为独立包模块。
- 默认生成安全的公开摘要，不包含原始敏感文字。
- 增加可选的本地敏感审计报告。
- 改进角色标签、姓名列表、动词上下文中的姓名识别。
- 增加更严格的公开输出默认行为：输出文件名匿名化、公开摘要去敏、PDF 元数据标题替换、可见标题脱敏、机构/地名/公司简称识别。
- 增加贡献指南、GitHub issue 模板、redaction 核心测试和 demo 脚本测试。
- 更新项目作者信息。

### English

#### Changed

- Rebuilt the tool as a layout-preserving PDF redactor.
- Replaced text reflow output with coordinate-based redaction and mosaic overlays.
- Split detection, redaction, reporting, and CLI into package modules.
- Added safe default summary output that does not include original sensitive text.
- Added optional local sensitive audit reports.
- Improved demo-case detection for role labels, name lists, and verb contexts.
- Added stricter public-output defaults: anonymized output filenames, sanitized public summaries, metadata title replacement, visible title redaction, and organization/location/company-alias detection.
- Added contributing guidelines, GitHub issue templates, core redaction tests, and demo script tests.
- Updated project author metadata.

## [1.0.0] - 2026-06-22

### 中文

#### 新增

- 初始原型：抽取 PDF 文本、替换敏感词，并重新生成 PDF。

### English

#### Added

- Initial prototype that extracted PDF text, replaced sensitive terms, and generated a new PDF.
