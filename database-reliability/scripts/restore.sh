#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $0 backup.dump" >&2
  exit 2
fi

DB="${POSTGRES_DB:-appdb}"
USER="${POSTGRES_USER:-appuser}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
backup="$1"

test -s "$backup"
cat "$backup" | docker compose -f "$ROOT/docker-compose.yml" exec -T postgres pg_restore -U "$USER" -d "$DB" --clean --if-exists --no-owner --no-privileges
