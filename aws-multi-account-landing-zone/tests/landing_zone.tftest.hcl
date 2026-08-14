mock_provider "aws" {
  mock_data "aws_iam_policy_document" {
    defaults = {
      json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}"
    }
  }
}

variables {
  management_account_id      = "111111111111"
  security_account_id        = "222222222222"
  log_archive_bucket_name    = "example-org-audit-logs-111111111111"
  create_accounts            = false
  config_aggregator_role_arn = ""
}

run "secure_defaults" {
  command = plan

  assert {
    condition     = aws_organizations_organization.this.feature_set == "ALL"
    error_message = "Organizations must use ALL features."
  }

  assert {
    condition     = contains(aws_organizations_organization.this.enabled_policy_types, "SERVICE_CONTROL_POLICY")
    error_message = "SCP support must remain enabled."
  }

  assert {
    condition     = length(aws_organizations_account.managed) == 0
    error_message = "Account creation must be disabled by default."
  }

  assert {
    condition = (
      aws_s3_bucket_public_access_block.logs.block_public_acls &&
      aws_s3_bucket_public_access_block.logs.block_public_policy &&
      aws_s3_bucket_public_access_block.logs.ignore_public_acls &&
      aws_s3_bucket_public_access_block.logs.restrict_public_buckets
    )
    error_message = "The audit bucket must block every public access path."
  }

  assert {
    condition     = aws_kms_key.logs.enable_key_rotation
    error_message = "The audit KMS key must keep rotation enabled."
  }

  assert {
    condition = (
      aws_cloudtrail.organization.is_multi_region_trail &&
      aws_cloudtrail.organization.is_organization_trail &&
      aws_cloudtrail.organization.enable_log_file_validation
    )
    error_message = "CloudTrail must remain organization-wide, multi-region and validation-enabled."
  }
}
