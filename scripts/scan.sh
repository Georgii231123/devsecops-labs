#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "[1/3] Conftest policy gate"
docker run --rm -v "${PWD}:/project" -w /project \
  openpolicyagent/conftest:latest \
  test k8s/hardened --policy policy

echo "[2/3] Trivy config scan"
docker run --rm -v "${PWD}:/project" \
  aquasec/trivy:latest \
  config --severity HIGH,CRITICAL --exit-code 0 /project/k8s/hardened

echo "[3/3] Checkov scan"
docker run --rm -v "${PWD}:/project" \
  bridgecrew/checkov:latest \
  -d /project/k8s/hardened --framework kubernetes --compact --soft-fail

echo "Security scan complete"
