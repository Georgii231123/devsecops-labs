#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
rm -rf dist .build-a .build-b
mkdir -p dist .build-a .build-b

export CGO_ENABLED=0
export GOFLAGS="-mod=readonly"
export SOURCE_DATE_EPOCH=1704067200

build() {
  local out="$1"
  go build -trimpath -ldflags="-s -w -buildid=" -o "$out/provenance-demo" ./cmd/provenance-demo
}

build .build-a
build .build-b

HASH_A="$(sha256sum .build-a/provenance-demo | awk '{print $1}')"
HASH_B="$(sha256sum .build-b/provenance-demo | awk '{print $1}')"

if [[ "$HASH_A" != "$HASH_B" ]]; then
  echo "reproducible build check failed: $HASH_A != $HASH_B" >&2
  exit 1
fi

install -m 0755 .build-a/provenance-demo dist/provenance-demo
tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner -czf dist/provenance-demo-linux-amd64.tar.gz -C dist provenance-demo
sha256sum dist/provenance-demo-linux-amd64.tar.gz > dist/provenance-demo-linux-amd64.sha256

printf '{"binary_sha256":"%s","reproducible":true}\n' "$HASH_A" > dist/reproducibility.json
rm -rf .build-a .build-b
