#!/usr/bin/env sh
set -eu

ruff check --fix-only .
ruff format .
git diff -- . ':!autofix.patch' > autofix.patch

if [ -s autofix.patch ]; then
  echo "Safe deterministic fixes are available in autofix.patch"
  cat autofix.patch
else
  echo "No safe autofixes are required."
fi
