# Incident Runbook

## Service down

1. Check `docker compose ps` and the application healthcheck.
2. Inspect `docker compose logs --tail=200 app`.
3. Verify Prometheus target state at `/targets`.
4. Restart only after collecting enough evidence to understand the failure.
5. Confirm `up{job="app"}` returns to `1` and traffic succeeds.

## High error rate

1. Check the error-ratio and request-rate panels together.
2. Compare recent deployment/configuration changes.
3. Inspect application logs and the `/work` endpoint behavior.
4. If a real deployment caused the increase, roll back to the last known-good version.
5. Keep monitoring until the rolling error ratio returns below the threshold.

## High latency

1. Check p50/p95/p99 behavior and request rate.
2. Determine whether latency follows CPU/memory saturation or only one endpoint.
3. Check downstream dependencies before scaling blindly.
4. Mitigate by rollback, capacity increase or dependency isolation depending on evidence.

## After recovery

Record impact, timeline, root cause, detection quality and corrective actions. Prefer changes that prevent recurrence or reduce time-to-detect rather than only documenting the incident.
