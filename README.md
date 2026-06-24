# PDF Desensitizer / PDF 脱敏工具

## 中文说明

本地 PDF 脱敏工具。它会识别中文人名、机构、公司全称/简称、地名、合同金额、合同签订方、账户和税务联系信息等敏感内容，在原 PDF 的文字坐标上执行 redaction，并绘制灰度马赛克遮罩，尽量保持表格、图片、页眉页脚和页面版式不变。

> 重要提醒：自动识别一定可能漏检。公开分享任何脱敏 PDF 前，请人工复核每一页。

### 特性

- 保留原 PDF 页面布局，不重新排版
- 对命中的文字区域执行 PDF redaction，删除原始文字内容后再绘制马赛克
- 自动识别常见中文人名、角色字段中的姓名、公司全称、公司简称、机构名、地名
- 支持合同类敏感信息辅助脱敏，包括合同金额、甲乙丙丁等签订方全名、纳税人名称、纳税人识别号、办公地址、电话、手机、联系人姓名、开户行和银行账号等
- 默认脱敏输出文件名，例如 `redacted-001.pdf`
- 默认脱敏第一页可见标题，并替换 PDF 元数据标题
- 支持手动补充脱敏词
- 默认只生成不含原始文件名和原文敏感词的公开摘要
- 可选生成本地审计报告，但报告包含原始敏感文字，不能公开发布
- 全程本地处理，不上传，不联网

### 安装

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

也可以作为命令行工具安装：

```bash
pip install -e .
```

### 使用

处理一个文件夹：

```bash
pdf-desensitize ./input-pdfs ./output
```

处理单个 PDF：

```bash
pdf-desensitize ./contract.pdf ./output
```

从源码目录直接运行：

```bash
python3 pdf_desensitize.py ./input-pdfs ./output
```

手动补充漏检词：

```bash
pdf-desensitize ./input-pdfs ./output \
  --custom-names 陈建国 刘洋 周明华 \
  --custom-companies 万科企业股份有限公司
```

从文本文件读取手动脱敏词：

```bash
pdf-desensitize ./input-pdfs ./output --custom-words ./example/manual_words_example.txt
```

如果你确定第一页标题不敏感，可以保留标题：

```bash
pdf-desensitize ./input-pdfs ./output --keep-visible-title
```

生成本地审计报告：

```bash
pdf-desensitize ./input-pdfs ./output --write-sensitive-report
```

### 输出文件

默认输出：

```text
output/
├── redacted-001.pdf
└── redaction-summary.json
```

`redaction-summary.json` 不包含原始文件名和原始敏感文字，适合随脱敏 PDF 保留。

如果使用 `--write-sensitive-report`，会额外生成：

```text
output/
├── sensitive-redaction-map.json
└── sensitive-redaction-report.md
```

这两个文件包含原始文件名、原始姓名、公司名、机构名、地名等，只能用于本地复核，不要上传 GitHub、网盘或发给外部人员。

### 适用范围

适合：

- 可提取文本的 PDF
- 合同、报告、尽调材料中的中文姓名、公司名、机构名、地名、金额、账户和联系信息辅助脱敏
- 希望保留原版式，只遮盖敏感文字区域的场景

### 合同类脱敏范围

处理合同时，工具会尽量遮盖各方详细信息，同时保留合同条文结构，方便继续审核合同内容。

默认会尝试遮盖：

- 合同金额，包括阿拉伯数字金额和中文大写金额
- 甲方、乙方、丙方、丁方等合同签订方全名
- 纳税人名称
- 纳税人识别号、统一社会信用代码、税号
- 办公地址、注册地址、通讯地址、联系地址
- 电话、座机、手机、联系电话
- 联系人姓名、联系人
- 开户名称、账户名称、户名
- 开户银行、开户行
- 银行账号、银行账户、收款账号、付款账号

可能还需要人工补充的内容：

- 身份证号、护照号、营业执照编号
- 邮箱、微信号、QQ号、网址、IP 地址
- 签章、手写签名、图片水印、扫描件中的文字
- 项目名称、订单号、合同编号、发票号码、快递单号
- 付款节点中能反推出商业条件的特殊价格、折扣、费率

如果合同中有特殊名称或编号，请使用 `--custom-words` 手动词表补充。

不适合直接依赖：

- 扫描版 PDF 或图片里的文字
- 手写签名、印章、图片水印中的敏感信息
- 需要法律级/合规级保证的最终脱敏流程

对扫描版 PDF，请先使用 OCR 工具生成可搜索文本层，再运行本工具，并人工复核。

### 手动词表格式

每行一个词，`#` 开头为注释：

```text
# 人名
张三
李四

# 公司名
北京某科技有限公司
上海创新集团
```

### 开发

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

### 常见问题

#### 出现 `zsh: command not found: python` 怎么办？

如果终端显示：

```text
zsh: command not found: python
```

说明你的 Mac 没有 `python` 这个命令。新版 macOS 通常只有 `python3`。

先试：

```bash
python3 --version
```

如果看到类似：

```text
Python 3.13.5
```

说明 Python 已安装。后续命令请把 `python` 改成 `python3`，例如：

```bash
python3 -m venv .venv
python3 pdf_desensitize.py ./input-pdfs ./output
```

贡献代码前请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)。提交 issue 时请勿上传真实敏感 PDF 或真实个人/机构信息。

### 公开发布建议

