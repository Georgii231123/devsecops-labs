#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

SENSITIVE_PATHS = {"/etc/shadow", "/etc/sudoers"}


def triage(event: dict) -> dict:
    lsm = event.get("process_lsm", {})
    process = lsm.get("process", {})
    pod = process.get("pod", {})
    paths: list[str] = []
    for arg in lsm.get("args", []) or []:
        file_arg = arg.get("file_arg", {})
        if file_arg.get("path"):
            paths.append(file_arg["path"])
    sensitive = sorted(set(paths) & SENSITIVE_PATHS)
    return {
        "rule": "sensitive-file-access" if sensitive else "runtime-observation",
        "severity": "high" if sensitive else "info",
        "binary": process.get("binary", "unknown"),
        "namespace": pod.get("namespace", "host"),
        "pod": pod.get("name", "host"),
        "paths": paths,
        "policy": lsm.get("policy_name", "unknown"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("event", type=Path)
    args = parser.parse_args()
    result = triage(json.loads(args.event.read_text()))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
