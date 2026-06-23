# Contributing / 贡献指南

## 中文

感谢你愿意改进 PDF Desensitizer。这个项目处理的是脱敏和隐私相关场景，请优先考虑安全、可复核和清晰边界。

### 提交 issue

提交问题时，请尽量包含：

- 你的操作系统和 Python 版本
- 安装方式
- 执行的命令
- 期望结果和实际结果
- 是否是扫描版 PDF、图片文字或可复制文本

请不要上传真实合同、真实个人信息、真实机构名称或任何敏感文件。可以使用合成 PDF、截图打码后的说明，或最小复现文本。

### 提交 PR

建议流程：

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

PR 建议包含：

- 修改目的
- 主要变更
- 测试结果
- 是否影响脱敏安全边界

### 安全原则

- 不要提交真实敏感 PDF
- 不要提交 `output/`、`example_output/`、`sensitive-*` 审计报告
- 新增识别规则时，优先避免漏脱敏；误遮可以接受，漏遮更危险
- README 中的限制说明不要弱化

## English

Thank you for improving PDF Desensitizer. Because this project is used for privacy and redaction workflows, please prioritize safety, reviewability, and clear limitations.

### Filing Issues

When opening an issue, please include:

- Operating system and Python version
- Installation method
- Command you ran
- Expected result and actual result
- Whether the PDF is scanned, image-based, or contains selectable text

Do not upload real contracts, real personal data, real organization names, or sensitive files. Use synthetic PDFs, redacted screenshots, or minimal reproduction text instead.

### Submitting Pull Requests

Recommended workflow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Please include:

- Purpose of the change
- Main changes
- Test results
- Whether the redaction safety boundary is affected

### Safety Principles

- Do not commit real sensitive PDFs
- Do not commit `output/`, `example_output/`, or `sensitive-*` audit reports
- When adding detection rules, prefer over-redaction to missed redaction
- Do not weaken the limitations documented in README

