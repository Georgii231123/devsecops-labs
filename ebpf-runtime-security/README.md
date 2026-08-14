# eBPF Runtime Security

Runtime-security lab built around Cilium Tetragon tracing policies. The project separates **observation**, **enforcement** and **event triage** so a policy can be reviewed before it is allowed to kill or block a workload.

## What is implemented

- Tetragon `TracingPolicy` for sensitive file access using an LSM hook;
- enforcement policy using an in-kernel action;
- workload scoping through Kubernetes labels;
- policy-mode separation between monitoring and enforcement;
- deterministic policy contract checks;
- Tetragon-style event triage with severity/rule mapping;
- pinned `tetra` CLI artifact verification in CI;
- a real-cluster runbook for kind/Tetragon verification.

## Layout

```text
policies/               Tetragon policies
fixtures/events/        deterministic runtime-event samples
scripts/                policy validator and event triage
runbooks/                local kernel/runtime verification
 tests/                  regression tests
```

## Security model

Sensitive file controls use the `file_open` LSM hook instead of hooking a userspace-facing syscall. This keeps the decision closer to the kernel security hook and avoids building the control around a userspace pointer that may change between check and use.

The monitoring policy has no enforcement action. The enforcement policy is explicitly marked with `policy-mode: enforcement` and contains a `Sigkill` action. Both are scoped to pods carrying `runtime-security: enabled`.

## Local checks

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_policies.py policies
python scripts/event_triage.py fixtures/events/sensitive-file.json
pytest -q
```

## Runtime test

CI can validate the policy contract and event processing on a normal runner, but actual eBPF enforcement depends on the host kernel and Tetragon agent privileges. `runbooks/kind-tetragon.md` contains the real runtime procedure rather than pretending a hosted runner is equivalent to a production node.
