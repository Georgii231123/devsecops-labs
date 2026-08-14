#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "reusable-supply-chain-build.yml"
text = WORKFLOW.read_text()

uses = re.findall(r"uses:\s*([^\s#]+)", text)
external = [item for item in uses if not item.startswith("./")]
assert external, "expected external actions"
for item in external:
    ref = item.rsplit("@", 1)[-1]
    assert re.fullmatch(r"[0-9a-f]{40}", ref), f"action is not SHA pinned: {item}"

required_permissions = ["contents: read", "id-token: write", "attestations: write"]
for permission in required_permissions:
    assert permission in text, f"missing permission: {permission}"

for required in ["reproducible_build.sh", "syft", "cosign sign-blob", "cosign verify-blob", "actions/attest"]:
    assert required in text, f"missing supply-chain control: {required}"

print("reusable supply-chain workflow policy checks passed")
