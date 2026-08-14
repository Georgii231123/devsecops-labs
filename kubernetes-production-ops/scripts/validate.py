from pathlib import Path

text = Path("/tmp/prod.yaml").read_text()
required = [
    "kind: PodDisruptionBudget",
    "kind: HorizontalPodAutoscaler",
    "kind: ResourceQuota",
    "kind: LimitRange",
    "kind: NetworkPolicy",
    "maxUnavailable: 0",
    "topologySpreadConstraints:",
    "runAsNonRoot: true",
    "readOnlyRootFilesystem: true",
    "allowPrivilegeEscalation: false",
    "automountServiceAccountToken: false",
    "startupProbe:",
    "readinessProbe:",
    "livenessProbe:",
]
missing = [item for item in required if item not in text]
if missing:
    raise SystemExit(f"missing production controls: {missing}")
if ":latest" in text:
    raise SystemExit("mutable latest tag detected")
print("Kubernetes production controls validated")
