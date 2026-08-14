# Pipeline design

The pipeline is ordered to fail fast and keep expensive or reporting-oriented work later.

1. **Validate** — Ruff linting and formatting.
2. **Test** — unit tests and JUnit report.
3. **Autofix** — safe deterministic fixes are exported as a patch artifact.
4. **Security** — Bandit, pip-audit, Gitleaks, Trivy and Hadolint run as gates.
5. **Supply chain** — Syft creates a CycloneDX SBOM after the security stage succeeds.

The autofix stage intentionally does not push code. Automation is allowed to make deterministic safe changes, but protected branches remain controlled by the normal review process.
