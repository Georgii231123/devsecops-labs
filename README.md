# DevOps & DevSecOps Engineering Labs

Hands-on engineering portfolio covering secure delivery, Kubernetes, cloud infrastructure, SRE, platform engineering, Linux automation, GitOps, database reliability, secrets management, messaging, distributed tracing and traffic engineering.

## Portfolio map

| # | Project | Direction | Main stack |
|---|---|---|---|
| 1 | Kubernetes Policy-as-Code Security Lab | Kubernetes / DevSecOps | Kubernetes, OPA, Conftest, Trivy, Checkov |
| 2 | GitLab Secure Pipeline Lab | CI/CD / DevSecOps | GitLab CI, Docker, Ruff, Bandit, Gitleaks, Trivy, SBOM |
| 3 | Cloud Platform on Terraform | Cloud / IaC | Terraform, AWS VPC, ECS, ECR, IAM, CloudWatch |
| 4 | Observability & SRE Stack | SRE / Monitoring | Prometheus, Grafana, Alertmanager, SLO/SLI |
| 5 | Platform Engineering Golden Path | Platform Engineering | service scaffolding, CI templates, Docker, Kubernetes |
| 6 | Ansible Linux Platform Automation | Linux / Configuration Management | Ansible, Docker, Nginx, systemd, journald, UFW |
| 7 | GitOps Delivery Platform | GitOps / Kubernetes Delivery | Argo CD, ApplicationSet, Helm, HPA, NetworkPolicy |
| 8 | PostgreSQL Database Reliability Lab | Database Operations / Reliability | PostgreSQL, migrations, pg_dump/pg_restore, Prometheus |
| 9 | Jenkins CI/CD Platform | CI/CD Platform | Jenkins, JCasC, Shared Library, Trivy, Syft |
| 10 | Vault Secrets Platform | Secrets Management | HashiCorp Vault, HCL policies, Kubernetes auth |
| 11 | Messaging Reliability Lab | Messaging / Reliability | RabbitMQ, quorum queues, DLQ, Prometheus |
| 12 | OpenTelemetry Distributed Tracing | Observability / Tracing | OpenTelemetry, OTLP, Jaeger, Flask |
| 13 | Kubernetes Production Operations | Kubernetes / SRE | Kustomize, PDB, HPA, ResourceQuota, NetworkPolicy |
| 14 | Nginx & HAProxy Load Balancing | Traffic Engineering | Nginx, HAProxy, health checks, failover |

## Project guide

**Kubernetes Policy-as-Code.** The repository root contains vulnerable and hardened Kubernetes workloads plus custom OPA/Conftest policy, policy gates, workload hardening and IaC scanning. Relevant paths: [`k8s/`](k8s/), [`policy/`](policy/), [`docs/findings.md`](docs/findings.md).

**GitLab Secure Pipeline.** [`gitlab-secure-pipeline/`](gitlab-secure-pipeline/) demonstrates tests, linting, SAST, dependency auditing, secret detection, Trivy scanning, Dockerfile checks, CycloneDX SBOM generation and deterministic safe-autofix.

**Cloud Platform on Terraform.** [`cloud-platform-terraform/`](cloud-platform-terraform/) provides a reusable AWS baseline with a multi-AZ VPC, public/private subnets, optional NAT, ECR scanning, ECS Container Insights, CloudWatch logs and IAM.

**Observability & SRE.** [`observability-sre/`](observability-sre/) contains an instrumented service, Prometheus, Grafana, Alertmanager, Node Exporter, recording rules, SLO/SLI definitions, alerts and incident runbooks.

**Platform Engineering Golden Path.** [`platform-engineering/`](platform-engineering/) is an internal-developer-platform prototype whose CLI generates a service with tests, hardened Dockerfile, Kubernetes resources, probes, ownership metadata and CI.

**Ansible Linux Platform.** [`ansible-linux-platform/`](ansible-linux-platform/) configures Ubuntu application hosts using reusable roles for OS baseline, Docker, Nginx and application lifecycle.

**GitOps Delivery Platform.** [`gitops-argocd-platform/`](gitops-argocd-platform/) packages a service as a Helm chart and models dev/prod delivery through Argo CD ApplicationSet, immutable promotion and Git rollback.

**PostgreSQL Database Reliability.** [`database-reliability/`](database-reliability/) covers migrations, logical backups, restore verification, PostgreSQL metrics and recovery objectives. CI performs a real backup/mutate/restore drill.

**Jenkins CI/CD Platform.** [`jenkins-cicd-platform/`](jenkins-cicd-platform/) models a controller configured by JCasC with a reusable Shared Library, immutable artifact flow, SBOM/security stages and production approval.

**Vault Secrets Platform.** [`vault-secrets-platform/`](vault-secrets-platform/) demonstrates KV v2, least-privilege HCL policies, Kubernetes auth role design and a real CI secret read/write smoke test.

**Messaging Reliability.** [`messaging-reliability/`](messaging-reliability/) demonstrates RabbitMQ quorum queues, DLQ routing, a three-node cluster topology and an automated reject/dead-letter verification drill.

**OpenTelemetry Distributed Tracing.** [`opentelemetry-tracing/`](opentelemetry-tracing/) traces a frontend-to-backend request through OTel Collector into Jaeger and verifies both services through the Jaeger API.

**Kubernetes Production Operations.** [`kubernetes-production-ops/`](kubernetes-production-ops/) demonstrates PDB, HPA, topology spread, quotas, probes, hardened securityContext, NetworkPolicy and rollout/node-drain runbooks.

**Nginx & HAProxy Load Balancing.** [`edge-load-balancing/`](edge-load-balancing/) compares two proxy approaches and runs an automated backend-failure drill to verify continued traffic through the surviving node.

## Engineering themes

- infrastructure, delivery and operations as code;
- CI/CD quality and security gates;
- immutable artifacts and Git-based promotion;
- cloud cost awareness and review-before-apply;
- SLO-driven observability, metrics and distributed tracing;
- self-service platform engineering;
- Linux and Kubernetes operations with explicit runbooks;
- least-privilege secrets management instead of credentials in source;
- messaging correctness, dead-letter handling and recovery drills;
- tested database backup restoration;
- traffic health checks, retries and failover behavior;
- secure runtime defaults and reduced privilege.

Each project contains its own README and technical material suitable for a standalone interview walkthrough.
