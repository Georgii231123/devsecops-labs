#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
latest="$(find "${BACKUP_DIR:-$ROOT/backups}" -maxdepth 1 -type f -name '*.dump' -printf '%T@ %p\n' | sort -nr | head -1 | cut -d' ' -f2-)"
if [[ -z "$latest" ]]; then
  echo "no backup found" >&2
  exit 1
fi

echo "verifying $latest"
"$ROOT/scripts/restore.sh" "$latest"
DB="${POSTGRES_DB:-appdb}"
USER="${POSTGRES_USER:-appuser}"
docker compose -f "$ROOT/docker-compose.yml" exec -T postgres psql -U "$USER" -d "$DB" -c "SELECT count(*) AS restored_accounts FROM accounts;"
