from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def require(path: str, snippets: list[str]) -> list[str]:
    text = (ROOT / path).read_text()
    return [f"{path}: missing {snippet}" for snippet in snippets if snippet not in text]


def main() -> int:
    errors: list[str] = []
    errors += require(
        "organizations.tf",
        [
            'feature_set = "ALL"',
            'enabled_policy_types = ["SERVICE_CONTROL_POLICY"]',
            "for_each = var.create_accounts ? var.accounts : {}",
            "prevent_destroy = true",
            "aws_guardduty_organization_admin_account",
            "aws_securityhub_organization_admin_account",
        ],
    )
    errors += require(
        "guardrails.tf",
        [
            "organizations:LeaveOrganization",
            "cloudtrail:StopLogging",
            "config:StopConfigurationRecorder",
            "guardduty:DeleteDetector",
            "securityhub:DisableSecurityHub",
        ],
    )
    errors += require(
        "logging.tf",
        [
            "enable_key_rotation     = true",
            "block_public_acls       = true",
            "restrict_public_buckets = true",
            'sse_algorithm     = "aws:kms"',
            "is_multi_region_trail         = true",
            "is_organization_trail         = true",
            "enable_log_file_validation    = true",
            "organization_aggregation_source",
            "CloudTrailOrganizationWrite",
            "AWSLogs/${aws_organizations_organization.this.id}/*",
            'variable = "aws:SourceArn"',
        ],
    )
    if errors:
        print("landing-zone contract failed")
        for error in errors:
            print(f"- {error}")
        return 1
    print("landing-zone security contract checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
