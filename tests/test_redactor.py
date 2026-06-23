from pathlib import Path

import fitz

from pdf_desensitizer.redactor import redact_pdf, redact_path, write_summary_json


def _make_pdf(path: Path, text: str) -> None:
    doc = fitz.open()
    page = doc.new_page(width=420, height=240)
    page.insert_text((36, 48), text, fontsize=12)
    doc.save(path)
    doc.close()


def _extract_text(path: Path) -> str:
    doc = fitz.open(path)
    text = "\n".join(page.get_text("text") for page in doc)
    doc.close()
    return text


def test_redact_pdf_removes_manual_sensitive_text_and_sets_metadata(tmp_path):
    source = tmp_path / "real-company-contract.pdf"
    output = tmp_path / "redacted.pdf"
    _make_pdf(source, "Confidential Contract\nAlice works with SecretCorp in Beijing.")

    report = redact_pdf(
        source,
        output,
        custom_names=["Alice"],
        custom_companies=["SecretCorp", "Beijing"],
        document_id="document-999",
        redact_visible_title=True,
    )

    assert output.exists()
    assert report.document_id == "document-999"
    assert report.output_file == "redacted.pdf"
    assert report.redaction_count >= 3

    redacted_text = _extract_text(output)
    assert "Confidential Contract" not in redacted_text
    assert "Alice" not in redacted_text
    assert "SecretCorp" not in redacted_text
    assert "Beijing" not in redacted_text

    doc = fitz.open(output)
    metadata = doc.metadata
    doc.close()
    assert metadata["title"] == "document-999"


def test_redact_path_uses_anonymized_output_names_and_public_summary(tmp_path):
    input_dir = tmp_path / "input"
    output_dir = tmp_path / "output"
    input_dir.mkdir()
    _make_pdf(input_dir / "sensitive-original-name.pdf", "Title\nBob met AcmeCorp in Shanghai.")

    report = redact_path(
        input_dir,
        output_dir,
        custom_names=["Bob"],
        custom_companies=["AcmeCorp", "Shanghai"],
    )
    summary_path = write_summary_json(report, output_dir)

    assert (output_dir / "redacted-001.pdf").exists()
    summary = summary_path.read_text(encoding="utf-8")
    assert "sensitive-original-name" not in summary
    assert "Bob" not in summary
    assert "AcmeCorp" not in summary
    assert "redacted-001.pdf" in summary

