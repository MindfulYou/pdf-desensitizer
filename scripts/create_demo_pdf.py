#!/usr/bin/env python3
"""Create a small demo PDF with synthetic data only."""

from __future__ import annotations

import sys
from pathlib import Path


def find_cjk_font() -> str | None:
    candidates = [
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/PingFang.ttc",
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "C:/Windows/Fonts/msyh.ttc",
        "C:/Windows/Fonts/simsun.ttc",
    ]
    for candidate in candidates:
        if Path(candidate).exists():
            return candidate
    return None


def main() -> int:
    try:
        import fitz  # type: ignore
    except ModuleNotFoundError:
        print("PyMuPDF is required. Install dependencies with `pip install -r requirements.txt`.", file=sys.stderr)
        return 1

    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("example/demo_contract.pdf")
    output.parent.mkdir(parents=True, exist_ok=True)
    font_file = find_cjk_font()
    if not font_file:
        print("No CJK font found for demo generation.", file=sys.stderr)
        return 1

    doc = fitz.open()
    page = doc.new_page(width=595, height=842)
    lines = [
        "保密合作协议",
        "",
        "甲方：王大力（北京某科技有限公司CEO）",
        "乙方：赵敏（上海创新集团副总裁）",
        "项目负责人：陈建国",
        "技术顾问：刘洋",
        "法务审核：周明华、吴小红",
        "涉及单位：华为技术有限公司",
        "协作方：阿里巴巴集团、深圳市腾讯计算机系统有限公司",
        "本协议由马超草拟，经黄磊先生审批后交由京东集团备案。",
        "特此感谢万科企业股份有限公司与小米科技有限责任公司的技术支持。",
    ]
    y = 82
    for line in lines:
        if line:
            page.insert_text((72, y), line, fontsize=12, fontname="cjk", fontfile=font_file)
        y += 22
    page.draw_rect(fitz.Rect(72, 380, 520, 480), color=(0, 0, 0), width=0.8)
    page.draw_line(fitz.Point(72, 430), fitz.Point(520, 430), color=(0, 0, 0), width=0.5)
    page.draw_line(fitz.Point(296, 380), fitz.Point(296, 480), color=(0, 0, 0), width=0.5)
    page.insert_text((90, 410), "表格和图形应保持不动", fontsize=12, fontname="cjk", fontfile=font_file)
    page.insert_text((315, 410), "只遮盖命中文字区域", fontsize=12, fontname="cjk", fontfile=font_file)
    doc.save(str(output), garbage=4, deflate=True)
    doc.close()
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
