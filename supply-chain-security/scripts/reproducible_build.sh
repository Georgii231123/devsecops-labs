#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
rm -rf dist .repro
mkdir -p dist .repro

export CGO_ENABLED=0
export GOFLAGS="-mod=readonly"
export SOURCE_DATE_EPOCH=1704067200

build_once() {
  rm -f .repro/provenance-demo
  go build -buildvcs=false -trimpath -ldflags="-s -w -buildid=" -o .repro/provenance-demo ./cmd/provenance-demo
}

build_once
cp .repro/provenance-demo .repro/build-a
build_once
cp .repro/provenance-demo .repro/build-b

HASH_A="$(sha256sum .repro/build-a | awk '{print $1}')"
HASH_B="$(sha256sum .repro/build-b | awk '{print $1}')"

if [[ "$HASH_A" != "$HASH_B" ]]; then
  echo "reproducible build check failed: $HASH_A != $HASH_B" >&2
  exit 1
fi

install -m 0755 .repro/build-a dist/provenance-demo
tar --sort=name --mtime="@$SOURCE_DATE_EPOCH" --owner=0 --group=0 --numeric-owner -czf dist/provenance-demo-linux-amd64.tar.gz -C dist provenance-demo
sha256sum dist/provenance-demo-linux-amd64.tar.gz > dist/provenance-demo-linux-amd64.sha256

printf '{"binary_sha256":"%s","reproducible":true,"buildvcs":false}\n' "$HASH_A" > dist/reproducibility.json
rm -rf .repro
