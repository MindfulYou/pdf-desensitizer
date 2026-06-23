.PHONY: install dev test clean demo

PYTHON ?= python

install:
	$(PYTHON) -m pip install -r requirements.txt

dev:
	$(PYTHON) -m pip install -e .
	$(PYTHON) -m pip install pytest

test:
	$(PYTHON) -m pytest

demo:
	$(PYTHON) scripts/create_demo_pdf.py example/demo_contract.pdf
	$(PYTHON) pdf_desensitize.py example/demo_contract.pdf example_output --write-sensitive-report

clean:
	rm -rf build dist *.egg-info .pytest_cache example_output output test_output
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null; true

