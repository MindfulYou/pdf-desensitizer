"""Command line interface."""

from __future__ import annotations

import argparse
import sys

from .redactor import redact_path, write_summary_json
from .reports import write_sensitive_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf-desensitize",
        description="Redact Chinese names and company names in PDFs while preserving original layout.",
    )
    parser.add_argument("input", help="Input PDF file or folder containing PDF files")
    parser.add_argument("output", help="Output folder")
    parser.add_argument("--custom-names", nargs="*", default=[], help="Extra person names to redact")
    parser.add_argument("--custom-companies", nargs="*", default=[], help="Extra company names to redact")
    parser.add_argument("--custom-words", default=None, help="Text file with one manual redaction word per line")
    parser.add_argument(
        "--keep-visible-title",
        action="store_true",
        help="Do not automatically redact the first visible title line on page 1",
    )
    parser.add_argument("--padding", type=float, default=1.5, help="Redaction rectangle padding in PDF points")
    parser.add_argument("--mosaic-block-size", type=float, default=3.2, help="Mosaic tile size in PDF points")
    parser.add_argument(
        "--write-sensitive-report",
        action="store_true",
        help="Write local audit reports containing original sensitive text. Do not publish those files.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        report = redact_path(
            args.input,
            args.output,
            custom_names=args.custom_names,
            custom_companies=args.custom_companies,
            custom_words_file=args.custom_words,
            redact_visible_title=not args.keep_visible_title,
            padding=args.padding,
            mosaic_block_size=args.mosaic_block_size,
        )
        summary = write_summary_json(report, args.output)
        print(f"Done. Processed {report.total_files} PDF file(s).")
        print(f"Redaction rectangles: {report.total_redactions}")
        print(f"Public summary: {summary}")
        if args.write_sensitive_report:
            mapping, markdown = write_sensitive_report(report, args.output)
            print("Sensitive local audit files were written. Do not publish them:")
            print(f"- {mapping}")
            print(f"- {markdown}")
        return 0
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
