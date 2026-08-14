#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ROOT/artifacts"

for cluster in workload-eu workload-us; do
  kind create cluster --name "$cluster" --wait 60s
  kubectl --context "kind-$cluster" create namespace payments

done

kubectl kustomize "$ROOT/apps/demo/overlays/eu" > "$ROOT/artifacts/eu.yaml"
kubectl kustomize "$ROOT/apps/demo/overlays/us" > "$ROOT/artifacts/us.yaml"

kubectl --context kind-workload-eu apply -f "$ROOT/artifacts/eu.yaml"
kubectl --context kind-workload-us apply -f "$ROOT/artifacts/us.yaml"

kubectl --context kind-workload-eu patch deployment payments-demo -n payments --type merge -p '{"spec":{"replicas":7,"template":{"spec":{"containers":[{"name":"web","image":"nginx:drifted"}]}}}}'
kubectl --context kind-workload-us patch deployment payments-demo -n payments --type merge -p '{"spec":{"replicas":9}}'

[[ "$(kubectl --context kind-workload-eu get deployment payments-demo -n payments -o jsonpath='{.spec.replicas}')" == "7" ]]
[[ "$(kubectl --context kind-workload-us get deployment payments-demo -n payments -o jsonpath='{.spec.replicas}')" == "9" ]]

kubectl --context kind-workload-eu apply -f "$ROOT/artifacts/eu.yaml"
kubectl --context kind-workload-us apply -f "$ROOT/artifacts/us.yaml"

EU_REPLICAS="$(kubectl --context kind-workload-eu get deployment payments-demo -n payments -o jsonpath='{.spec.replicas}')"
US_REPLICAS="$(kubectl --context kind-workload-us get deployment payments-demo -n payments -o jsonpath='{.spec.replicas}')"
EU_IMAGE="$(kubectl --context kind-workload-eu get deployment payments-demo -n payments -o jsonpath='{.spec.template.spec.containers[0].image}')"

[[ "$EU_REPLICAS" == "2" ]]
[[ "$US_REPLICAS" == "3" ]]
[[ "$EU_IMAGE" == "nginx:1.27.5-alpine" ]]

cat > "$ROOT/artifacts/drift-report.json" <<EOF
{
  "workload-eu": {"driftedReplicas": 7, "reconciledReplicas": $EU_REPLICAS, "reconciledImage": "$EU_IMAGE"},
  "workload-us": {"driftedReplicas": 9, "reconciledReplicas": $US_REPLICAS},
  "result": "desired-state-restored"
}
EOF
