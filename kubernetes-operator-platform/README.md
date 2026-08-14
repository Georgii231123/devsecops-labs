# Kubernetes Operator Platform

Production-style Go operator that turns a small `WebService` custom resource into a hardened Kubernetes runtime contract.

## What is implemented

- `WebService` CRD with OpenAPI validation and `/status` subresource;
- idempotent Deployment, Service and ConfigMap reconciliation;
- owner references plus finalizer-based cleanup;
- `Ready` condition, `readyReplicas` and `observedGeneration`;
- non-root runtime, read-only root filesystem, seccomp `RuntimeDefault`, dropped Linux capabilities and disabled service-account token automount;
- CPU/memory requests and limits plus liveness/readiness probes;
- least-privilege controller RBAC;
- fake-client unit tests and an `envtest` integration test against a real ephemeral Kubernetes API server.

## CI contract

The workflow uses Go 1.26, controller-runtime 0.24.1, `go vet`, unit tests, checksum-verified `setup-envtest`, Kubernetes 1.36 envtest assets and a final operator build.

## Interview walkthrough

Custom API design -> reconcile loop -> idempotency -> owner references/finalizers -> status conditions -> controller RBAC -> security-by-default workload generation -> fake-client testing -> API-server integration testing.
