# Security gates

| Gate | Purpose | Pipeline behavior |
|---|---|---|
| Ruff | Code quality and deterministic safe fixes | Fails validation |
| Bandit | Python SAST | Fails on medium/high confidence issues selected by CLI policy |
| pip-audit | Known vulnerable Python dependencies | Fails when known vulnerabilities are detected |
| Gitleaks | Secrets in repository history/content | Fails on detected secrets |
| Trivy | Vulnerabilities, secrets and misconfiguration | Fails on HIGH/CRITICAL findings |
| Hadolint | Dockerfile best practices | Fails on lint violations |
| Syft | CycloneDX SBOM | Produces an artifact after gates pass |

The goal is not to maximize scanner count. Each gate covers a different failure class, and the pipeline keeps the remediation signal close to the merge request.
