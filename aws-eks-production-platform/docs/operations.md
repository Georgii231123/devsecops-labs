# Operations notes

## Cluster access

The API endpoint is private. Run `kubectl`, Terraform Kubernetes providers and operational automation from a network path that can reach the VPC, such as a VPN, Direct Connect-connected network or a controlled runner inside the VPC.

## Node upgrades

1. Review EKS and add-on compatibility.
2. Update `kubernetes_version` deliberately.
3. Upgrade the control plane first.
4. Upgrade managed add-ons.
5. Roll the managed node group with PodDisruptionBudgets in place.
6. Verify workloads, DNS, CNI and observability before continuing.

## Recovery

Terraform is the source of truth for AWS infrastructure. Application state must be protected separately through workload-specific backup procedures. KMS deletion uses a 30-day window to reduce the chance of accidental destructive removal.
