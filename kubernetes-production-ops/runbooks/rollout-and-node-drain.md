# Rollout and node-drain runbook

## Deployment rollout

1. Check current replica availability and recent error/latency signals.
2. Apply the reviewed desired state through GitOps.
3. Watch `kubectl rollout status deployment/resilient-web`.
4. Confirm new pods become Ready before old pods terminate.
5. Verify application SLO signals after rollout, not only Kubernetes status.
6. If the release regresses, revert the Git change or roll back to the previous immutable image.

## Node maintenance

1. Confirm PDB and replica distribution before drain.
2. Ensure at least two healthy replicas are on independent nodes/failure domains.
3. Cordon the target node.
4. Drain while respecting PDBs; do not start with `--disable-eviction`.
5. Verify replacement pods are Ready and service SLOs remain healthy.
6. Complete maintenance, uncordon, then verify topology is balanced again.
