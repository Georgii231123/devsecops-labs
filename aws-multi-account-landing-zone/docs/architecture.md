# Landing-zone architecture

The management account owns AWS Organizations, SCP attachment and the organization CloudTrail. A dedicated security account is delegated for GuardDuty and Security Hub administration. The OU hierarchy separates Security, Infrastructure and Workloads, with Prod/NonProd children under Workloads.

Account vending is intentionally guarded by `create_accounts=false`. This avoids accidental account creation during review or CI. Enabling account creation is an explicit operational decision and created accounts are additionally protected with Terraform `prevent_destroy` and `close_on_deletion=false`.

The centralized audit path uses an S3 bucket with all public-access controls enabled, versioning, KMS encryption with rotation and an HTTPS-only bucket policy. CloudTrail access is constrained with `aws:SourceArn`, and the bucket policy contains both management-account and organization-ID delivery prefixes. Organization CloudTrail is multi-region and enables log-file validation. AWS Config organization aggregation is optional because its aggregation role is usually bootstrapped in a dedicated security account.