- 只发布源码、README、测试和不含真实敏感信息的示例
- 不要提交真实输入 PDF、脱敏输出 PDF、本地审计报告
- 发布前运行 `pytest`
- 在 release 包里排除 `__MACOSX`、`.DS_Store`、`output/`、`sensitive-*`

## English

PDF Desensitizer is a local PDF redaction tool. It detects sensitive Chinese terms such as personal names, organizations, full and abbreviated company names, locations, contract amounts, contract parties, account details, tax IDs, addresses, phone numbers, and contact names. It applies PDF redaction at the original text coordinates and draws grayscale mosaic overlays while preserving tables, images, headers, footers, and page layout as much as possible.

> Important: automatic detection can miss sensitive content. Always review every page before sharing a redacted PDF.

### Features

- Preserves the original PDF page layout instead of rebuilding the document from extracted text
- Applies real PDF redaction to matched text areas, then draws mosaic overlays
- Detects common Chinese personal names, role-labeled names, company full names, company aliases, organization names, and locations
- Supports contract redaction for amounts, party names, taxpayer names, tax IDs, addresses, phone numbers, contact names, bank names, and bank accounts
- Uses anonymized output filenames by default, for example `redacted-001.pdf`
- Redacts the first visible title line by default and replaces the PDF metadata title
- Supports manual redaction terms
- Generates a public summary that does not include original filenames or original sensitive terms
- Can optionally generate local audit reports, but those reports contain original sensitive text and must not be published
- Runs locally only; no upload and no network access are required during processing

### Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

You can also install it as a command line tool:

```bash
pip install -e .
```

### Usage

Redact a folder of PDFs:

```bash
pdf-desensitize ./input-pdfs ./output
```

Redact a single PDF:

```bash
pdf-desensitize ./contract.pdf ./output
```

Run directly from a source checkout:

```bash
python3 pdf_desensitize.py ./input-pdfs ./output
```

Add manual terms for missed detections:

```bash
pdf-desensitize ./input-pdfs ./output \
  --custom-names 陈建国 刘洋 周明华 \
  --custom-companies 万科企业股份有限公司
```

Load manual terms from a text file:

```bash
pdf-desensitize ./input-pdfs ./output --custom-words ./example/manual_words_example.txt
```

Keep the first visible title line if you know it is not sensitive:

```bash
pdf-desensitize ./input-pdfs ./output --keep-visible-title
```

Write local audit reports:

```bash
pdf-desensitize ./input-pdfs ./output --write-sensitive-report
```

### Output Files

Default output:

```text
output/
├── redacted-001.pdf
└── redaction-summary.json
```

`redaction-summary.json` does not contain original filenames or original sensitive text, so it can be kept with the redacted PDFs.

If `--write-sensitive-report` is used, these files are also generated:

```text
output/
├── sensitive-redaction-map.json
└── sensitive-redaction-report.md
```

These two files contain original filenames, personal names, company names, organization names, locations, and other sensitive terms. Use them only for local review. Do not upload them to GitHub, cloud drives, or share them externally.

### Scope

Suitable for:

- PDFs with extractable text
- Assisted redaction of Chinese personal names, company names, organization names, locations, amounts, account details, and contact information in contracts, reports, and due diligence materials
- Cases where the original layout should remain unchanged and only sensitive text areas should be covered

### Contract Redaction Scope

For contracts, the tool tries to redact detailed party information while keeping the contract clauses and structure readable for review.

It attempts to redact:

- Contract amounts, including numeric amounts and Chinese uppercase amounts
- Full names of Party A, Party B, Party C, Party D, and other contracting parties
- Taxpayer names
- Taxpayer identification numbers, unified social credit codes, and tax IDs
- Office addresses, registered addresses, mailing addresses, and contact addresses
- Telephone numbers, landlines, mobile numbers, and contact phone numbers
- Contact names
- Account names and account holders
- Bank names
- Bank account numbers

Items that may still need manual terms:

- ID card numbers, passport numbers, and business license numbers
- Emails, WeChat IDs, QQ IDs, URLs, and IP addresses
- Seals, handwritten signatures, image watermarks, and scanned text
- Project names, order numbers, contract numbers, invoice numbers, and tracking numbers
- Special prices, discounts, rates, or payment terms that reveal commercial conditions

Use `--custom-words` for contract-specific terms or identifiers.

Do not rely on it alone for:

- Scanned PDFs or text embedded in images
- Handwritten signatures, seals, stamps, or image watermarks
- Final legal-grade or compliance-grade redaction without human review

For scanned PDFs, run OCR first to create a searchable text layer, then use this tool and review the result manually.

### Manual Terms File

Use one term per line. Lines starting with `#` are comments:

```text
# Personal names
张三
李四

# Company names
北京某科技有限公司
上海创新集团
```

### Development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

### FAQ

#### What if I see `zsh: command not found: python`?

This means your Mac does not have the `python` command. Newer macOS versions usually provide `python3` instead.

Try:

```bash
python3 --version
```

If you see a version such as:

```text
Python 3.13.5
```

Python is installed. Use `python3` instead of `python`, for example:

```bash
python3 -m venv .venv
python3 pdf_desensitize.py ./input-pdfs ./output
```

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before contributing. Do not upload real sensitive PDFs or real personal/organization information when filing issues.

### Publishing Notes

- Publish only source code, README, tests, and examples without real sensitive data
- Do not commit real input PDFs, redacted output PDFs, or local audit reports
- Run `pytest` before publishing
- Exclude `__MACOSX`, `.DS_Store`, `output/`, and `sensitive-*` from release packages

## License / 许可

MIT License. See [LICENSE](./LICENSE).
