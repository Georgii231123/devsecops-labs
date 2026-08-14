# AWS IAM Attack & Defense Lab

A defensive IAM analysis lab that models common privilege-escalation paths without requiring an AWS account or executing any attack against live infrastructure.

## Covered escalation patterns

- wildcard administrator access;
- `iam:PassRole` combined with compute creation;
- managed-policy version escalation;
- attaching powerful managed policies;
- creating access keys for other identities;
- wildcard `sts:AssumeRole`.

The analyzer converts IAM JSON into normalized allow-actions, detects dangerous combinations, assigns severity/risk points and produces JSON + Markdown evidence. Vulnerable fixtures must trigger findings; the hardened deployer policy must remain clean.

## Run

```bash
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/run_lab.py
```

## Why this matters

IAM reviews often fail when permissions are considered one statement at a time. The lab focuses on combinations: a permission that looks harmless alone can become an escalation path when another allowed action is present.
