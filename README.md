# DevSecOps Labs

A small portfolio of practical DevSecOps labs focused on automated security controls, policy enforcement and CI/CD security gates.

## Labs

### 1. Kubernetes Policy-as-Code Security Lab

The root of this repository contains a Kubernetes hardening lab with:

- vulnerable and hardened Kubernetes manifests;
- OPA / Conftest policies;
- Trivy and Checkov scanning;
- NetworkPolicy and workload hardening;
- GitHub Actions security gates.

See [`docs/findings.md`](docs/findings.md), [`policy/`](policy/) and [`k8s/`](k8s/).

### 2. GitLab Secure Pipeline Lab

[`gitlab-secure-pipeline/`](gitlab-secure-pipeline/) is a self-contained GitLab CI project that demonstrates:

- linting and unit tests;
- deterministic safe autofix with Ruff;
- SAST with Bandit;
- SCA with pip-audit;
- secret scanning with Gitleaks;
- repository and misconfiguration scanning with Trivy;
- Dockerfile linting;
- CycloneDX SBOM generation;
- security gates that stop later stages when checks fail.

A GitHub Actions smoke workflow also validates the lab while it is hosted in this GitHub portfolio.

---

## Kubernetes Policy-as-Code Lab details

The repository contains two versions of the same workload:

- `k8s/vulnerable/` — intentionally insecure configuration;
- `k8s/hardened/` — remediated configuration designed to satisfy the security policy.

The custom policy rejects workloads that run privileged, allow privilege escalation, do not enforce non-root execution, use writable root filesystems, retain Linux capabilities, omit resource limits, use `latest`, enable host namespaces, mount `hostPath`, or omit seccomp.

### Run locally

Requirements: Docker and `make`.

```bash
make policy
make trivy
make checkov
```

To prove that the gate catches the insecure example:

```bash
make vulnerable
```

That command is expected to fail with policy violations.
