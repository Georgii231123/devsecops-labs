# Reconciliation contract

Each `WebService` reconcile loop installs a finalizer, converges an owned Deployment/Service/ConfigMap, enforces hardened workload defaults, observes Deployment readiness and writes status. The controller uses owner references for garbage collection and an explicit finalizer for cleanup that must complete before deletion. `CreateOrUpdate` keeps reconciliation idempotent.
