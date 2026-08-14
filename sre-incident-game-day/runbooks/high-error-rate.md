# Runbook: ApplicationFailureMode / High5xxVolume

## Detection

Confirm that `ApplicationFailureMode` is firing in Prometheus and inspect `app_requests_total{status="5xx"}`. Record the first alert timestamp before changing service state.

## Triage

1. Verify `/healthz` is reachable.
2. Verify Prometheus can scrape the target.
3. Confirm the failure is application-level rather than a complete process outage.
4. Check whether the runtime mode file contains `errors`.

## Containment

Stop additional failure injection and avoid unrelated changes while the paging condition is active.

## Remediation

Restore the runtime mode to `healthy`. In a production system this step would map to rollback, feature-flag disablement, dependency failover or configuration correction.

## Verification

Send successful requests, confirm `app_failure_mode` returns to `0`, and wait until `ApplicationFailureMode` is no longer firing.

## Rollback

If remediation introduces a new fault, restore the previous known-good deployment/configuration and re-run the verification steps.

## Post-incident

Preserve detection and recovery timestamps, calculate MTTA/MTTR, document root cause and add follow-up actions that reduce recurrence or detection time.
