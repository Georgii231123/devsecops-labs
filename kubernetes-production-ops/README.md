# Kubernetes Production Operations Lab

A production-minded Kubernetes workload baseline. The focus is not merely getting a Deployment to run, but making rollouts, disruption, scaling and multi-node placement predictable.

## Demonstrated controls

- rolling update with zero planned unavailable replicas;
- PodDisruptionBudget;
- HPA with CPU and memory targets;
- topology spread across zones and hosts;
- readiness, liveness and startup probes;
- requests/limits and namespace quotas;
- default-deny NetworkPolicy;
- non-root execution, dropped Linux capabilities and read-only root filesystem;
- disabled service-account token automount;
- LimitRange and ResourceQuota;
- operations runbook for rollout, rollback and node maintenance.

## Render production desired state

```bash
cd kubernetes-production-ops
kubectl kustomize overlays/prod
```

CI renders the overlay, checks required operational controls and scans the manifests with Trivy.

## Interview discussion

The important distinction is that `replicas: 3` alone is not high availability. Availability depends on scheduling across failure domains, disruption budgets, readiness behavior, resource headroom, rollout strategy, autoscaling and tested operational procedures.
