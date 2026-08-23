.PHONY: validate validate-schemas visualize wiki-lint install clean agent-test tool-test agent-run agent-web agent-eval

PYTHON := python3
VENV   := .venv
PIP    := $(VENV)/bin/pip
PY     := $(VENV)/bin/python

# ── Setup ──────────────────────────────────────────────────────────────────────

install:
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	@echo "✓ Dependencies installed in $(VENV)"

# ── Ontology ───────────────────────────────────────────────────────────────────

validate:
	$(PY) tools/validate/validate.py

# ── Artifact layer ─────────────────────────────────────────────────────────────

validate-schemas:
	$(PY) tools/validate/validate_schemas.py

visualize:
	$(PY) tools/visualize/visualize.py
	@echo "Output → docs/generated/"

# ── Wiki ───────────────────────────────────────────────────────────────────────

wiki-lint:
	@echo "Run: /llm-wiki lint"

# ── Agent ──────────────────────────────────────────────────────────────────────

agent-test:
	$(PY) -m pytest agent/tests/ -v

tool-test:
	$(PY) -m pytest tools/tests/ -v

agent-run:
	$(PY) -m agent --templates-dir templates/ --output-dir output/

agent-eval:
	$(PY) -m pytest agent/evals/ --run-evals -v

# ── Clean ──────────────────────────────────────────────────────────────────────

clean:
	rm -rf docs/generated __pycache__ .pytest_cache output/
