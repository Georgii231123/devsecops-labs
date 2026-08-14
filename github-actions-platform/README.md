# Reusable GitHub Actions Secure CI Platform

A reusable CI building block that demonstrates how a platform team can expose one maintained security/quality workflow to many application repositories instead of copying pipeline logic everywhere.

## Contract

The reusable workflow accepts:

- `working-directory` — application directory inside the repository;
- `python-version` — Python runtime used for tests;
- `run-container-scan` — whether to build and inspect a container.

It performs linting, tests, Bandit SAST, dependency auditing when runtime dependencies exist, Git history secret scanning, a container build, deterministic non-root image policy, Trivy review and CycloneDX SBOM generation.

## Call it

```yaml
jobs:
  secure-ci:
    uses: ./.github/workflows/reusable-secure-ci.yml
    with:
      working-directory: github-actions-platform/sample
      python-version: '3.13'
      run-container-scan: true
```

A real organization would host the reusable workflow in a dedicated platform repository and consume an immutable tag or commit SHA, for example `org/platform-workflows/.github/workflows/secure-ci.yml@v1`.

## Self-test

`.github/workflows/reusable-platform-selftest.yml` consumes the reusable workflow against `sample/`. That means changes to the platform contract are tested by the same consumer path that application teams would use.

## Platform-engineering point

The interesting part is ownership. Application teams provide source code and a small set of inputs; the platform team centrally evolves security gates, action versions, artifact generation and policy without asking every repository to reimplement them.
