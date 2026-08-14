# Platform Engineering Golden Path

A small internal-developer-platform prototype. Instead of asking every team to reinvent Dockerfiles, Kubernetes manifests and CI rules, this project generates a service from an opinionated secure template.

## Capabilities

- CLI service bootstrapper;
- standardized Python service layout;
- non-root container image;
- Kubernetes Deployment, Service and HPA;
- liveness/readiness probes and resource limits;
- default securityContext and dropped capabilities;
- generated ownership metadata;
- reusable CI template with tests, linting, container build and security scan;
- policy validation for generated manifests;
- automated tests for the scaffolder itself.

## Developer flow

```mermaid
flowchart LR
  Dev[Developer] --> CLI[bootstrap.py]
  CLI --> Template[Golden template]
  Template --> Repo[New service repository]
  Repo --> CI[CI quality + security gates]
  CI --> Image[Container image]
  Image --> K8s[Kubernetes]
```

## Generate a service

```bash
python bootstrap.py payments-api --owner payments-team --port 8080 --output ./generated
```

The command creates `generated/payments-api/` with application code, tests, Dockerfile, Kubernetes manifests, ownership metadata and a CI workflow.

Run validation:

```bash
python scripts/validate_service.py generated/payments-api
```

## Design goal

The platform should make the secure/reliable path the easiest path. Teams can extend the generated project, but they start with a known baseline instead of a blank repository.

## Interview explanation

> I implemented a small golden-path platform. A developer gives the service name and owner, and the platform scaffolds a production-oriented repository with health endpoints, tests, container hardening, Kubernetes resources and CI. A validator checks mandatory platform controls, so generated services remain consistent and reviewable.
