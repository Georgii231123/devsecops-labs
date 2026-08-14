# Jenkins CI/CD Platform

A portfolio-grade Jenkins platform lab focused on repeatable controller configuration, reusable pipelines and delivery guardrails.

## What this demonstrates

- Jenkins Configuration as Code (JCasC);
- plugin installation from a pinned manifest;
- reusable Shared Library pipeline primitives;
- CI stages for test, lint, image build, SBOM and security scanning;
- explicit production approval instead of unattended deployment;
- immutable image tags based on Git commit SHA;
- controller hardening defaults and disabled anonymous access;
- automated validation of the platform configuration in GitHub Actions.

## Layout

- `Dockerfile` - reproducible Jenkins controller image;
- `plugins.txt` - controller plugins;
- `casc/jenkins.yaml` - JCasC configuration;
- `Jenkinsfile` - example consumer pipeline;
- `vars/securePipeline.groovy` - reusable Shared Library entrypoint;
- `scripts/validate.py` - policy checks for the lab.

## Local controller

```bash
cd jenkins-cicd-platform
docker compose build
docker compose up -d
```

The lab intentionally keeps credentials out of Git. Production credentials should be injected from an external secret manager such as Vault.

## Interview walkthrough

A useful walkthrough is: controller bootstrapping -> JCasC -> shared library -> immutable artifact -> security gates -> manual production approval -> rollback to the previous immutable image.
