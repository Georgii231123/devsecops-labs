from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CATALOG_FILES = [
    ROOT / "catalog/org/groups.yaml",
    ROOT / "catalog/platform/domain-system.yaml",
    ROOT / "catalog/payments/catalog.yaml",
]


def load_documents(path: Path) -> list[dict[str, Any]]:
    docs = [doc for doc in yaml.safe_load_all(path.read_text()) if doc]
    if not all(isinstance(doc, dict) for doc in docs):
        raise ValueError(f"{path}: every YAML document must be an object")
    return docs


def entity_ref(entity: dict[str, Any]) -> str:
    kind = str(entity["kind"]).lower()
    name = entity["metadata"]["name"]
    namespace = entity["metadata"].get("namespace", "default")
    return f"{kind}:{namespace}/{name}"


def normalize_ref(value: str, default_kind: str | None = None) -> str:
    if ":" not in value:
        if default_kind is None:
            return value
        value = f"{default_kind}:{value}"
    kind, remainder = value.split(":", 1)
    if "/" not in remainder:
        remainder = f"default/{remainder}"
    return f"{kind.lower()}:{remainder}"


def validate() -> list[str]:
    errors: list[str] = []
    entities: list[dict[str, Any]] = []
    for path in CATALOG_FILES:
        entities.extend(load_documents(path))

    refs = {entity_ref(entity) for entity in entities}
    for entity in entities:
        metadata = entity.get("metadata", {})
        spec = entity.get("spec", {})
        label = f"{entity.get('kind', '?')}/{metadata.get('name', '?')}"
        if entity.get("apiVersion") != "backstage.io/v1alpha1":
            errors.append(f"{label}: unexpected catalog apiVersion")
        if not metadata.get("name"):
            errors.append(f"{label}: metadata.name is required")

        kind = entity.get("kind")
        owner = spec.get("owner")
        if kind in {"Component", "API", "Resource", "System", "Domain"}:
            if not owner:
                errors.append(f"{label}: owner is required")
            elif normalize_ref(owner, "group") not in refs:
                errors.append(f"{label}: owner {owner!r} does not resolve")

        if kind in {"Component", "API", "Resource"}:
            system = spec.get("system")
            if not system:
                errors.append(f"{label}: system is required")
            elif normalize_ref(system, "system") not in refs:
                errors.append(f"{label}: system {system!r} does not resolve")

        if kind == "Component":
            annotations = metadata.get("annotations", {})
            for annotation in ("backstage.io/techdocs-ref", "github.com/project-slug"):
                if not annotations.get(annotation):
                    errors.append(f"{label}: missing annotation {annotation}")
            if spec.get("lifecycle") not in {"experimental", "production", "deprecated"}:
                errors.append(f"{label}: unsupported lifecycle")
            for api_ref in spec.get("providesApis", []):
                if normalize_ref(api_ref, "api") not in refs:
                    errors.append(f"{label}: API reference {api_ref!r} does not resolve")
            for dep_ref in spec.get("dependsOn", []):
                if normalize_ref(dep_ref) not in refs:
                    errors.append(f"{label}: dependency {dep_ref!r} does not resolve")

    template = load_documents(ROOT / "templates/python-service/template.yaml")[0]
    actions = [step.get("action") for step in template.get("spec", {}).get("steps", [])]
    required_actions = {"fetch:template", "publish:github", "catalog:register"}
    if template.get("apiVersion") != "scaffolder.backstage.io/v1beta3":
        errors.append("Template/python-service: expected scaffolder.backstage.io/v1beta3")
    missing = sorted(required_actions - set(actions))
    if missing:
        errors.append(f"Template/python-service: missing actions {missing}")

    skeleton = (ROOT / "templates/python-service/skeleton/catalog-info.yaml").read_text()
    for placeholder in ("${{ values.name }}", "${{ values.owner }}", "${{ values.system }}"):
        if placeholder not in skeleton:
            errors.append(f"skeleton catalog-info: missing placeholder {placeholder}")

    app = yaml.safe_load((ROOT / "app-config.yaml").read_text())
    for location in app.get("catalog", {}).get("locations", []):
        target = location.get("target", "")
        if location.get("type") == "file" and not (ROOT / target).resolve().exists():
            errors.append(f"app-config: catalog location does not exist: {target}")

    scorecard = yaml.safe_load((ROOT / "scorecards/service-scorecard.yaml").read_text())
    required_checks = {"owner", "system", "techdocs", "repository", "api-contract"}
    found_checks = {check["id"] for check in scorecard.get("checks", []) if check.get("required")}
    if required_checks != found_checks:
        errors.append("scorecard: required production checks changed unexpectedly")

    deployment = (ROOT / "templates/python-service/skeleton/k8s/deployment.yaml").read_text()
    for control in (
        "automountServiceAccountToken: false",
        "allowPrivilegeEscalation: false",
        "readOnlyRootFilesystem: true",
        "runAsNonRoot: true",
        "type: RuntimeDefault",
        "drop: [ALL]",
    ):
        if control not in deployment:
            errors.append(f"golden-path deployment: missing control {control}")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("portal contract failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("internal developer portal contract checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
