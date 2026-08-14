from __future__ import annotations

from dataclasses import asdict, dataclass
from fnmatch import fnmatchcase
from typing import Any


@dataclass(frozen=True)
class Finding:
    id: str
    severity: str
    score: int
    title: str
    evidence: tuple[str, ...]
    remediation: str


def _items(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    return list(value or [])


def _allowed(policy: dict[str, Any]) -> tuple[set[str], set[str]]:
    actions: set[str] = set()
    resources: set[str] = set()
    for statement in policy.get("Statement", []):
        if statement.get("Effect") != "Allow":
            continue
        actions.update(action.lower() for action in _items(statement.get("Action")))
        resources.update(_items(statement.get("Resource")))
    return actions, resources


def _has(actions: set[str], wanted: str) -> bool:
    wanted = wanted.lower()
    return any(fnmatchcase(wanted, granted) for granted in actions)


def analyze(policy: dict[str, Any]) -> list[Finding]:
    actions, resources = _allowed(policy)
    findings: list[Finding] = []

    if _has(actions, "*") or _has(actions, "iam:*"):
        findings.append(
            Finding(
                "IAM001",
                "critical",
                100,
                "Wildcard administrative permissions",
                tuple(sorted(actions)),
                "Replace wildcards with task-scoped actions and resources.",
            )
        )

    compute = any(
        _has(actions, action)
        for action in (
            "lambda:CreateFunction",
            "lambda:UpdateFunctionCode",
            "ec2:RunInstances",
            "ecs:RunTask",
        )
    )
    if _has(actions, "iam:PassRole") and compute:
        findings.append(
            Finding(
                "IAM002",
                "critical",
                90,
                "PassRole plus compute execution",
                ("iam:PassRole", "compute-create/run"),
                "Scope PassRole to approved role ARNs and restrict compute execution paths.",
            )
        )

    if _has(actions, "iam:CreatePolicyVersion") and _has(
        actions, "iam:SetDefaultPolicyVersion"
    ):
        findings.append(
            Finding(
                "IAM003",
                "critical",
                90,
                "Managed-policy version escalation",
                ("iam:CreatePolicyVersion", "iam:SetDefaultPolicyVersion"),
                "Do not grant both policy-version mutation permissions to workload identities.",
            )
        )

    attach = any(
        _has(actions, action)
        for action in (
            "iam:AttachUserPolicy",
            "iam:AttachRolePolicy",
            "iam:PutUserPolicy",
            "iam:PutRolePolicy",
        )
    )
    if attach and "*" in resources:
        findings.append(
            Finding(
                "IAM004",
                "high",
                75,
                "Unscoped policy attachment or inline-policy mutation",
                tuple(sorted(a for a in actions if a.startswith("iam:"))),
                (
                    "Scope identity mutation to named roles/users and control which "
                    "policies can be attached."
                ),
            )
        )

    if _has(actions, "iam:CreateAccessKey") and "*" in resources:
        findings.append(
            Finding(
                "IAM005",
                "high",
                70,
                "Access-key creation is not identity-scoped",
                ("iam:CreateAccessKey", "Resource=*"),
                (
                    "Allow access-key lifecycle only for an explicitly approved "
                    "identity when unavoidable."
                ),
            )
        )

    if _has(actions, "sts:AssumeRole") and "*" in resources:
        findings.append(
            Finding(
                "IAM006",
                "high",
                70,
                "Wildcard role assumption",
                ("sts:AssumeRole", "Resource=*"),
                "Restrict AssumeRole to explicit role ARNs and trust conditions.",
            )
        )

    return findings


def report(policy_name: str, policy: dict[str, Any]) -> dict[str, Any]:
    findings = analyze(policy)
    return {
        "policy": policy_name,
        "finding_count": len(findings),
        "risk_score": min(100, sum(item.score for item in findings)),
        "findings": [asdict(item) for item in findings],
    }
