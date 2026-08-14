# DevOps & DevSecOps Engineering Labs

[![Repository Quality](https://github.com/Georgii231123/devsecops-labs/actions/workflows/repository-quality.yml/badge.svg)](https://github.com/Georgii231123/devsecops-labs/actions/workflows/repository-quality.yml)

Infrastructure, delivery, reliability and security projects collected in one repository. The labs cover Kubernetes, cloud/IaC, CI/CD, platform engineering, SRE, Linux automation, identity, application security and industrial security engineering. Most projects have an executable CI check rather than only static configuration.

Cloud projects are safe by default: CI validates plans, policies and mocked contracts instead of applying paid infrastructure unless a project README explicitly says otherwise. Intentionally vulnerable examples are isolated and exist to prove that a corresponding control rejects them.

## Project map

| # | Project | Direction | Main stack |
|---|---|---|---|
| 1 | [Kubernetes Policy-as-Code Security Lab](./) | Kubernetes / DevSecOps | Kubernetes, OPA, Conftest, Trivy, Checkov |
| 2 | [GitLab Secure Pipeline Lab](gitlab-secure-pipeline/) | CI/CD / DevSecOps | GitLab CI, Docker, Ruff, Bandit, Gitleaks, Trivy, SBOM |
| 3 | [Cloud Platform on Terraform](cloud-platform-terraform/) | Cloud / IaC | Terraform, AWS VPC, ECS, ECR, IAM, CloudWatch |
| 4 | [Observability & SRE Stack](observability-sre/) | SRE / Monitoring | Prometheus, Grafana, Alertmanager, SLO/SLI |
| 5 | [Platform Engineering Golden Path](platform-engineering/) | Platform Engineering | service scaffolding, CI templates, Docker, Kubernetes |
| 6 | [Ansible Linux Platform Automation](ansible-linux-platform/) | Linux / Configuration Management | Ansible, Docker, Nginx, systemd, journald, UFW |
| 7 | [GitOps Delivery Platform](gitops-argocd-platform/) | GitOps / Kubernetes Delivery | Argo CD, ApplicationSet, Helm, HPA, NetworkPolicy |
| 8 | [PostgreSQL Database Reliability Lab](database-reliability/) | Database Operations / Reliability | PostgreSQL, migrations, pg_dump/pg_restore, Prometheus |
| 9 | [Jenkins CI/CD Platform](jenkins-cicd-platform/) | CI/CD Platform | Jenkins, JCasC, Shared Library, Trivy, Syft |
| 10 | [Vault Secrets Platform](vault-secrets-platform/) | Secrets Management | HashiCorp Vault, HCL policies, Kubernetes auth |
| 11 | [Messaging Reliability Lab](messaging-reliability/) | Messaging / Reliability | RabbitMQ, quorum queues, DLQ, Prometheus |
| 12 | [OpenTelemetry Distributed Tracing](opentelemetry-tracing/) | Observability / Tracing | OpenTelemetry, OTLP, Jaeger, Flask |
| 13 | [Kubernetes Production Operations](kubernetes-production-ops/) | Kubernetes / SRE | Kustomize, PDB, HPA, ResourceQuota, NetworkPolicy |
| 14 | [Nginx & HAProxy Load Balancing](edge-load-balancing/) | Traffic Engineering | Nginx, HAProxy, health checks, failover |
| 15 | [AWS EKS Production Platform](aws-eks-production-platform/) | Cloud Kubernetes / Platform | Terraform, EKS, KMS, IAM, Pod Identity, multi-AZ VPC |
| 16 | [Istio Service Mesh Security](istio-service-mesh-security/) | Zero Trust / Service Mesh | Istio, mTLS, AuthorizationPolicy, canary, circuit breaking |
| 17 | [Chaos Engineering Reliability Lab](chaos-engineering/) | Resilience / SRE | Toxiproxy, Docker Compose, fault injection, recovery drills |
| 18 | [FinOps Governance Lab](finops-governance/) | Cost Governance / Platform | budgets, allocation policy, Kubernetes resources, CI reports |
| 19 | [Grafana LGTM Observability Platform](grafana-observability-platform/) | Observability Platform | Grafana, Loki, Tempo, Mimir, telemetry smoke tests |
| 20 | [Reusable GitHub Actions Secure CI](github-actions-platform/) | CI Platform / DevSecOps | workflow_call, Gitleaks, Bandit, Trivy, CycloneDX SBOM |
| 21 | [Multi-Cluster GitOps Platform](multi-cluster-gitops/) | Multi-Cluster GitOps / Platform | Argo CD, ApplicationSet, Kustomize, kind, drift reconciliation |
| 22 | [Software Supply Chain Security](supply-chain-security/) | Supply Chain Security / DevSecOps | Cosign, Syft, GitHub attestations, reproducible builds, CycloneDX |
| 23 | [SRE Incident Response Game Day](sre-incident-game-day/) | Incident Response / SRE | Prometheus, Docker Compose, paging alerts, runbooks, MTTA/MTTR |
| 24 | [Kubernetes Admission Control](kyverno-admission-control/) | Admission Policy / DevSecOps | Kyverno, validation, mutation, generation, policy regression |
| 25 | [AWS IAM Attack & Defense Lab](aws-iam-attack-defense/) | Cloud IAM / Security Engineering | IAM JSON, privilege-escalation detection, pytest, Bandit |
| 26 | [Vulnerability Management Platform](vulnerability-management-platform/) | Vulnerability Management / SOC to DevSecOps | Trivy, CVSS, EPSS, SLA routing, DefectDojo API |
| 27 | [Kubernetes Operator Platform](kubernetes-operator-platform/) | Kubernetes Controllers / Platform Engineering | Go, controller-runtime, CRD, envtest, RBAC |
| 28 | [Internal Developer Portal](internal-developer-portal/) | Platform Engineering / Developer Experience | Backstage catalog, Scaffolder, TechDocs, golden path |
| 29 | [AWS Multi-Account Landing Zone](aws-multi-account-landing-zone/) | Cloud Governance / Platform Security | Terraform, AWS Organizations, SCP, CloudTrail, KMS, Config |
| 30 | [eBPF Runtime Security](ebpf-runtime-security/) | Runtime Security / eBPF | Tetragon, TracingPolicy, LSM hooks, runtime event triage |
| 31 | [Kubernetes Multi-Tenant Platform](kubernetes-multi-tenant-platform/) | Kubernetes Platform / Isolation | kind, RBAC, Pod Security, ResourceQuota, NetworkPolicy |
| 32 | [AWS Zero-Trust CI Identity](aws-zero-trust-identity/) | Cloud Identity / Zero Trust | GitHub OIDC, STS, IAM, Terraform, permissions boundaries |
| 33 | [Industrial Cyber Range](industrial-cyber-range/) | OT / ICS Security Engineering | PLC simulator, Modbus/TCP, OPC UA, MQTT, SCADA, Prometheus |

A category-oriented overview is in [`docs/projects.md`](docs/projects.md). The machine-readable project/workflow map is kept in [`docs/project-catalog.json`](docs/project-catalog.json).

## Repository quality

The repository has a top-level quality gate in addition to project-specific workflows. It checks:

- the 33-project catalog, project paths, READMEs and primary workflows;
- JSON, TOML and non-templated YAML syntax;
- local Markdown links in the root documentation;
- explicit GitHub Actions permissions and forbidden `pull_request_target` usage;
- accidental floating `:latest` container tags outside intentional vulnerable fixtures;
- sensitive local files such as `.env`, Terraform state and key bundles;
- GitHub Actions syntax with `actionlint`;
- shell scripts with ShellCheck;
- repository-wide Terraform formatting.

Run the structural check locally with:

```bash
make audit
```

The root Kubernetes security lab can still be run independently with:

```bash
make policy
make trivy
make checkov
```

## Repository conventions

- Real credentials and Terraform state are never committed.
- Vulnerable fixtures are isolated from hardened examples.
- Cloud CI validates and tests configuration without automatically creating paid infrastructure.
- Security/reliability checks are expected to fail when an intentionally unsafe regression is introduced.
- Runtime and scanner versions are pinned when deterministic behavior matters; dependency updates are handled separately.
- Each project owns its README and operational notes instead of relying on the root document for implementation details.

See [`SECURITY.md`](SECURITY.md) for repository safety boundaries and reporting guidance.
