#!/usr/bin/env bash
set -euo pipefail

docker compose exec -T \
  -e VAULT_ADDR=http://127.0.0.1:8200 \
  -e VAULT_TOKEN=dev-root \
  vault vault audit enable file file_path=stdout 2>/dev/null || true
