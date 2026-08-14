# Kubernetes Admission Control with Kyverno

Production-style admission-control lab built around Kyverno policies instead of relying on developer discipline alone.

## What is enforced

- containers cannot run privileged;
- pod workloads must run as non-root;
- mutable `:latest` image tags are rejected;
- CPU/memory requests and limits plus readiness/liveness probes are required;
- `hostPath` volumes are rejected;
- missing pod-level seccomp is mutated to `RuntimeDefault`;
- namespaces labeled `network-policy=default-deny` receive a default-deny NetworkPolicy.

The repository contains hardened and intentionally vulnerable fixtures. CI installs the real Kyverno CLI, validates policy syntax, proves allowed workloads pass, proves unsafe workloads fail, and checks mutation/generation contracts.

## Structure

```text
kyverno-admission-control/
├── policies/
├── fixtures/
│   ├── good.yaml
│   ├── bad-privileged.yaml
│   ├── bad-root.yaml
│   ├── bad-latest.yaml
│   ├── bad-resources.yaml
│   └── bad-hostpath.yaml
└── scripts/validate_contract.py
```

## Interview story

The useful point is not that Kyverno exists. The platform changes the default from "please remember security settings" to "unsafe workload cannot enter the cluster". Validation, mutation and generation are treated as platform controls and regression-tested in CI.
