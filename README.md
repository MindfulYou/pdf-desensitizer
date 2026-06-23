# PDF Desensitizer / PDF 脱敏工具

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Beta-orange)
![Tests](https://github.com/MindfulYou/pdf-desensitizer/actions/workflows/tests.yml/badge.svg)

## 中文说明

PDF Desensitizer 是一个面向中文文档的本地 PDF 脱敏工具。它会识别中文姓名、机构、公司全称/简称、地名等敏感名词，在原 PDF 的文字坐标上执行 redaction，并绘制灰度马赛克遮罩，尽量保持表格、图片、页眉页脚和页面版式不变。

> 重要提醒：自动识别一定可能漏检。公开分享任何脱敏 PDF 前，请人工复核每一页。

## 特性

- 面向中文 PDF 文档脱敏场景
- 保留原 PDF 页面布局，不重新排版
- 对命中的文字区域执行 PDF redaction，删除原始文字内容后再绘制马赛克
- 自动识别常见中文人名、角色字段中的姓名、公司全称、公司简称、机构名、地名
- 默认脱敏输出文件名，例如 `redacted-001.pdf`
- 默认脱敏第一页可见标题，并替换 PDF 元数据标题
- 支持手动补充脱敏词
- 默认只生成不含原始文件名和原文敏感词的公开摘要
- 可选生成本地审计报告，但报告包含原始敏感文字，不能公开发布
- 全程本地处理，不上传，不联网

## 普通用户使用指南

这份指南写给不熟悉 GitHub、Python、终端命令的普通用户。

PDF Desensitizer 可以帮助你把 PDF 里的姓名、公司名、机构名、地名等敏感信息打上马赛克，并尽量保留原来的 PDF 排版。

请注意：当前版本还不是一个可以双击打开的 App。它需要通过电脑里的“终端”运行。如果你完全不熟悉终端，建议请熟悉电脑的人协助你操作，或等待未来的图形界面版本。

### 这个工具适合做什么？

适合：

- 合同对外发送前脱敏
- 报告分享前脱敏
- 尽调材料整理
- 案例材料匿名化
- PDF 中姓名、公司、机构、地名的初步遮盖

不适合直接依赖：

- 扫描版 PDF
- 图片里的文字
- 手写签名
- 印章
- 水印
- 法律级、合规级、审计级最终脱敏

正式发送文件前，请一定人工检查每一页。

### 第一步：下载项目

1. 打开项目页面：

   https://github.com/MindfulYou/pdf-desensitizer

2. 点击绿色按钮：

   Code

3. 点击：

   Download ZIP

4. 下载完成后，双击解压。

5. 你会得到一个文件夹，名字类似：

   pdf-desensitizer-main

### 第二步：准备 PDF 文件夹

为了避免搞混，建议你在桌面新建两个文件夹：

- 原始PDF
- 脱敏PDF

把需要处理的 PDF 放进：

- 原始PDF

处理完成后的文件会出现在：

- 脱敏PDF

### 第三步：打开终端

macOS 用户：

1. 按下键盘：

   Command + 空格

2. 输入：

   终端

   或者：

   Terminal

3. 按回车打开。

### 第四步：进入工具文件夹

假设你把项目解压到了“下载”文件夹，请在终端里输入：

    cd ~/Downloads/pdf-desensitizer-main

然后按回车。

如果你看到报错，说明文件夹名字可能不一样。你可以打开下载文件夹，看一下真实名字，然后把命令里的名字改成一致。

### 第五步：安装运行环境

第一次使用，需要安装依赖。

在终端里依次复制粘贴下面命令，每粘贴一行按一次回车：

    python3 -m venv .venv

    source .venv/bin/activate

    pip install -r requirements.txt

这一步可能需要等待一会儿。

如果没有出现红色错误，就说明安装成功。

### 第六步：运行脱敏

如果你的 PDF 放在桌面的“原始PDF”文件夹里，想把结果放到桌面的“脱敏PDF”文件夹里，请运行：

    python pdf_desensitize.py ~/Desktop/原始PDF ~/Desktop/脱敏PDF

处理完成后，打开桌面上的：

- 脱敏PDF

你会看到类似文件：

- redacted-001.pdf
- redaction-summary.json

你真正要使用的是：

- redacted-001.pdf

### 第七步：检查结果

请打开 `redacted-001.pdf`，逐页检查：

- 姓名是否被遮盖
- 公司名是否被遮盖
- 机构名是否被遮盖
- 地名是否被遮盖
- 标题是否被遮盖
- 是否有图片、印章、手写签名没有处理

如果有漏掉的内容，不要直接对外发送。

### 如果有漏掉的词怎么办？

你可以手动告诉工具要遮盖哪些词。

例如漏掉了“张三”和“北京某某科技有限公司”，可以运行：

    python pdf_desensitize.py ~/Desktop/原始PDF ~/Desktop/脱敏PDF --custom-names 张三 --custom-companies 北京某某科技有限公司

如果有很多词，建议写进一个文本文件，每行一个词。

### 常见问题

#### 1. 为什么有些内容没有被遮盖？

可能原因：

- PDF 是扫描件
- 文字其实是图片
- 内容在印章或水印里
- 手写签名无法识别
- 没有 OCR 文本层
- 自动识别规则没有覆盖到

#### 2. 扫描件怎么办？

请先使用 OCR 工具，把扫描件变成可搜索 PDF，再运行本工具。

#### 3. 这个工具会上传我的文件吗？

不会。这个工具在本地电脑运行，不会主动上传你的 PDF。

#### 4. 可以保证完全脱敏吗？

不能。自动工具不能保证 100% 不漏。正式对外发送前，必须人工复核。

#### 5. `redaction-summary.json` 是什么？

这是处理摘要，不是最终 PDF。一般不用发给别人。

#### 6. `sensitive-redaction-report.md` 是什么？

如果你使用了 `--write-sensitive-report`，会生成本地审计报告。这个文件可能包含原始敏感信息，不要发给别人，不要上传网络。

### 给完全不懂终端的用户

如果你不熟悉终端，请把这份指南发给熟悉电脑的人协助操作。

未来如果项目提供图形界面 App，你就可以像普通软件一样双击使用。

## 安装

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

也可以作为命令行工具安装：

    pip install -e .

## 使用

处理一个文件夹：

    pdf-desensitize ./input-pdfs ./output

处理单个 PDF：

    pdf-desensitize ./contract.pdf ./output

从源码目录直接运行：

    python pdf_desensitize.py ./input-pdfs ./output

手动补充漏检词：

    pdf-desensitize ./input-pdfs ./output --custom-names 陈建国 刘洋 周明华 --custom-companies 万科企业股份有限公司

从文本文件读取手动脱敏词：

    pdf-desensitize ./input-pdfs ./output --custom-words ./example/manual_words_example.txt

如果你确定第一页标题不敏感，可以保留标题：

    pdf-desensitize ./input-pdfs ./output --keep-visible-title

生成本地审计报告：

    pdf-desensitize ./input-pdfs ./output --write-sensitive-report

## 输出文件

默认输出：

    output/
    ├── redacted-001.pdf
    └── redaction-summary.json

`redaction-summary.json` 不包含原始文件名和原始敏感文字，适合随脱敏 PDF 保留。

如果使用 `--write-sensitive-report`，会额外生成：

    output/
    ├── sensitive-redaction-map.json
    └── sensitive-redaction-report.md

这两个文件包含原始文件名、原始姓名、公司名、机构名、地名等，只能用于本地复核，不要上传 GitHub、网盘或发给外部人员。

## 适用范围

适合：

- 可提取文本的 PDF
- 合同、报告、尽调材料中的中文姓名、公司名、机构名、地名辅助脱敏
- 希望保留原版式，只遮盖敏感文字区域的场景

不适合直接依赖：

- 扫描版 PDF 或图片里的文字
- 手写签名、印章、图片水印中的敏感信息
- 需要法律级、合规级保证的最终脱敏流程

对扫描版 PDF，请先使用 OCR 工具生成可搜索文本层，再运行本工具，并人工复核。

## 手动词表格式

每行一个词，`#` 开头为注释：

    # 人名
    张三
    李四

    # 公司名
    北京某科技有限公司
    上海创新集团

## 开发

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    pytest

贡献代码前请阅读 [CONTRIBUTING.md](./CONTRIBUTING.md)。提交 issue 时请勿上传真实敏感 PDF 或真实个人/机构信息。

## 公开发布建议

- 只发布源码、README、测试和不含真实敏感信息的示例
- 不要提交真实输入 PDF、脱敏输出 PDF、本地审计报告
- 发布前运行 `pytest`
- 在 release 包里排除 `__MACOSX`、`.DS_Store`、`output/`、`sensitive-*`

## 许可

MIT License. See [LICENSE](./LICENSE).

## 支持作者

如果这个项目对你有帮助，欢迎给仓库点一个 Star。

也可以通过支付宝支持作者。

<img src="./assets/alipay.png" alt="Alipay QR Code" width="220">

## 关于作者

作者：**XueyouChu**

- GitHub: [MindfulYou](https://github.com/MindfulYou)
- Email: cxy@youshengyu.com

---

# English

PDF Desensitizer is a local PDF redaction tool for Chinese PDF documents. It detects sensitive Chinese terms such as personal names, organizations, full and abbreviated company names, and locations. It applies PDF redaction at the original text coordinates and draws grayscale mosaic overlays while preserving tables, images, headers, footers, and page layout as much as possible.

> Important: automatic detection can miss sensitive content. Always review every page before sharing a redacted PDF.

## Features

- Designed for Chinese PDF redaction scenarios
- Preserves the original PDF page layout instead of rebuilding the document from extracted text
- Applies real PDF redaction to matched text areas, then draws mosaic overlays
- Detects common Chinese personal names, role-labeled names, company full names, company aliases, organization names, and locations
- Uses anonymized output filenames by default, for example `redacted-001.pdf`
- Redacts the first visible title line by default and replaces the PDF metadata title
- Supports manual redaction terms
- Generates a public summary that does not include original filenames or original sensitive terms
- Can optionally generate local audit reports, but those reports contain original sensitive text and must not be published
- Runs locally only; no upload and no network access are required during processing

## Beginner User Guide

This guide is for users who are not familiar with GitHub, Python, or terminal commands.

PDF Desensitizer helps cover sensitive terms such as personal names, company names, organization names, and locations while preserving the original PDF layout as much as possible.

Please note: the current version is not a double-click desktop app. It must be run from the terminal. If you are not comfortable using the terminal, ask someone technical to help you or wait for a future graphical version.

### What is this tool for?

Good for:

- Redacting contracts before external sharing
- Redacting reports before sharing
- Preparing due diligence materials
- Anonymizing case materials
- Covering names, companies, organizations, and locations in PDFs

Do not rely on it alone for:

- Scanned PDFs
- Text inside images
- Handwritten signatures
- Seals or stamps
- Watermarks
- Legal-grade, compliance-grade, or audit-grade final redaction

Always review every page manually before sending files externally.

### Step 1: Download the Project

1. Open:

   https://github.com/MindfulYou/pdf-desensitizer

2. Click the green button:

   Code

3. Click:

   Download ZIP

4. Unzip the downloaded file.

5. You will get a folder named something like:

   pdf-desensitizer-main

### Step 2: Prepare PDF Folders

Create two folders on your Desktop:

- OriginalPDF
- RedactedPDF

Put the PDFs you want to process into:

- OriginalPDF

The processed files will be saved into:

- RedactedPDF

### Step 3: Open Terminal

macOS:

1. Press:

   Command + Space

2. Type:

   Terminal

3. Press Enter.

### Step 4: Enter the Tool Folder

If you unzipped the project into Downloads, run:

    cd ~/Downloads/pdf-desensitizer-main

If the folder name is different, change the command to match the actual folder name.

### Step 5: Install Dependencies

Run these commands one by one:

    python3 -m venv .venv

    source .venv/bin/activate

    pip install -r requirements.txt

Wait for the installation to finish. If there are no red error messages, it is ready.

### Step 6: Redact PDFs

If your PDFs are in `OriginalPDF` on your Desktop and you want results in `RedactedPDF`, run:

    python pdf_desensitize.py ~/Desktop/OriginalPDF ~/Desktop/RedactedPDF

After it finishes, open:

- RedactedPDF

You should see files like:

- redacted-001.pdf
- redaction-summary.json

The file you need is:

- redacted-001.pdf

### Step 7: Review the Result

Open `redacted-001.pdf` and check every page:

- Are personal names covered?
- Are company names covered?
- Are organization names covered?
- Are locations covered?
- Is the title covered?
- Are there images, stamps, seals, or handwritten signatures that were not processed?

If anything is missed, do not send the PDF externally yet.

### What if some terms are missed?

You can manually tell the tool what to cover.

For example:

    python pdf_desensitize.py ~/Desktop/OriginalPDF ~/Desktop/RedactedPDF --custom-names 陈建国 刘洋 --custom-companies 万科企业股份有限公司

For many terms, create a text file with one term per line and use `--custom-words`.

### FAQ

#### 1. Why did some content not get covered?

Possible reasons:

- The PDF is scanned
- The text is actually an image
- The content is inside a stamp or watermark
- The signature is handwritten
- The document has no OCR text layer
- The detection rules did not catch it

#### 2. What should I do with scanned PDFs?

Run OCR first to create a searchable PDF, then use this tool.

#### 3. Does this tool upload my files?

No. It runs locally and does not upload your PDFs.

#### 4. Can it guarantee complete redaction?

No. No automatic tool can guarantee 100% complete redaction. Always review manually before sharing.

#### 5. What is `redaction-summary.json`?

It is a processing summary, not the final PDF.

#### 6. What is `sensitive-redaction-report.md`?

If you use `--write-sensitive-report`, the tool creates a local audit report. It may contain original sensitive information. Do not share it or upload it.

### For Non-Technical Users

If you are not comfortable using the terminal, please ask someone technical to help.

A future graphical desktop app may make this tool easier to use.

## Installation

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

You can also install it as a command line tool:

    pip install -e .

## Usage

Redact a folder of PDFs:

    pdf-desensitize ./input-pdfs ./output

Redact a single PDF:

    pdf-desensitize ./contract.pdf ./output

Run directly from a source checkout:

    python pdf_desensitize.py ./input-pdfs ./output

Add manual terms for missed detections:

    pdf-desensitize ./input-pdfs ./output --custom-names 陈建国 刘洋 周明华 --custom-companies 万科企业股份有限公司

Load manual terms from a text file:

    pdf-desensitize ./input-pdfs ./output --custom-words ./example/manual_words_example.txt

Keep the first visible title line if you know it is not sensitive:

    pdf-desensitize ./input-pdfs ./output --keep-visible-title

Write local audit reports:

    pdf-desensitize ./input-pdfs ./output --write-sensitive-report

## Output Files

Default output:

    output/
    ├── redacted-001.pdf
    └── redaction-summary.json

`redaction-summary.json` does not contain original filenames or original sensitive text, so it can be kept with the redacted PDFs.

If `--write-sensitive-report` is used, these files are also generated:

    output/
    ├── sensitive-redaction-map.json
    └── sensitive-redaction-report.md

These two files contain original filenames, personal names, company names, organization names, locations, and other sensitive terms. Use them only for local review. Do not upload them to GitHub, cloud drives, or share them externally.

## Scope

Suitable for:

- PDFs with extractable text
- Assisted redaction of Chinese personal names, company names, organization names, and locations in contracts, reports, and due diligence materials
- Cases where the original layout should remain unchanged and only sensitive text areas should be covered

Do not rely on it alone for:

- Scanned PDFs or text embedded in images
- Handwritten signatures, seals, stamps, or image watermarks
- Final legal-grade or compliance-grade redaction without human review

For scanned PDFs, run OCR first to create a searchable text layer, then use this tool and review the result manually.

## Manual Terms File

Use one term per line. Lines starting with `#` are comments:

    # Personal names
    张三
    李四

    # Company names
    北京某科技有限公司
    上海创新集团

## Development

    python -m venv .venv
    source .venv/bin/activate
    pip install -e ".[dev]"
    pytest

Please read [CONTRIBUTING.md](./CONTRIBUTING.md) before contributing. Do not upload real sensitive PDFs or real personal/organization information when filing issues.

## Publishing Notes

- Publish only source code, README, tests, and examples without real sensitive data
- Do not commit real input PDFs, redacted output PDFs, or local audit reports
- Run `pytest` before publishing
- Exclude `__MACOSX`, `.DS_Store`, `output/`, and `sensitive-*` from release packages

## License

MIT License. See [LICENSE](./LICENSE).

## Support

If this project helps you, please consider giving it a Star.

You can also support the author via Alipay.

<img src="./assets/alipay.png" alt="Alipay QR Code" width="220">

## About the Author

Created and maintained by **XueyouChu**.

- GitHub: [MindfulYou](https://github.com/MindfulYou)
- Email: cxy@youshengyu.com
