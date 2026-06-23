import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "create_demo_pdf.py"
spec = importlib.util.spec_from_file_location("create_demo_pdf", SCRIPT_PATH)
create_demo_pdf = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(create_demo_pdf)


def test_find_cjk_font_returns_path_or_none():
    font = create_demo_pdf.find_cjk_font()
    assert font is None or Path(font).exists()

