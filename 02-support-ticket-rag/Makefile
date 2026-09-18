.PHONY: setup run test demo

PYTHON := .venv/bin/python
PIP := .venv/bin/pip
LLM_PROVIDER ?= mock

setup:
	python3 -m venv .venv
	$(PIP) install -r requirements.txt

run:
	LLM_PROVIDER=$(LLM_PROVIDER) $(PYTHON) -m uvicorn src.api:app --host 127.0.0.1 --port 8000

test:
	$(PYTHON) -m pytest -q

demo:
	LLM_PROVIDER=$(LLM_PROVIDER) $(PYTHON) -m src.rag_pipeline
