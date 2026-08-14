#!/usr/bin/env bash
set -euo pipefail

compose=(docker compose -f "$(dirname "$0")/docker-compose.yml")
"${compose[@]}" up -d

for node in rabbit1 rabbit2 rabbit3; do
  for _ in {1..40}; do
    if "${compose[@]}" exec -T "$node" rabbitmq-diagnostics -q ping >/dev/null 2>&1; then break; fi
    sleep 2
  done
done

for node in rabbit2 rabbit3; do
  "${compose[@]}" exec -T "$node" rabbitmqctl stop_app
  "${compose[@]}" exec -T "$node" rabbitmqctl reset
  "${compose[@]}" exec -T "$node" rabbitmqctl join_cluster rabbit@rabbit1
  "${compose[@]}" exec -T "$node" rabbitmqctl start_app
done

"${compose[@]}" exec -T rabbit1 rabbitmqctl cluster_status
