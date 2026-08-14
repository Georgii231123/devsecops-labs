# Runtime verification runbook

This drill requires a Linux host capable of running privileged kind nodes and Tetragon eBPF programs.

## 1. Create a disposable cluster

```bash
kind create cluster --name runtime-security
helm repo add cilium https://helm.cilium.io
helm repo update
helm install tetragon cilium/tetragon --namespace kube-system
kubectl -n kube-system rollout status daemonset/tetragon --timeout=180s
```

## 2. Apply the policies

```bash
kubectl apply -f policies/observe-sensitive-files.yaml
kubectl apply -f policies/enforce-shadow-access.yaml
kubectl apply -f policies/enforce-test-file.yaml
```

## 3. Create a labelled workload

Use a disposable pod with label `runtime-security=enabled`. Keep enforcement tests on `/tmp/tetragon-denied`; do not start by experimenting against arbitrary host paths.

## 4. Observe events

Forward or exec into the Tetragon agent and use `tetra getevents`. Confirm that normal file events remain observable and the test-file policy emits the expected policy name.

## 5. Enforcement drill

Create `/tmp/tetragon-denied` inside the disposable workload and attempt to open it. The process should be terminated by the policy. Remove the enforcement policy immediately after the test:

```bash
kubectl delete -f policies/enforce-test-file.yaml
```

## 6. Cleanup

```bash
kind delete cluster --name runtime-security
```

Treat tracing policies as kernel-level controls: review hook portability and rollout scope before enabling enforcement outside a disposable environment.
