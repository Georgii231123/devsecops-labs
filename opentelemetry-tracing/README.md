# OpenTelemetry Distributed Tracing Lab

End-to-end tracing lab with two HTTP services, OpenTelemetry automatic instrumentation, an OpenTelemetry Collector and Jaeger.

## Request path

`client -> frontend -> backend`

Both application services export OTLP spans to the collector. The collector batches and forwards traces to Jaeger. The CI workflow performs a real request and checks Jaeger's API for both service names.

## Components

- Flask frontend service;
- Flask backend service;
- OpenTelemetry Python instrumentation;
- OpenTelemetry Collector with memory limiter + batch processor;
- Jaeger trace storage/UI;
- explicit service names and deployment environment resource attributes;
- trace context propagation across the frontend/backend HTTP call.

## Run

```bash
cd opentelemetry-tracing
docker compose up --build -d
curl http://localhost:8000/request
```

Jaeger UI: `http://localhost:16686`.

## Why it matters

Metrics can show that latency increased; distributed traces can show which hop consumed that latency. A production setup should additionally define sampling policy, tail sampling for selected errors/latency, retention, PII controls and trace-to-log correlation.
