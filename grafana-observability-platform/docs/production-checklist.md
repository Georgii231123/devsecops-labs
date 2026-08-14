# Production checklist

Before treating an LGTM deployment as production-ready, review at least:

- authenticated ingress and TLS for every externally reachable API;
- tenant isolation and authorization;
- durable object storage instead of local filesystem backends;
- multi-zone failure domains and replication strategy;
- retention, compaction and storage lifecycle policies;
- resource requests/limits and workload-specific sizing;
- alerting for ingestion failures, query saturation, storage errors and cardinality growth;
- backup/export strategy for Grafana configuration and dashboards;
- upgrade compatibility and rollback procedure;
- cost controls for logs, metrics cardinality and trace retention.
