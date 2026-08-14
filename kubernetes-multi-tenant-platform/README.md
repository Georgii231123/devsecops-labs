# Kubernetes Multi-Tenant Platform

A namespace-based Kubernetes tenancy baseline with deterministic tenant generation and isolation regression tests.

Each tenant receives the same platform controls from one source of truth:

- namespace ownership labels;
- Pod Security `restricted` enforcement;
- ResourceQuota and LimitRange;
- namespace-scoped developer RBAC;
- workload ServiceAccount with token automount disabled;
- default-deny ingress and egress;
- DNS egress and same-tenant traffic policy.

## Tenant model

`config/tenants.yaml` is the input. `scripts/render_tenants.py` converts it into Kubernetes resources, so platform rules are not copied by hand between teams.

```bash
python -m pip install -r requirements-dev.txt
python scripts/render_tenants.py --out-dir build
pytest -q
```

## Isolation contract

The CI drill creates a disposable kind cluster and verifies:

1. generated resources are accepted by the Kubernetes API;
2. the payments developer group can create a Deployment in `payments`;
3. the same identity cannot create a Deployment in `analytics`;
4. tenant developers cannot read Secrets;
5. Pod Security rejects a privileged pod in a tenant namespace.

NetworkPolicy objects are validated as part of the platform contract. The CI does not claim packet-level NetworkPolicy enforcement because the default kind networking layer is not used here as a production CNI conformance test.
