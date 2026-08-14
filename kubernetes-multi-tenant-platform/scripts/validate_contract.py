#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml


def validate_file(path: Path) -> list[str]:
    docs = [doc for doc in yaml.safe_load_all(path.read_text()) if doc]
    errors: list[str] = []
    by_kind: dict[str, list[dict]] = {}
    for doc in docs:
        by_kind.setdefault(doc.get("kind", ""), []).append(doc)

    required = {"Namespace", "ResourceQuota", "LimitRange", "ServiceAccount", "Role", "RoleBinding", "NetworkPolicy"}
    missing = required - set(by_kind)
    if missing:
        errors.append(f"missing kinds: {sorted(missing)}")

    for ns in by_kind.get("Namespace", []):
        labels = ns.get("metadata", {}).get("labels", {})
        if labels.get("pod-security.kubernetes.io/enforce") != "restricted":
            errors.append("namespace must enforce restricted Pod Security")

    for sa in by_kind.get("ServiceAccount", []):
        if sa.get("automountServiceAccountToken") is not False:
            errors.append("workload service account must disable token automount")

    for role in by_kind.get("Role", []):
        for rule in role.get("rules", []):
            if "*" in rule.get("verbs", []) or "*" in rule.get("resources", []):
                errors.append("tenant role must not contain wildcards")
            if "secrets" in rule.get("resources", []):
                errors.append("tenant developer role must not grant secret access")

    policies = {item["metadata"]["name"] for item in by_kind.get("NetworkPolicy", [])}
    if "default-deny" not in policies:
        errors.append("default-deny NetworkPolicy is required")
    if "allow-tenant-and-dns" not in policies:
        errors.append("tenant DNS/traffic policy is required")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    files = sorted(args.path.glob("*.yaml")) if args.path.is_dir() else [args.path]
    failed = False
    for path in files:
        errors = validate_file(path)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}")
        else:
            print(f"OK {path}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
