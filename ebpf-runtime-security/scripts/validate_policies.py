#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

HOOK_KEYS = {"kprobes", "tracepoints", "uprobes", "lsmhooks", "fentries", "usdts"}
ALLOWED_MODES = {"monitoring", "enforcement", "monitor_only"}


def policy_mode(spec: dict) -> str | None:
    for option in spec.get("options", []):
        if option.get("name") == "policy-mode":
            return option.get("value")
    return None


def actions(spec: dict) -> list[str]:
    found: list[str] = []
    for hook_key in HOOK_KEYS:
        for hook in spec.get(hook_key, []) or []:
            for selector in hook.get("selectors", []) or []:
                for action in selector.get("matchActions", []) or []:
                    if action.get("action"):
                        found.append(str(action["action"]))
    return found


def validate(path: Path) -> list[str]:
    doc = yaml.safe_load(path.read_text())
    errors: list[str] = []
    if not isinstance(doc, dict):
        return ["document must be a mapping"]
    if doc.get("apiVersion") != "cilium.io/v1alpha1":
        errors.append("apiVersion must be cilium.io/v1alpha1")
    if doc.get("kind") not in {"TracingPolicy", "TracingPolicyNamespaced"}:
        errors.append("kind must be a Tetragon tracing policy")

    metadata = doc.get("metadata", {})
    if not metadata.get("name"):
        errors.append("metadata.name is required")

    spec = doc.get("spec", {})
    if not any(spec.get(key) for key in HOOK_KEYS):
        errors.append("at least one supported hook is required")
    selector = spec.get("podSelector", {})
    if doc.get("kind") == "TracingPolicy" and not selector:
        errors.append("cluster-scoped lab policies must use podSelector")

    mode = policy_mode(spec)
    if mode not in ALLOWED_MODES:
        errors.append(f"explicit policy-mode required; got {mode!r}")

    found_actions = actions(spec)
    if mode == "enforcement" and not found_actions:
        errors.append("enforcement policy has no matchActions")
    if mode in {"monitoring", "monitor_only"} and found_actions:
        errors.append("monitoring policy must not contain enforcement actions")

    for hook in spec.get("lsmhooks", []) or []:
        if hook.get("hook") == "file_open":
            args = hook.get("args", []) or []
            if not any(arg.get("type") == "file" for arg in args):
                errors.append("file_open LSM hook must capture a file argument")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    files = sorted(args.path.glob("*.y*ml")) if args.path.is_dir() else [args.path]
    failed = False
    for path in files:
        errors = validate(path)
        if errors:
            failed = True
            for error in errors:
                print(f"{path}: {error}")
        else:
            print(f"OK {path}")
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
