"""Report writers for redaction runs."""

from __future__ import annotations

import json
from pathlib import Path

from .redactor import BatchRedactionReport


def write_sensitive_report(report: BatchRedactionReport, output_dir: str | Path) -> tuple[Path, Path]:
    """Write reports that contain original sensitive text.

    These files are useful for local auditing but should not be shared publicly.
    """

    output_dir = Path(output_dir)
    mapping_path = output_dir / "sensitive-redaction-map.json"
    markdown_path = output_dir / "sensitive-redaction-report.md"

    data = {
        "warning": "This file contains original sensitive text. Do not publish it.",
        "files": [
            {
                "document_id": file.document_id,
                "input_file": file.input_file,
                "output_file": file.output_file,
                "hits": [
                    {
                        "text": hit.text,
                        "kind": hit.kind,
                        "page": hit.page,
                        "rect_count": hit.rect_count,
                    }
                    for hit in file.hits
                ],
                "warnings": file.warnings,
            }
            for file in report.files
        ],
    }
    mapping_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Sensitive Redaction Report",
        "",
        "> This report contains original sensitive text. Do not publish it.",
        "",
    ]
    for file in report.files:
        lines.append(f"## {file.document_id}")
        lines.append("")
        lines.append(f"- Original input file: `{file.input_file}`")
        lines.append(f"- Output: `{file.output_file}`")
        lines.append(f"- Pages: {file.pages}")
        lines.append(f"- Redaction rectangles: {file.redaction_count}")
        lines.append("")
        if file.hits:
            lines.extend(["| Page | Type | Text | Rectangles |", "|---:|---|---|---:|"])
            for hit in file.hits:
                lines.append(f"| {hit.page} | {hit.kind} | {hit.text} | {hit.rect_count} |")
            lines.append("")
        if file.warnings:
            lines.append("Warnings:")
            for warning in file.warnings:
                lines.append(f"- {warning}")
            lines.append("")

    markdown_path.write_text("\n".join(lines), encoding="utf-8")
    return mapping_path, markdown_path
