# Projects

The repository is split into independent labs. Each directory keeps its own runtime/configuration files and README; the root Kubernetes Policy-as-Code lab uses `k8s/` and `policy/` directly.

## Kubernetes and platform engineering

- **Kubernetes Policy-as-Code Security Lab** — OPA/Conftest policy gates against vulnerable and hardened manifests.
- **Platform Engineering Golden Path** — service scaffolding with CI, Docker, Kubernetes and ownership metadata.
- **GitOps Delivery Platform** — Helm + Argo CD ApplicationSet promotion between environments.
- **Kubernetes Production Operations** — PDB, HPA, topology spread, quotas, probes and operational runbooks.
- **AWS EKS Production Platform** — private multi-AZ EKS baseline with KMS, IAM and audit logging.
- **Istio Service Mesh Security** — strict mTLS, authorization, traffic policy and canary routing.
- **Multi-Cluster GitOps Platform** — management/workload clusters, fleet placement and drift reconciliation.
- **Kubernetes Admission Control** — Kyverno validation, mutation and generated defaults.
- **Kubernetes Operator Platform** — Go/controller-runtime reconciliation for a custom `WebService` CRD.
- **Internal Developer Portal** — Backstage-style catalog, ownership and self-service service templates.
- **eBPF Runtime Security** — Tetragon tracing/enforcement policies and runtime event triage.
- **Kubernetes Multi-Tenant Platform** — tenant generation, RBAC, quotas, Pod Security and network isolation.

## CI/CD and software supply chain

- **GitLab Secure Pipeline Lab** — test, SAST, SCA, secret scanning, image scanning, SBOM and deterministic autofix preview.
- **Jenkins CI/CD Platform** — JCasC, Shared Library and controlled artifact promotion.
- **Reusable GitHub Actions Secure CI** — a reusable quality/security workflow with a self-test consumer.
- **Software Supply Chain Security** — reproducible build checks, CycloneDX SBOM, Cosign verification and build provenance.

## Cloud, infrastructure and identity

- **Cloud Platform on Terraform** — VPC, public/private subnets, ECR, ECS, IAM and CloudWatch baseline.
- **AWS IAM Attack & Defense Lab** — offline detection of dangerous IAM permission combinations and least-privilege regression tests.
- **AWS Multi-Account Landing Zone** — Organizations, OUs, SCPs, centralized audit logging and delegated security administration.
- **AWS Zero-Trust CI Identity** — GitHub OIDC to short-lived AWS STS sessions with branch-scoped trust and permissions boundaries.

## Reliability, observability and traffic

- **Observability & SRE Stack** — Prometheus, Grafana, Alertmanager, SLI/SLO rules and runbooks.
- **OpenTelemetry Distributed Tracing** — frontend/backend traces through OTel Collector into Jaeger.
- **Nginx & HAProxy Load Balancing** — health checks and automated backend-failure verification.
- **Chaos Engineering Reliability Lab** — Toxiproxy fault injection and recovery verification.
- **Grafana LGTM Observability Platform** — Grafana, Loki, Tempo and Mimir with end-to-end telemetry smoke tests.
- **SRE Incident Response Game Day** — controlled 5xx incident, Prometheus paging, runbook remediation and MTTA/MTTR evidence.

## Operations, data and security services

- **Ansible Linux Platform Automation** — Ubuntu baseline, Docker, Nginx, systemd, journald and firewall automation.
- **PostgreSQL Database Reliability Lab** — migrations, backup/restore verification and PostgreSQL metrics.
- **Vault Secrets Platform** — KV v2, least-privilege policies and Kubernetes auth design.
- **Messaging Reliability Lab** — RabbitMQ quorum queues, DLQ routing and failure-flow verification.
- **FinOps Governance Lab** — budget, allocation metadata and Kubernetes cost-control policy.
- **Vulnerability Management Platform** — Trivy ingestion, CVSS/EPSS prioritization, SLA routing and DefectDojo-compatible import.

## Industrial and OT security

- **Industrial Cyber Range** — local pump/PLC process simulator with Modbus/TCP, OPC UA, MQTT, SCADA, asset inventory, segmentation policy, detections, safe-state logic and incident evidence.
