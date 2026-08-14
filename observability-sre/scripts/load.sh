#!/usr/bin/env bash
set -euo pipefail

URL="${1:-http://localhost:8080/work}"
for _ in {1..300}; do
  curl -fsS "$URL" >/dev/null || true
  sleep 0.05
done
