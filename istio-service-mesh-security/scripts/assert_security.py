from pathlib import Path
import yaml

manifests = []
for path in sorted((Path(__file__).parents[1] / "manifests").glob("*.yaml")):
    manifests.extend(doc for doc in yaml.safe_load_all(path.read_text()) if doc)

by_kind = {}
for doc in manifests:
    by_kind.setdefault(doc.get("kind"), []).append(doc)

peer = by_kind["PeerAuthentication"][0]
assert peer["spec"]["mtls"]["mode"] == "STRICT"

authz = by_kind["AuthorizationPolicy"][0]
principals = authz["spec"]["rules"][0]["from"][0]["source"]["principals"]
assert principals == ["cluster.local/ns/mesh-lab/sa/frontend"]

destination = by_kind["DestinationRule"][0]["spec"]["trafficPolicy"]
assert destination["connectionPool"]["tcp"]["maxConnections"] <= 100
assert destination["outlierDetection"]["maxEjectionPercent"] == 50

backend_vs = next(v for v in by_kind["VirtualService"] if v["metadata"]["name"] == "backend")
http = backend_vs["spec"]["http"][0]
assert http["timeout"] == "2s"
assert http["retries"]["attempts"] == 2
assert sum(route["weight"] for route in http["route"]) == 100

assert by_kind.get("Sidecar"), "egress scope is missing"
print("Istio security assertions passed")
