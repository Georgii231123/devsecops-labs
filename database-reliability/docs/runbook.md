# PostgreSQL operations runbook

## Database or exporter down

1. Check `docker compose ps` and PostgreSQL health state.
2. Inspect PostgreSQL logs before restarting.
3. Run `pg_isready` and a simple read-only query.
4. Distinguish database failure from exporter/monitoring failure.
5. If data recovery is needed, preserve the failed volume before restore work.

## High connection usage

1. Inspect active vs idle sessions in `pg_stat_activity`.
2. Identify application/user sources and long-running transactions.
3. Check connection-pool limits before raising PostgreSQL `max_connections`.
4. Resolve leaks or pool pressure rather than only increasing the ceiling.

## Backup restore drill

1. Select a known backup and record its timestamp/size.
2. Restore into an isolated database whenever possible.
3. Run schema and row-level sanity checks.
4. Record restore duration and compare it with the RTO target.
5. Treat an untested backup as an unverified recovery mechanism.
