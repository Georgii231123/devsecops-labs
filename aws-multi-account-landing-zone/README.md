# AWS Multi-Account Landing Zone

Terraform reference implementation for a secure AWS Organizations baseline using **Terraform 1.15.x** and **AWS provider 6.60.x**.

## Included controls

- AWS Organizations with all features and SCP support;
- Security, Infrastructure, Workloads, Prod and NonProd OUs;
- guarded account vending (`create_accounts=false` by default);
- account deletion protection in Terraform;
- delegated GuardDuty and Security Hub security account;
- SCP protection for organization membership, CloudTrail, AWS Config, GuardDuty and Security Hub;
- central S3 audit bucket with public-access blocking, versioning, KMS encryption and HTTPS-only access;
- CloudTrail S3/KMS permissions bound to the expected trail ARN and organization log prefix;
- KMS rotation and CloudTrail service permissions;
- organization-wide, multi-region CloudTrail with log-file validation;
- optional AWS Config organization aggregator;
- native `terraform test` regression suite with a mock AWS provider, so CI creates no cloud resources.

## Validation

```bash
terraform fmt -check -recursive
terraform init -backend=false
terraform validate
terraform test
python scripts/validate_contract.py
```

The design is intentionally safe for a public portfolio: running validation and tests does not need AWS credentials, and account creation stays disabled until explicitly enabled.
