# DevOps & DevSecOps Engineering Labs

Hands-on portfolio covering secure delivery, Kubernetes, GitLab CI, cloud infrastructure, SRE/observability, platform engineering and Linux automation.

## Projects

| # | Project | Direction | Main stack |
|---|---|---|---|
| 1 | Kubernetes Policy-as-Code Security Lab | Kubernetes / DevSecOps | Kubernetes, OPA, Conftest, Trivy, Checkov |
| 2 | GitLab Secure Pipeline Lab | CI/CD / DevSecOps | GitLab CI, Docker, Ruff, Bandit, Gitleaks, Trivy, SBOM |
| 3 | Cloud Platform on Terraform | Cloud / IaC | Terraform, AWS VPC, ECS, ECR, IAM, CloudWatch |
| 4 | Observability & SRE Stack | SRE / Monitoring | Prometheus, Grafana, Alertmanager, SLO/SLI |
| 5 | Platform Engineering Golden Path | Platform Engineering | service scaffolding, CI templates, Docker, Kubernetes |
| 6 | Ansible Linux Platform Automation | Linux / Configuration Management | Ansible, Docker, Nginx, systemd, journald, UFW |

### Kubernetes Policy-as-Code

The repository root contains vulnerable and hardened Kubernetes workloads plus custom OPA/Conftest policy. The lab demonstrates policy gates, workload hardening, NetworkPolicy and IaC scanning.

Relevant paths: [`k8s/`](k8s/), [`policy/`](policy/), [`docs/findings.md`](docs/findings.md).

### GitLab Secure Pipeline

[`gitlab-secure-pipeline/`](gitlab-secure-pipeline/) demonstrates tests, linting, SAST, dependency auditing, secret detection, Trivy scanning, Dockerfile checks, CycloneDX SBOM generation and a deterministic safe-autofix patch flow.

### Cloud Platform on Terraform

[`cloud-platform-terraform/`](cloud-platform-terraform/) provides a reusable AWS baseline with a multi-AZ VPC, public/private subnets, optional NAT, ECR scanning, ECS Container Insights, CloudWatch logs and IAM. Cost-sensitive NAT creation is disabled by default.

### Observability & SRE

[`observability-sre/`](observability-sre/) contains an instrumented demo application, Prometheus, Grafana, Alertmanager, Node Exporter, recording rules, SLO/SLI definitions, alerts and incident runbooks.

```bash
cd observability-sre
docker compose up --build -d
```

### Platform Engineering Golden Path

[`platform-engineering/`](platform-engineering/) is an internal-developer-platform prototype. Its CLI generates a service with application code, tests, hardened Dockerfile, Kubernetes Deployment/Service/HPA, probes, ownership metadata and CI.

```bash
cd platform-engineering
python bootstrap.py payments-api --owner payments-team --output ./generated
python scripts/validate_service.py generated/payments-api
```

### Ansible Linux Platform Automation

[`ansible-linux-platform/`](ansible-linux-platform/) configures an Ubuntu application host using reusable roles for OS baseline, Docker, Nginx and application lifecycle. SSH/firewall changes are feature-gated and the documented workflow starts with check mode.

```bash
cd ansible-linux-platform
ansible-playbook -i inventories/dev/hosts.yml site.yml --check --diff
```

## Engineering themes

- infrastructure and configuration as code;
- CI/CD gates and reproducible automation;
- secure runtime defaults and least privilege;
- cloud cost-awareness and review before apply;
- SLO-driven observability and incident runbooks;
- self-service platform engineering;
- Linux host automation and repeatable operations.

Each project contains its own README and architecture/operations notes suitable for a technical interview walkthrough.
