# AWS Zero-Trust CI Identity

Terraform baseline for GitHub Actions authentication to AWS through OIDC and STS instead of long-lived access keys.

## Identity flow

```text
GitHub Actions job
      |
      | OIDC JWT
      v
AWS IAM OIDC provider
      |
      | AssumeRoleWithWebIdentity
      v
short-lived deploy role
      |
      | permissions boundary + inline policy
      v
specific deployment bucket
```

The trust policy is restricted by both token audience and subject. By default only `Georgii231123/devsecops-labs` on `refs/heads/main` can assume the role.

## Controls

- no `aws_iam_access_key` resources;
- no AWS access-key secrets in the workflow example;
- GitHub job requires `id-token: write` explicitly;
- OIDC `aud` must be `sts.amazonaws.com`;
- OIDC `sub` is pinned to repository and branch;
- STS role session is limited to 3600 seconds;
- permissions boundary limits the role to one deployment bucket;
- example action is pinned to the commit behind `configure-aws-credentials` v6.2.3;
- Terraform tests run with a mocked AWS provider and create no cloud resources.

## Validate

```bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
terraform test
python scripts/check_identity_contract.py
```

## Deploying for real

Use a dedicated AWS account/role naming convention and replace the example deployment bucket ARN. The OIDC provider is an account-level object; if an account already has the GitHub provider, import it into state or adapt the module to reference the existing provider rather than creating a duplicate.
