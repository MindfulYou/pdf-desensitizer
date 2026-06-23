# Roadmap / 路线图

## 中文

PDF Desensitizer 目前是一个本地 PDF 脱敏工具，重点是尽量保留原 PDF 排版，并对中文姓名、公司名、机构名、地名等敏感信息进行辅助脱敏。

这个路线图用于记录未来可能的改进方向。具体优先级会根据实际使用反馈、问题严重程度和维护成本调整。

### 近期计划

- 增强中文姓名、公司简称、机构名称和地名识别规则
- 增加更多真实但不敏感的合成测试样例
- 改进 README 中的使用示例和截图
- 增加 GitHub Actions 自动测试
- 补充更多安全边界和使用限制说明

### 中期计划

- 增加 OCR 工作流说明，支持扫描版 PDF 的前置处理
- 增加脱敏前后对比预览示例
- 增加批量处理结果汇总
- 增加更详细的本地审计报告选项
- 优化误遮和漏遮的人工复核流程

### 长期计划

- 提供图形界面版本，降低非技术用户使用门槛
- 探索桌面应用打包，例如 macOS 和 Windows
- 支持更多语言和地区的姓名、机构、地名识别
- 支持自定义规则模板
- 支持更完整的 OCR 集成
- 支持脱敏任务配置文件

### 暂不计划

- 不计划上传用户文件到云端处理
- 不计划保存用户原始 PDF
- 不计划承诺法律级、合规级或审计级最终脱敏
- 不计划替代人工复核流程

### 欢迎贡献

欢迎提交 issue 或 PR，尤其是：

- 漏脱敏案例，但请不要上传真实敏感文件
- 合成测试样例
- 识别规则改进
- 文档改进
- 跨平台使用反馈

---

## English

PDF Desensitizer is currently a local PDF redaction tool focused on preserving the original PDF layout while assisting with redaction of Chinese personal names, company names, organization names, locations, and related sensitive terms.

This roadmap records possible future improvements. Priorities may change based on user feedback, issue severity, and maintenance cost.

### Near-term Plans

- Improve detection rules for Chinese personal names, company aliases, organization names, and locations
- Add more realistic but non-sensitive synthetic test cases
- Improve README usage examples and screenshots
- Add GitHub Actions automated tests
- Expand documentation for security boundaries and limitations

### Mid-term Plans

- Add OCR workflow documentation for scanned PDFs
- Add before-and-after redaction preview examples
- Improve batch processing summaries
- Add more detailed local audit report options
- Improve manual review workflows for over-redaction and missed redaction

### Long-term Plans

- Provide a graphical user interface for non-technical users
- Explore desktop app packaging for macOS and Windows
- Support more languages and regional name, organization, and location patterns
- Support custom rule templates
- Support deeper OCR integration
- Support redaction task configuration files

### Not Planned

- No cloud upload or cloud processing of user files
- No storage of user original PDFs
- No promise of legal-grade, compliance-grade, or audit-grade final redaction
- No replacement for human review

### Contributions Welcome

Issues and pull requests are welcome, especially for:

- Missed redaction cases, but do not upload real sensitive files
- Synthetic test samples
- Detection rule improvements
- Documentation improvements
- Cross-platform usage feedback
