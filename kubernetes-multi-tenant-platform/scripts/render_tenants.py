#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def render_tenant(tenant: dict) -> list[dict]:
    name = tenant["name"]
    group = tenant["developer_group"]
    quota = tenant["quota"]
    labels = {
        "tenant.platform/name": name,
        "pod-security.kubernetes.io/enforce": "restricted",
        "pod-security.kubernetes.io/audit": "restricted",
        "pod-security.kubernetes.io/warn": "restricted",
    }
    namespace = {
        "apiVersion": "v1",
        "kind": "Namespace",
        "metadata": {"name": name, "labels": labels},
    }
    resource_quota = {
        "apiVersion": "v1",
        "kind": "ResourceQuota",
        "metadata": {"name": "tenant-budget", "namespace": name},
        "spec": {
            "hard": {
                "requests.cpu": quota["cpu"],
                "limits.cpu": quota["cpu"],
                "requests.memory": quota["memory"],
                "limits.memory": quota["memory"],
                "pods": quota["pods"],
                "persistentvolumeclaims": quota["persistentvolumeclaims"],
            }
        },
    }
    limit_range = {
        "apiVersion": "v1",
        "kind": "LimitRange",
        "metadata": {"name": "container-defaults", "namespace": name},
        "spec": {
            "limits": [
                {
                    "type": "Container",
                    "defaultRequest": {"cpu": "100m", "memory": "128Mi"},
                    "default": {"cpu": "500m", "memory": "512Mi"},
                }
            ]
        },
    }
    service_account = {
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {"name": "workload", "namespace": name},
        "automountServiceAccountToken": False,
    }
    role = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "Role",
        "metadata": {"name": "tenant-developer", "namespace": name},
        "rules": [
            {
                "apiGroups": ["", "apps", "batch"],
                "resources": [
                    "pods",
                    "pods/log",
                    "services",
                    "configmaps",
                    "deployments",
                    "replicasets",
                    "statefulsets",
                    "jobs",
                    "cronjobs",
                ],
                "verbs": ["get", "list", "watch", "create", "update", "patch", "delete"],
            }
        ],
    }
    role_binding = {
        "apiVersion": "rbac.authorization.k8s.io/v1",
        "kind": "RoleBinding",
        "metadata": {"name": "tenant-developers", "namespace": name},
        "subjects": [{"kind": "Group", "name": group, "apiGroup": "rbac.authorization.k8s.io"}],
        "roleRef": {
            "apiGroup": "rbac.authorization.k8s.io",
            "kind": "Role",
            "name": "tenant-developer",
        },
    }
    default_deny = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {"name": "default-deny", "namespace": name},
        "spec": {"podSelector": {}, "policyTypes": ["Ingress", "Egress"]},
    }
    tenant_traffic = {
        "apiVersion": "networking.k8s.io/v1",
        "kind": "NetworkPolicy",
        "metadata": {"name": "allow-tenant-and-dns", "namespace": name},
        "spec": {
            "podSelector": {},
            "policyTypes": ["Ingress", "Egress"],
            "ingress": [{"from": [{"podSelector": {}}]}],
            "egress": [
                {"to": [{"podSelector": {}}]},
                {
                    "to": [{"namespaceSelector": {"matchLabels": {"kubernetes.io/metadata.name": "kube-system"}}}],
                    "ports": [
                        {"protocol": "UDP", "port": 53},
                        {"protocol": "TCP", "port": 53},
                    ],
                },
            ],
        },
    }
    return [namespace, resource_quota, limit_range, service_account, role, role_binding, default_deny, tenant_traffic]


def load_tenants(path: Path) -> list[dict]:
    data = yaml.safe_load(path.read_text())
    return data["tenants"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config/tenants.yaml"))
    parser.add_argument("--out-dir", type=Path, default=Path("build"))
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    for tenant in load_tenants(args.config):
        output = args.out_dir / f"{tenant['name']}.yaml"
        output.write_text(yaml.safe_dump_all(render_tenant(tenant), sort_keys=False))
        print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
