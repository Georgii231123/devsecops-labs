#!/usr/bin/env python3
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load(path: str):
    return yaml.safe_load((ROOT / path).read_text())


def main() -> None:
    project = load("argocd/appproject.yaml")
    appset = load("argocd/applicationset.yaml")

    assert project["kind"] == "AppProject"
    assert project["spec"]["sourceRepos"] == [
        "https://github.com/Georgii231123/devsecops-labs.git"
    ]
    destinations = {
        (item["name"], item["namespace"])
        for item in project["spec"]["destinations"]
    }
    assert destinations == {
        ("workload-eu", "payments"),
        ("workload-us", "payments"),
    }
    assert project["spec"]["clusterResourceWhitelist"] == []

    elements = appset["spec"]["generators"][0]["list"]["elements"]
    clusters = {item["cluster"] for item in elements}
    overlays = {item["overlay"] for item in elements}
    assert clusters == {"workload-eu", "workload-us"}
    assert overlays == {"eu", "us"}

    template = appset["spec"]["template"]["spec"]
    assert template["project"] == "platform-workloads"
    assert template["source"]["targetRevision"] == "main"
    assert template["syncPolicy"]["automated"] == {
        "prune": True,
        "selfHeal": True,
    }
    sync_options = set(template["syncPolicy"]["syncOptions"])
    assert {"CreateNamespace=true", "ServerSideApply=true"} <= sync_options

    for overlay in overlays:
        path = ROOT / "apps" / "demo" / "overlays" / overlay / "kustomization.yaml"
        assert path.exists(), f"missing overlay: {overlay}"

    print("multi-cluster GitOps policy checks passed")


if __name__ == "__main__":
    main()
