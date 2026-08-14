#!/usr/bin/env bash
set -euo pipefail

DB="${POSTGRES_DB:-appdb}"
USER="${POSTGRES_USER:-appuser}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for migration in "$ROOT"/migrations/*.sql; do
  version="$(basename "$migration" .sql)"
  applied="$(docker compose -f "$ROOT/docker-compose.yml" exec -T postgres psql -U "$USER" -d "$DB" -Atc "SELECT 1 FROM schema_migrations WHERE version='$version'" || true)"
  if [[ "$applied" == "1" ]]; then
    echo "skip $version"
    continue
  fi
  echo "apply $version"
  cat "$migration" | docker compose -f "$ROOT/docker-compose.yml" exec -T postgres psql -v ON_ERROR_STOP=1 -U "$USER" -d "$DB"
  docker compose -f "$ROOT/docker-compose.yml" exec -T postgres psql -v ON_ERROR_STOP=1 -U "$USER" -d "$DB" -c "INSERT INTO schema_migrations(version) VALUES ('$version')"
done
