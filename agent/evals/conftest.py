"""Eval test configuration — real model, opt-in only.

Evals are gated behind the 'eval' marker. They are NOT run during
standard `make agent-test`. To run them:

    pytest -m eval agent/evals/

Or with explicit flag:

    pytest -m eval --run-evals agent/evals/
"""

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--run-evals",
        action="store_true",
        default=False,
        help="Run eval tests (requires live model credentials).",
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--run-evals", default=False):
        skip_eval = pytest.mark.skip(reason="Pass --run-evals to run eval tests.")
        for item in items:
            if "eval" in item.keywords:
                item.add_marker(skip_eval)
