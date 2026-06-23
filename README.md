# PDF Desensitizer / PDF 脱敏工具

## 中文说明

本地 PDF 脱敏工具。它会识别中文人名、机构、公司全称/简称、地名等敏感名词，在原 PDF 的文字坐标上执行 redaction，并绘制灰度马赛克遮罩，尽量保持表格、图片、页眉页脚和页面版式不变。

> 重要提醒：自动识别一定可能漏检。公开分享任何脱敏 PDF 前，请人工复核每一页。

### 特性

- 保留原 PDF 页面布局，不重新排版
- 对命中的文字区域执行 PDF redaction，删除原始文字内容后再绘制马赛克
- 自动识别常见中文人名、角色字段中的姓名、公司全称、公司简称、机构名、地名
- 默认脱敏输出文件名，例如 `redacted-001.pdf`
- 默认脱敏第一页可见标题，并替换 PDF 元数据标题
- 支持手动补充脱敏词
- 默认只生成不含原始文件名和原文敏感词的公开摘要
- 可选生成本地审计报告，但报告包含原始敏感文字，不能公开发布
- 全程本地处理，不上传，不联网

### 安装

```bash
python -m venv .venv
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
python pdf_desensitize.py ./input-pdfs ./output
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
- 合同、报告、尽调材料中的中文姓名、公司名、机构名、地名辅助脱敏
- 希望保留原版式，只遮盖敏感文字区域的场景

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
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

贡献代码前请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)。提交 issue 时请勿上传真实敏感 PDF 或真实个人/机构信息。

### 公开发布建议

- 只发布源码、README、测试和不含真实敏感信息的示例
- 不要提交真实输入 PDF、脱敏输出 PDF、本地审计报告
- 发布前运行 `pytest`
- 在 release 包里排除 `__MACOSX`、`.DS_Store`、`output/`、`sensitive-*`

## English

PDF Desensitizer is a local PDF redaction tool. It detects sensitive Chinese terms such as personal names, organizations, full and abbreviated company names, and locations. It applies PDF redaction at the original text coordinates and draws grayscale mosaic overlays while preserving tables, images, headers, footers, and page layout as much as possible.

> Important: automatic detection can miss sensitive content. Always review every page before sharing a redacted PDF.

### Features

- Preserves the original PDF page layout instead of rebuilding the document from extracted text
- Applies real PDF redaction to matched text areas, then draws mosaic overlays
- Detects common Chinese personal names, role-labeled names, company full names, company aliases, organization names, and locations
- Uses anonymized output filenames by default, for example `redacted-001.pdf`
- Redacts the first visible title line by default and replaces the PDF metadata title
- Supports manual redaction terms
- Generates a public summary that does not include original filenames or original sensitive terms
- Can optionally generate local audit reports, but those reports contain original sensitive text and must not be published
- Runs locally only; no upload and no network access are required during processing

### Installation

```bash
python -m venv .venv
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
python pdf_desensitize.py ./input-pdfs ./output
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
- Assisted redaction of Chinese personal names, company names, organization names, and locations in contracts, reports, and due diligence materials
- Cases where the original layout should remain unchanged and only sensitive text areas should be covered

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
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before contributing. Do not upload real sensitive PDFs or real personal/organization information when filing issues.

### Publishing Notes

- Publish only source code, README, tests, and examples without real sensitive data
- Do not commit real input PDFs, redacted output PDFs, or local audit reports
- Run `pytest` before publishing
- Exclude `__MACOSX`, `.DS_Store`, `output/`, and `sensitive-*` from release packages

## License / 许可

MIT License. See [LICENSE](./LICENSE).

## Support / 支持作者

If this project helps you, please consider giving it a Star.

如果这个项目对你有帮助，欢迎给仓库点一个 Star。

You can also support the author via Alipay.

也可以通过支付宝支持作者。一杯美式，或者一碗豆浆，一瓶水也行。

![Alipay QR Code](./assets/alipay.png)

## About the Author / 关于作者

Created and maintained by **XueyouChu**.

- GitHub: [MindfulYou](https://github.com/MindfulYou)
- Email: cxy@youshengyu.com
