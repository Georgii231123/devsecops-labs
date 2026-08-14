from __future__ import annotations

import argparse
from pathlib import Path

import yaml

REQUIRED_FILES = [
    "Dockerfile",
    "service.yaml",
    "app/main.py",
    "tests/test_main.py",
    "k8s/deployment.yaml",
    "k8s/service.yaml",
    "k8s/hpa.yaml",
]


def validate(root: Path) -> list[str]:
    errors: list[str] = []
    for item in REQUIRED_FILES:
        if not (root / item).exists():
            errors.append(f"missing required file: {item}")

    deployment_file = root / "k8s/deployment.yaml"
    if deployment_file.exists():
        doc = yaml.safe_load(deployment_file.read_text(encoding="utf-8"))
        pod = doc["spec"]["template"]["spec"]
        container = pod["containers"][0]
        security = container.get("securityContext", {})
        pod_security = pod.get("securityContext", {})

        if not pod_security.get("runAsNonRoot"):
            errors.append("pod must enforce runAsNonRoot")
        if security.get("allowPrivilegeEscalation") is not False:
            errors.append("allowPrivilegeEscalation must be false")
        if security.get("readOnlyRootFilesystem") is not True:
            errors.append("readOnlyRootFilesystem must be true")
        if "ALL" not in security.get("capabilities", {}).get("drop", []):
            errors.append("container must drop ALL capabilities")
        if not container.get("resources", {}).get("limits"):
            errors.append("resource limits are required")
        if not container.get("readinessProbe") or not container.get("livenessProbe"):
            errors.append("liveness and readiness probes are required")

    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    errors = validate(args.path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)
    print("service satisfies platform baseline")


if __name__ == "__main__":
    main()
