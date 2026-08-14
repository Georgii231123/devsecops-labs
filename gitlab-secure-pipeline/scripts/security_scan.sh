#!/usr/bin/env sh
set -eu

ruff check .
ruff format --check .
pytest -q
bandit -r app -q -ll
pip-audit -r requirements.txt
