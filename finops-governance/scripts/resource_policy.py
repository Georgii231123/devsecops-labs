import json
from pathlib import Path
import yaml

ROOT = Path(__file__).parents[1]
policy = json.loads((ROOT / "policy.json").read_text())
required = set(policy["required_labels"])
max_hpa = int(policy["max_hpa_replicas"])

docs = [
    doc
    for doc in yaml.safe_load_all((ROOT / "k8s" / "workloads.yaml").read_text())
    if doc
]
errors = []

for doc in docs:
    kind = doc.get("kind")
    name = doc.get("metadata", {}).get("name", "unknown")
    labels = doc.get("metadata", {}).get("labels", {})
    missing = required - labels.keys()
    if missing:
        errors.append(f"{kind}/{name}: missing metadata labels {sorted(missing)}")

    if kind == "Deployment":
        pod_labels = doc["spec"]["template"]["metadata"].get("labels", {})
        pod_missing = required - pod_labels.keys()
        if pod_missing:
            errors.append(f"Deployment/{name}: missing pod labels {sorted(pod_missing)}")
        for container in doc["spec"]["template"]["spec"]["containers"]:
            resources = container.get("resources", {})
            for field in ("requests", "limits"):
                values = resources.get(field, {})
                if not {"cpu", "memory"}.issubset(values):
                    errors.append(
                        f"Deployment/{name}:{container['name']} missing cpu/memory {field}"
                    )

    if kind == "HorizontalPodAutoscaler" and int(doc["spec"]["maxReplicas"]) > max_hpa:
        errors.append(f"HPA/{name}: maxReplicas exceeds policy ceiling {max_hpa}")

if errors:
    raise SystemExit("\n".join(errors))
print(f"FinOps resource policy passed for {len(docs)} Kubernetes objects")
