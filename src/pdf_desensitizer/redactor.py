"""PDF layout-preserving redaction engine."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from .detector import find_sensitive_items


@dataclass
class RedactionHit:
    text: str
    kind: str
    page: int
    rect_count: int


@dataclass
class FileRedactionReport:
    document_id: str
    input_file: str
    output_file: str
    pages: int
    hits: list[RedactionHit] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def redaction_count(self) -> int:
        return sum(hit.rect_count for hit in self.hits)


@dataclass
class BatchRedactionReport:
    files: list[FileRedactionReport] = field(default_factory=list)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_redactions(self) -> int:
        return sum(file.redaction_count for file in self.files)


def _load_fitz():
    try:
        import fitz  # type: ignore
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing dependency: PyMuPDF. Install it with `pip install -r requirements.txt`."
        ) from exc
    return fitz


def _read_manual_words(path: str | Path | None) -> tuple[set[str], set[str]]:
    names: set[str] = set()
    companies: set[str] = set()
    if not path:
        return names, companies

    words_path = Path(path)
    if not words_path.is_file():
        raise FileNotFoundError(f"Manual words file not found: {words_path}")

    for raw_line in words_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.endswith(("公司", "集团", "企业", "有限公司", "事务所")):
            companies.add(line)
        else:
            names.add(line)
    return names, companies


def _safe_warning(page_number: int) -> str:
    return f"Page {page_number}: a detected term did not locate coordinates"


def _dedupe_terms(terms: Iterable[tuple[str, str]]) -> list[tuple[str, str]]:
    unique: dict[str, str] = {}
    for text, kind in terms:
        text = text.strip()
        if not text:
            continue
        unique[text] = kind
    return sorted(unique.items(), key=lambda item: (-len(item[0]), item[0]))


def _expand_rect(rect, padding: float):
    rect.x0 -= padding
    rect.y0 -= padding
    rect.x1 += padding
    rect.y1 += padding
    return rect


def _first_page_title_terms(page) -> list[tuple[str, str]]:
    terms: list[tuple[str, str]] = []
    data = page.get_text("dict")
    for block in data.get("blocks", []):
        for line in block.get("lines", []):
            text = "".join(span.get("text", "") for span in line.get("spans", [])).strip()
            if text:
                terms.append((text, "title"))
                return terms
    return terms


def _draw_mosaic(page, rect, block_size: float, colors: list[tuple[float, float, float]]) -> None:
    fitz = _load_fitz()
    width = max(rect.width, block_size)
    height = max(rect.height, block_size)
    cols = max(1, int(width / block_size) + 1)
    rows = max(1, int(height / block_size) + 1)
    for row in range(rows):
        for col in range(cols):
            x0 = rect.x0 + col * block_size
            y0 = rect.y0 + row * block_size
            tile = fitz.Rect(
                x0,
                y0,
                min(x0 + block_size, rect.x1),
                min(y0 + block_size, rect.y1),
            )
            if tile.is_empty:
                continue
            color = colors[(row + col) % len(colors)]
            page.draw_rect(tile, color=color, fill=color, overlay=True)


def redact_pdf(
    input_pdf: str | Path,
    output_pdf: str | Path,
    *,
    custom_names: Iterable[str] | None = None,
    custom_companies: Iterable[str] | None = None,
    custom_words_file: str | Path | None = None,
    document_id: str = "document-001",
    redact_visible_title: bool = True,
    padding: float = 1.5,
    mosaic_block_size: float = 3.2,
) -> FileRedactionReport:
    """Redact one PDF by covering matched text areas while preserving page layout."""

    fitz = _load_fitz()
    input_path = Path(input_pdf)
    output_path = Path(output_pdf)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    manual_names, manual_companies = _read_manual_words(custom_words_file)
    manual_names.update(custom_names or [])
    manual_companies.update(custom_companies or [])

    doc = fitz.open(str(input_path))
    doc.set_metadata(
        {
            "title": document_id,
            "author": "",
            "subject": "",
            "keywords": "",
            "creator": "pdf-desensitizer",
            "producer": "pdf-desensitizer",
        }
    )
    report = FileRedactionReport(
        document_id=document_id,
        input_file=input_path.name,
        output_file=output_path.name,
        pages=doc.page_count,
    )

    page_terms: list[list[tuple[str, str]]] = []
    for page in doc:
        text = page.get_text("text") or ""
        detected = find_sensitive_items(text)
        names = set(detected.names)
        companies = set(detected.companies)
        organizations = set(detected.organizations)
        aliases = set(detected.aliases)
        locations = set(detected.locations)
        contract_terms = set(detected.contract_terms)
        names.update(name for name in manual_names if name in text)
        companies.update(company for company in manual_companies if company in text)
        terms = (
            [(value, "name") for value in names]
            + [(value, "company") for value in companies]
            + [(value, "organization") for value in organizations]
            + [(value, "alias") for value in aliases]
            + [(value, "location") for value in locations]
            + [(value, "contract") for value in contract_terms]
        )
        if redact_visible_title and page.number == 0:
            terms.extend(_first_page_title_terms(page))
        page_terms.append(
            _dedupe_terms(terms)
        )

    page_rects: list[list[tuple[str, str, object]]] = []
    for page, terms in zip(doc, page_terms):
        rects_for_page: list[tuple[str, str, object]] = []
        for term, kind in terms:
            rects = page.search_for(term)
            if not rects:
                report.warnings.append(_safe_warning(page.number + 1))
                continue
            for rect in rects:
                expanded = _expand_rect(fitz.Rect(rect), padding)
                page.add_redact_annot(expanded, fill=(0.88, 0.88, 0.88))
                rects_for_page.append((term, kind, expanded))
            report.hits.append(
                RedactionHit(text=term, kind=kind, page=page.number + 1, rect_count=len(rects))
            )
        page_rects.append(rects_for_page)

    for page in doc:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE)

    mosaic_colors = [(0.24, 0.24, 0.24), (0.42, 0.42, 0.42), (0.62, 0.62, 0.62), (0.78, 0.78, 0.78)]
    for page, rects_for_page in zip(doc, page_rects):
        for _term, _kind, rect in rects_for_page:
            _draw_mosaic(page, rect, mosaic_block_size, mosaic_colors)

    doc.save(str(output_path), garbage=4, deflate=True, clean=True)
    doc.close()
    return report


def redact_path(
    input_path: str | Path,
    output_dir: str | Path,
    *,
    custom_names: Iterable[str] | None = None,
    custom_companies: Iterable[str] | None = None,
    custom_words_file: str | Path | None = None,
    redact_visible_title: bool = True,
    padding: float = 1.5,
    mosaic_block_size: float = 3.2,
) -> BatchRedactionReport:
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if input_path.is_file():
        pdf_files = [input_path]
    else:
        pdf_files = sorted(list(input_path.glob("*.pdf")) + list(input_path.glob("*.PDF")))

    if not pdf_files:
        raise FileNotFoundError(f"No PDF files found: {input_path}")

    batch = BatchRedactionReport()
    for index, pdf_file in enumerate(pdf_files, start=1):
        document_id = f"document-{index:03d}"
        output_pdf = output_dir / f"redacted-{index:03d}.pdf"
        batch.files.append(
            redact_pdf(
                pdf_file,
                output_pdf,
                custom_names=custom_names,
                custom_companies=custom_companies,
                custom_words_file=custom_words_file,
                document_id=document_id,
                redact_visible_title=redact_visible_title,
                padding=padding,
                mosaic_block_size=mosaic_block_size,
            )
        )
    return batch


def write_summary_json(report: BatchRedactionReport, output_dir: str | Path) -> Path:
    output_path = Path(output_dir) / "redaction-summary.json"
    data = {
        "total_files": report.total_files,
        "total_redactions": report.total_redactions,
        "files": [
            {
                "document_id": file.document_id,
                "output_file": file.output_file,
                "pages": file.pages,
                "redactions": file.redaction_count,
                "warnings": file.warnings,
            }
            for file in report.files
        ],
    }
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
