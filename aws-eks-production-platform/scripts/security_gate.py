from pathlib import Path

source = (Path(__file__).parents[1] / "terraform" / "main.tf").read_text(encoding="utf-8")

checks = {
    "private EKS endpoint": "endpoint_public_access  = false",
    "private endpoint enabled": "endpoint_private_access = true",
    "KMS rotation": "enable_key_rotation     = true",
    "Kubernetes secret encryption": 'resources = ["secrets"]',
    "audit logging": '"audit"',
    "authenticator logging": '"authenticator"',
    "private node subnets": "subnet_ids      = values(aws_subnet.private)[*].id",
    "Access Entry administration": 'resource "aws_eks_access_entry" "admin"',
    "CNI Pod Identity": 'resource "aws_eks_pod_identity_association" "vpc_cni"',
    "controlled node updates": "max_unavailable = 1",
}

missing = [name for name, needle in checks.items() if needle not in source]
if missing:
    raise SystemExit("Missing required platform controls: " + ", ".join(missing))

print(f"EKS architecture gate passed: {len(checks)} controls verified")
