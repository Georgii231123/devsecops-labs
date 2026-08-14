#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

CONFTEST_IMAGE="${CONFTEST_IMAGE:-openpolicyagent/conftest:v0.69.0}"
TRIVY_IMAGE="${TRIVY_IMAGE:-aquasec/trivy:0.74.0}"
CHECKOV_IMAGE="${CHECKOV_IMAGE:-bridgecrew/checkov:3.3.9}"

echo "[1/3] Conftest policy gate"
docker run --rm -v "${PWD}:/project" -w /project \
  "$CONFTEST_IMAGE" \
  test k8s/hardened --policy policy

echo "[2/3] Trivy config scan"
docker run --rm -v "${PWD}:/project" \
  "$TRIVY_IMAGE" \
  config --severity HIGH,CRITICAL --exit-code 0 /project/k8s/hardened

echo "[3/3] Checkov scan"
docker run --rm -v "${PWD}:/project" \
  "$CHECKOV_IMAGE" \
  -d /project/k8s/hardened --framework kubernetes --compact --soft-fail

echo "Security scan complete"
