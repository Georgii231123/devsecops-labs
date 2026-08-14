# DevOps & DevSecOps Engineering Labs

Hands-on engineering portfolio covering secure delivery, Kubernetes, cloud infrastructure, SRE, platform engineering, Linux automation, GitOps, database reliability, secrets management, messaging, distributed tracing, traffic engineering, service mesh, chaos engineering, FinOps, reusable CI platforms, multi-cluster operations, software supply-chain security, incident response, admission control, IAM security and vulnerability management.

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
| 15 | AWS EKS Production Platform | Cloud Kubernetes / Platform | Terraform, EKS, KMS, IAM, Pod Identity, multi-AZ VPC |
| 16 | Istio Service Mesh Security | Zero Trust / Service Mesh | Istio, mTLS, AuthorizationPolicy, canary, circuit breaking |
| 17 | Chaos Engineering Reliability Lab | Resilience / SRE | Toxiproxy, Docker Compose, fault injection, recovery drills |
| 18 | FinOps Governance Lab | Cost Governance / Platform | budgets, allocation policy, Kubernetes resources, CI reports |
| 19 | Grafana LGTM Observability Platform | Observability Platform | Grafana, Loki, Tempo, Mimir, telemetry smoke tests |
| 20 | Reusable GitHub Actions Secure CI | CI Platform / DevSecOps | workflow_call, Gitleaks, Bandit, Trivy, CycloneDX SBOM |
| 21 | Multi-Cluster GitOps Platform | Multi-Cluster GitOps / Platform | Argo CD, ApplicationSet, Kustomize, kind, drift reconciliation |
| 22 | Software Supply Chain Security | Supply Chain Security / DevSecOps | Cosign, Syft, GitHub attestations, reproducible builds, CycloneDX |
| 23 | SRE Incident Response Game Day | Incident Response / SRE | Prometheus, Docker Compose, paging alerts, runbooks, MTTA/MTTR |
| 24 | Kubernetes Admission Control | Admission Policy / DevSecOps | Kyverno, validation, mutation, generation, policy regression |
| 25 | AWS IAM Attack & Defense Lab | Cloud IAM / Security Engineering | IAM JSON, privilege-escalation detection, pytest, Bandit |
| 26 | Vulnerability Management Platform | Vulnerability Management / SOC to DevSecOps | Trivy, CVSS, EPSS, SLA routing, DefectDojo API |

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

**AWS EKS Production Platform.** [`aws-eks-production-platform/`](aws-eks-production-platform/) models a private multi-AZ EKS platform with KMS secret encryption, control-plane audit logs, Access Entries, private managed nodes and VPC CNI Pod Identity.

**Istio Service Mesh Security.** [`istio-service-mesh-security/`](istio-service-mesh-security/) applies strict mTLS, workload-identity authorization, bounded retries, outlier ejection and explicit canary traffic policy.

**Chaos Engineering.** [`chaos-engineering/`](chaos-engineering/) runs a real Toxiproxy latency experiment and proves both fault observability and recovery after fault removal/backend restart.

**FinOps Governance.** [`finops-governance/`](finops-governance/) turns allocation metadata, budgets, Kubernetes resource controls and forecast headroom into reviewable CI gates and a report artifact.

**Grafana LGTM Observability Platform.** [`grafana-observability-platform/`](grafana-observability-platform/) provisions Loki, Tempo and Mimir into Grafana and runs an end-to-end telemetry/readiness smoke test.

**Reusable GitHub Actions Secure CI.** [`github-actions-platform/`](github-actions-platform/) exposes a `workflow_call` contract for linting, tests, SAST, secret detection, container policy, Trivy and SBOM generation, then self-tests that contract on a sample service.

**Multi-Cluster GitOps Platform.** [`multi-cluster-gitops/`](multi-cluster-gitops/) models one management plane and two workload clusters with ApplicationSet placement, Kustomize overlays, server-side Argo API validation and real drift/reconciliation drills.

**Software Supply Chain Security.** [`supply-chain-security/`](supply-chain-security/) uses a reusable SHA-pinned builder to prove reproducible Go builds, generate CycloneDX SBOMs, sign and verify release artifacts with Cosign and emit GitHub build provenance.

**SRE Incident Response Game Day.** [`sre-incident-game-day/`](sre-incident-game-day/) injects a controlled 5xx incident, waits for a real Prometheus paging alert, executes runbook remediation and generates MTTA/MTTR timeline and postmortem evidence.

**Kubernetes Admission Control.** [`kyverno-admission-control/`](kyverno-admission-control/) turns runtime requirements into Kyverno admission controls. CI proves a hardened workload is admitted, vulnerable fixtures are rejected, seccomp mutation is applied and a default-deny NetworkPolicy can be generated.

**AWS IAM Attack & Defense.** [`aws-iam-attack-defense/`](aws-iam-attack-defense/) models IAM privilege-escalation combinations offline, produces explainable findings and risk evidence, and regression-tests a least-privilege deployer policy to prevent critical false positives.

**Vulnerability Management Platform.** [`vulnerability-management-platform/`](vulnerability-management-platform/) ingests Trivy JSON, combines CVSS and EPSS, assigns remediation SLAs and owners, proves an overdue high-risk gate can block CI, and includes a DefectDojo import client.

## Engineering themes

- infrastructure, delivery and operations as code;
- CI/CD quality and security gates;
- immutable artifacts, SBOMs, signatures, attestations and Git-based promotion;
- reproducible builds and verifiable software supply chains;
- cloud platform design with private access and least privilege;
- multi-cluster GitOps fleet placement, drift detection and convergence;
- Kubernetes admission controls for validation, mutation and generated defaults;
- IAM permission-combination analysis and least-privilege regression tests;
- risk-based vulnerability management using CVSS, EPSS, ownership and SLAs;
- zero-trust east-west traffic with workload identity;
- SLO-driven observability across metrics, logs and traces;
- executable incident-response runbooks with MTTA/MTTR evidence;
- controlled failure injection and automated recovery verification;
- FinOps allocation, budgets and capacity policy;
- self-service platform engineering and reusable CI contracts;
- Linux and Kubernetes operations with explicit runbooks;
- least-privilege secrets management instead of credentials in source;
- messaging correctness, dead-letter handling and recovery drills;
- tested database backup restoration;
- traffic health checks, retries and failover behavior;
- secure runtime defaults and reduced privilege.

Each project contains its own README and technical material suitable for a standalone interview walkthrough.
