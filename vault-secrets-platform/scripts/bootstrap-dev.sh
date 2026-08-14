#!/usr/bin/env bash
set -euo pipefail

compose=(docker compose)
"${compose[@]}" exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root vault vault secrets enable -path=secret kv-v2 2>/dev/null || true
"${compose[@]}" exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root vault vault kv put secret/demo-app username=demo password=rotation-required
cat policies/app-read.hcl | "${compose[@]}" exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root vault vault policy write demo-app-read -
"${compose[@]}" exec -T -e VAULT_ADDR=http://127.0.0.1:8200 -e VAULT_TOKEN=dev-root vault vault kv get -field=username secret/demo-app | grep -qx demo

echo "Vault smoke test passed"
