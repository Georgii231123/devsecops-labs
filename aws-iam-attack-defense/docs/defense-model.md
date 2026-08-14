# Defense model

The lab analyzes permissions only; it does not call AWS APIs or attempt escalation against accounts.

Review priorities:

1. remove wildcard identity-administration permissions;
2. treat `iam:PassRole` as sensitive and pair it with `iam:PassedToService` conditions;
3. review combinations of permissions, not only individual actions;
4. scope role assumption and identity mutation to explicit ARNs;
5. use separate deployer, runtime and security-audit identities.

The detector is intentionally small and explainable. It is a portfolio example of guardrail logic, not a replacement for AWS IAM Access Analyzer or a full identity graph product.
