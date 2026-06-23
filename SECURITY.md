# Security Policy / 安全政策

## 中文

PDF Desensitizer 是一个本地 PDF 脱敏工具，适用于对可提取文本的 PDF 进行辅助脱敏。由于脱敏与隐私、安全、合规高度相关，请在使用和反馈问题时注意以下边界。

### 不要上传真实敏感文件

请不要在 GitHub issue、Pull Request、讨论区或公开页面中上传：

- 真实合同
- 真实报告
- 真实身份证明材料
- 真实姓名、电话、邮箱、地址
- 真实公司名、机构名、客户名
- 包含商业秘密、个人隐私或合规风险的 PDF

如果需要反馈问题，请使用：

- 合成示例 PDF
- 手工构造的最小复现文本
- 已经打码的截图
- 不含真实敏感信息的示例文件

### 如何反馈漏脱敏问题

如果你发现工具漏掉了某些内容，请在 issue 中说明：

- 漏掉的是哪一类信息，例如姓名、公司名、机构名、地名、简称
- 相关文本的大致结构，例如“项目负责人：张三”或“由某某公司提交”
- PDF 是否为扫描版
- 文字是否可以复制
- 使用的命令和参数
- 期望被遮盖的内容类型

请不要直接贴真实敏感文本。可以把真实内容替换为虚构内容，例如：

- 项目负责人：张三
- 供应商：北京某某科技有限公司
- 地点：上海市浦东新区

### 安全边界

本工具不能保证法律级、合规级或审计级的最终脱敏效果。

它适合作为脱敏流程中的辅助工具，但不能替代人工复核。正式对外发送、公开发布、提交监管机构、提交法院、提交客户或用于任何高风险场景前，请务必逐页检查输出 PDF。

本工具主要处理 PDF 中可提取的文本层。对于扫描版 PDF、图片中的文字、手写签名、印章、水印、截图文字或没有 OCR 文本层的文档，可能无法自动识别和遮盖。

对于扫描件或图片型 PDF，请先使用 OCR 工具生成可搜索文本层，再运行本工具，并进行人工复核。

### 本地审计报告

如果使用 --write-sensitive-report，工具会生成本地审计报告。该报告可能包含原始文件名、姓名、公司名、机构名、地名、简称以及其他敏感信息。

请不要上传、公开、转发或提交这些文件：

- sensitive-redaction-map.json
- sensitive-redaction-report.md

这些文件仅供本地复核使用。完成复核后，建议将其妥善保存到安全位置，或在不再需要时删除。

### 法律免责声明

本工具仅作为技术辅助工具提供，不构成法律意见、合规意见、审计意见或专业安全建议。

使用者应自行判断本工具是否适合其具体使用场景，并自行承担使用本工具所产生的全部风险。作者和贡献者不保证本工具能够识别、遮盖或删除所有敏感信息，也不保证输出文件满足任何法律、监管、合同、审计或合规要求。

因使用、误用、无法使用本工具，或因依赖本工具输出结果而产生的任何直接或间接后果，包括但不限于数据泄露、隐私侵权、商业损失、合规处罚、法律纠纷、诉讼、仲裁、索赔、费用、损害赔偿或其他责任，均由使用者自行承担。作者和贡献者在法律允许的最大范围内不承担任何责任。

在正式对外发送、公开发布、提交监管机构、提交法院、提交客户或用于任何高风险场景前，请务必进行人工复核，并在必要时咨询专业律师、合规顾问或安全专家。

### 安全问题联系方式

如果你发现严重安全问题，或发现工具可能导致敏感信息泄露，请不要公开提交包含敏感细节的 issue。

可以联系作者：

cxy@youshengyu.com

---

## English

PDF Desensitizer is a local PDF redaction tool designed to assist with redacting PDFs that contain extractable text. Because redaction involves privacy, security, and compliance concerns, please follow the boundaries below when using the tool or reporting issues.

### Do Not Upload Real Sensitive Files

Do not upload the following to GitHub issues, pull requests, discussions, or public pages:

- Real contracts
- Real reports
- Real identity documents
- Real names, phone numbers, emails, or addresses
- Real company names, organization names, or client names
- PDFs containing trade secrets, personal data, or compliance risks

If you need to report an issue, please use:

- Synthetic sample PDFs
- Minimal reproduction text
- Redacted screenshots
- Example files that contain no real sensitive information

### How to Report Missed Redactions

If the tool misses sensitive content, please describe:

- The type of missed information, such as personal name, company name, organization name, location, or alias
- The rough text pattern, such as “Project owner: Zhang San” or “submitted by Example Company”
- Whether the PDF is scanned
- Whether the text is selectable/copyable
- The command and options you used
- The type of content you expected to be covered

Do not paste real sensitive text directly. Replace it with fictional examples, such as:

- Project owner: Zhang San
- Supplier: Beijing Example Technology Co., Ltd.
- Location: Pudong New Area, Shanghai

### Security Boundary

This tool does not guarantee legal-grade, compliance-grade, or audit-grade final redaction.

It is intended as an assistive tool in a redaction workflow and does not replace human review. Before sending files externally, publishing files publicly, submitting files to regulators, courts, clients, or using files in any high-risk context, always review every page of the output PDF manually.

This tool primarily works with extractable PDF text layers. It may not automatically detect or cover scanned PDFs, text embedded in images, handwritten signatures, seals, watermarks, screenshot text, or documents without an OCR text layer.

For scanned or image-based PDFs, run OCR first to create a searchable text layer, then use this tool and review the output manually.

### Local Audit Reports

If you use --write-sensitive-report, the tool generates local audit reports. These reports may contain original filenames, personal names, company names, organization names, locations, aliases, and other sensitive information.

Do not upload, publish, forward, or submit these files:

- sensitive-redaction-map.json
- sensitive-redaction-report.md

These files are intended only for local review. After review, store them securely or delete them when they are no longer needed.

### Legal Disclaimer

This tool is provided solely as a technical aid. It does not constitute legal advice, compliance advice, audit advice, or professional security advice.

Users are responsible for determining whether this tool is suitable for their specific use case and assume all risks arising from the use of this tool. The author and contributors do not warrant that the tool will identify, cover, remove, or redact all sensitive information, nor do they warrant that any output file will satisfy any legal, regulatory, contractual, audit, or compliance requirement.

To the maximum extent permitted by applicable law, the author and contributors shall not be liable for any direct or indirect consequences arising from the use, misuse, inability to use, or reliance on the output of this tool, including but not limited to data leakage, privacy violations, business losses, compliance penalties, legal disputes, lawsuits, arbitration, claims, costs, damages, or any other liability.

Before sending files externally, publishing files publicly, submitting files to regulators, courts, clients, or using files in any high-risk context, always perform manual review and consult qualified legal, compliance, or security professionals when necessary.

### Contact for Security Issues

If you find a serious security issue or believe the tool may cause sensitive information leakage, please do not open a public issue containing sensitive details.

You can contact the author at:

cxy@youshengyu.com
