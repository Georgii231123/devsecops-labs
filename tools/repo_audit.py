#!/usr/bin/env python3
"""Repository-wide structural and safety checks for the engineering labs monorepo."""

from __future__ import annotations

import json
import re
import sys
import tomllib
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "docs" / "project-catalog.json"
README_PATH = ROOT / "README.md"

SKIP_PARTS = {".git", ".terraform", ".venv", "node_modules", "__pycache__"}
INTENTIONAL_RISK_PARTS = {"vulnerable", "fixtures"}
TEXT_CONFIG_SUFFIXES = {".yml", ".yaml", ".sh", ".tf", ".hcl"}
LATEST_LITERAL_ALLOWLIST = {
    Path("kyverno-admission-control/policies/disallow-latest.yaml"),
}
FORBIDDEN_NAMES = {
    ".env",
    "id_rsa",
    "id_ed25519",
    "terraform.tfstate",
    "terraform.tfstate.backup",
}

errors: list[str] = []
warnings: list[str] = []


def fail(message: str) -> None:
    errors.append(message)


def warn(message: str) -> None:
    warnings.append(message)


def should_skip(path: Path) -> bool:
    return bool(SKIP_PARTS.intersection(path.parts))


def load_catalog() -> list[dict[str, object]]:
    try:
        data = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"Cannot load project catalog: {exc}")
        return []
    if not isinstance(data, list):
        fail("Project catalog must be a JSON array")
        return []
    return data


def check_catalog(catalog: list[dict[str, object]]) -> None:
    ids = [entry.get("id") for entry in catalog]
    expected = list(range(1, len(catalog) + 1))
    if ids != expected:
        fail(f"Project IDs must be sequential: expected {expected}, got {ids}")

    seen_paths: set[str] = set()
    seen_workflows: set[str] = set()
    root_readme = README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else ""

    for entry in catalog:
        project_id = entry.get("id")
        name = entry.get("name")
        rel_path = entry.get("path")
        workflow = entry.get("workflow")

        if not isinstance(name, str) or not name.strip():
            fail(f"Project {project_id}: missing name")
            continue
        if not isinstance(rel_path, str) or not rel_path:
            fail(f"Project {project_id}: missing path")
            continue
        if not isinstance(workflow, str) or not workflow:
            fail(f"Project {project_id}: missing workflow")
            continue

        if rel_path in seen_paths and rel_path != ".":
            fail(f"Duplicate project path in catalog: {rel_path}")
        seen_paths.add(rel_path)
        if workflow in seen_workflows:
            fail(f"Duplicate primary workflow in catalog: {workflow}")
        seen_workflows.add(workflow)

        project_dir = ROOT if rel_path == "." else ROOT / rel_path
        if not project_dir.is_dir():
            fail(f"Project {project_id} path does not exist: {rel_path}")
            continue

        project_readme = README_PATH if rel_path == "." else project_dir / "README.md"
        if not project_readme.is_file():
            fail(f"Project {project_id} has no README.md: {rel_path}")
        else:
            text = project_readme.read_text(encoding="utf-8")
            if len(text.strip()) < 200:
                fail(f"Project {project_id} README is unexpectedly small: {project_readme.relative_to(ROOT)}")
            if not text.lstrip().startswith("# "):
                fail(f"Project {project_id} README must start with an H1: {project_readme.relative_to(ROOT)}")

        if not (ROOT / workflow).is_file():
            fail(f"Project {project_id} workflow does not exist: {workflow}")

        marker = f"| {project_id} |"
        if marker not in root_readme or name not in root_readme:
            fail(f"Project {project_id} is missing from the root README map: {name}")


def check_serialized_files() -> None:
    try:
        import yaml  # type: ignore[import-not-found]
    except ImportError:
        yaml = None
        warn("PyYAML is not installed; YAML syntax validation was skipped")

    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        try:
            if path.suffix == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            elif path.suffix == ".toml":
                tomllib.loads(path.read_text(encoding="utf-8"))
            elif path.suffix in {".yml", ".yaml"} and yaml is not None:
                text = path.read_text(encoding="utf-8")
                if "{{" in text or "{%" in text:
                    continue
                list(yaml.load_all(text, Loader=yaml.BaseLoader))
        except Exception as exc:  # YAML loaders use implementation-specific errors.
            fail(f"Cannot parse {path.relative_to(ROOT)}: {exc}")


def check_workflow_baseline() -> None:
    workflow_dir = ROOT / ".github" / "workflows"
    for path in sorted(workflow_dir.glob("*.yml")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        if "pull_request_target:" in text:
            fail(f"Unsafe pull_request_target trigger is not allowed: {rel}")
        if not re.search(r"(?m)^permissions:\s*$", text):
            fail(f"Workflow must declare explicit permissions: {rel}")


def check_no_floating_latest() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        rel = path.relative_to(ROOT)
        if rel in LATEST_LITERAL_ALLOWLIST:
            continue
        if INTENTIONAL_RISK_PARTS.intersection(path.parts):
            continue
        if path.name not in {"Dockerfile", "Makefile"} and path.suffix not in TEXT_CONFIG_SUFFIXES:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        if ":latest" in text:
            for number, line in enumerate(text.splitlines(), 1):
                if ":latest" in line and not line.lstrip().startswith("#"):
                    fail(f"Floating container tag ':latest' in {rel}:{number}")


def check_sensitive_files() -> None:
    for path in ROOT.rglob("*"):
        if not path.is_file() or should_skip(path):
            continue
        if path.name in FORBIDDEN_NAMES:
            fail(f"Sensitive/local file must not be tracked: {path.relative_to(ROOT)}")
        if path.suffix.lower() in {".p12", ".pfx"}:
            fail(f"Private key bundle must not be tracked: {path.relative_to(ROOT)}")


def check_links(path: Path) -> None:
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8")
    for raw_target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        target = raw_target.strip().split(" ", 1)[0].strip("<>")
        if not target or target.startswith(("#", "http://", "https://", "mailto:")):
            continue
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            fail(f"Link escapes repository in {path.relative_to(ROOT)}: {raw_target}")
            continue
        if not resolved.exists():
            fail(f"Broken local link in {path.relative_to(ROOT)}: {raw_target}")


def main() -> int:
    catalog = load_catalog()
    check_catalog(catalog)
    check_serialized_files()
    check_workflow_baseline()
    check_no_floating_latest()
    check_sensitive_files()
    check_links(README_PATH)
    check_links(ROOT / "docs" / "projects.md")

    for message in warnings:
        print(f"WARN: {message}")
    if errors:
        print(f"Repository audit failed with {len(errors)} issue(s):", file=sys.stderr)
        for message in errors:
            print(f" - {message}", file=sys.stderr)
        return 1

    print(f"Repository audit: OK ({len(catalog)} projects)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
