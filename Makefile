.PHONY: validate validate-schemas visualize wiki-lint install clean agent-test tool-test agent-run agent-web agent-eval agent-eval-live

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
	$(PY) -m agent --templates-dir domains/pm/templates/ --output-dir output/

agent-web:
	TEMPLATES_DIR=$(or $(TEMPLATES_DIR),domains/pm/templates/) OUTPUT_DIR=$(or $(OUTPUT_DIR),output/) $(VENV)/bin/adk web agent/

agent-eval:
	$(PY) -m pytest agent/evals/ -v

agent-eval-live:
	$(PY) -m pytest agent/evals/ --run-evals -v

# ── Clean ──────────────────────────────────────────────────────────────────────

clean:
	rm -rf docs/generated __pycache__ .pytest_cache output/
