# Threat model

| Threat | Control |
|---|---|
| plaintext east-west traffic | namespace-wide STRICT mTLS |
| compromised unrelated workload calls backend | AuthorizationPolicy bound to frontend SPIFFE identity |
| unhealthy backend keeps receiving traffic | outlier detection |
| retry storm amplifies an outage | two attempts, per-try timeout and overall timeout |
| accidental uncontrolled external service discovery | Sidecar egress host scope |
| risky rollout sends all traffic to a new version | explicit 90/10 canary split |

Residual risks include compromised trusted identities, ingress-gateway compromise and application-layer authorization defects. A service mesh reduces transport and identity risk; it does not replace application authorization.
