#!/usr/bin/env bash
set -euo pipefail

for _ in {1..40}; do
  if curl -fsS http://localhost:8000/healthz >/dev/null; then break; fi
  sleep 2
done

curl -fsS http://localhost:8000/request | grep -q 'simulated-work'
sleep 5
services="$(curl -fsS --retry 10 --retry-delay 2 http://localhost:16686/api/services)"
grep -q 'frontend' <<<"$services"
grep -q 'backend' <<<"$services"
echo "OpenTelemetry end-to-end trace smoke test passed"
