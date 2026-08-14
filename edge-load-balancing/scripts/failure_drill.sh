#!/usr/bin/env bash
set -euo pipefail

wait_url() {
  local url="$1"
  for _ in {1..40}; do
    if curl -fsS "$url" >/dev/null; then return 0; fi
    sleep 1
  done
  return 1
}

wait_url http://localhost:8080/
wait_url http://localhost:8081/

for port in 8080 8081; do
  responses=""
  for _ in {1..12}; do responses+="$(curl -fsS "http://localhost:${port}/")"; done
  grep -q backend1 <<<"$responses"
  grep -q backend2 <<<"$responses"
done

docker compose stop backend1
sleep 6
for port in 8080 8081; do
  for _ in {1..5}; do
    curl -fsS "http://localhost:${port}/" | grep -q backend2
  done
done

echo "Nginx and HAProxy backend failure drill passed"
