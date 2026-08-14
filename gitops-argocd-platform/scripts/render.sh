#!/usr/bin/env bash
set -euo pipefail

env_name="${1:-dev}"
case "$env_name" in
  dev|prod) ;;
  *) echo "environment must be dev or prod" >&2; exit 2 ;;
esac

root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
values="$root/environments/$env_name/values.yaml"

if grep -Eq 'tag:[[:space:]]*["'"']?latest["'"']?[[:space:]]*$' "$values"; then
  echo "refusing mutable latest image tag" >&2
  exit 1
fi

helm lint "$root/charts/demo-service" -f "$values"
helm template "demo-$env_name" "$root/charts/demo-service" -f "$values"
