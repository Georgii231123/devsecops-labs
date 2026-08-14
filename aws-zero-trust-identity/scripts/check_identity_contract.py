#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> int:
    terraform = "\n".join(path.read_text() for path in ROOT.glob("*.tf"))
    workflow = (ROOT / "examples/github-oidc-deploy.yml").read_text()

    if 'resource "aws_iam_access_key"' in terraform:
        fail("static IAM access keys are forbidden")
    if "repo:*" in terraform or "refs/heads/*" in terraform:
        fail("wildcard GitHub subjects are forbidden")
    if "sts:AssumeRoleWithWebIdentity" not in terraform:
        fail("web-identity trust action is required")
    if "token.actions.githubusercontent.com:aud" not in terraform and "${local.oidc_host}:aud" not in terraform:
        fail("OIDC audience condition is required")
    if "${local.oidc_host}:sub" not in terraform:
        fail("OIDC subject condition is required")
    if "permissions_boundary" not in terraform:
        fail("deployment role must have a permissions boundary")

    lowered = workflow.lower()
    forbidden = ["aws-access-key-id", "aws-secret-access-key", "aws_access_key_id", "aws_secret_access_key"]
    for token in forbidden:
        if token in lowered:
            fail(f"workflow contains static credential field: {token}")
    if "id-token: write" not in workflow:
        fail("workflow must request id-token: write")
    if "role-to-assume:" not in workflow:
        fail("workflow must assume an IAM role")
    if "configure-aws-credentials@e6de054238d6b7531b4efff3b6587d9aade6a06c" not in workflow:
        fail("configure-aws-credentials must remain SHA-pinned")

    print("zero-trust identity contract: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
