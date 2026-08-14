# Service Level Objectives

## Availability SLO

Target: **99.5% successful requests over 30 days**.

SLI:

```promql
1 - (sum(rate(http_requests_total{status=~"5.."}[5m])) / sum(rate(http_requests_total[5m])))
```

The monthly error budget for 99.5% availability is 0.5%. Short-window alerts in this lab are intentionally more sensitive so failures are visible during a demo.

## Latency objective

Target: **95% of requests below 500 ms** for the demo workload.

```promql
histogram_quantile(0.95, sum by (le) (rate(http_request_duration_seconds_bucket[5m])))
```

## Alert philosophy

Page/critical alerts should represent user-visible impact or total loss of telemetry. Warning alerts indicate degraded behavior that requires investigation but not necessarily immediate escalation.
