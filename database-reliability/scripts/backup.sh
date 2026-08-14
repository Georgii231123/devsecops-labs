#!/usr/bin/env bash
set -euo pipefail

DB="${POSTGRES_DB:-appdb}"
USER="${POSTGRES_USER:-appuser}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUP_DIR="${BACKUP_DIR:-$ROOT/backups}"
mkdir -p "$BACKUP_DIR"
file="$BACKUP_DIR/${DB}_$(date -u +%Y%m%dT%H%M%SZ).dump"

docker compose -f "$ROOT/docker-compose.yml" exec -T postgres pg_dump -U "$USER" -d "$DB" --format=custom > "$file"
test -s "$file"
echo "$file"
