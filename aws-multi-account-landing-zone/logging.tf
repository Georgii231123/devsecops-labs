data "aws_iam_policy_document" "kms" {
  statement {
    sid    = "ManagementAccountAdministration"
    effect = "Allow"

    principals {
      type        = "AWS"
      identifiers = ["arn:aws:iam::${var.management_account_id}:root"]
    }

    actions   = ["kms:*"]
    resources = ["*"]
  }

  statement {
    sid    = "CloudTrailEncryption"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["kms:GenerateDataKey*"]
    resources = ["*"]

    condition {
      test     = "StringLike"
      variable = "kms:EncryptionContext:aws:cloudtrail:arn"
      values   = ["arn:aws:cloudtrail:*:${var.management_account_id}:trail/*"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:aws:cloudtrail:${var.home_region}:${var.management_account_id}:trail/${var.organization_name}-organization"]
    }
  }

  statement {
    sid    = "CloudTrailDescribeKey"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["kms:DescribeKey"]
    resources = ["*"]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:aws:cloudtrail:${var.home_region}:${var.management_account_id}:trail/${var.organization_name}-organization"]
    }
  }
}

resource "aws_kms_key" "logs" {
  description             = "Organization audit log encryption key"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.kms.json
}

resource "aws_kms_alias" "logs" {
  name          = "alias/${var.organization_name}-audit-logs"
  target_key_id = aws_kms_key.logs.key_id
}

resource "aws_s3_bucket" "logs" {
  bucket        = var.log_archive_bucket_name
  force_destroy = false
}

resource "aws_s3_bucket_ownership_controls" "logs" {
  bucket = aws_s3_bucket.logs.id

  rule {
    object_ownership = "BucketOwnerEnforced"
  }
}

resource "aws_s3_bucket_public_access_block" "logs" {
  bucket = aws_s3_bucket.logs.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_versioning" "logs" {
  bucket = aws_s3_bucket.logs.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.logs.arn
      sse_algorithm     = "aws:kms"
    }
    bucket_key_enabled = true
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "logs" {
  bucket = aws_s3_bucket.logs.id

  rule {
    id     = "archive"
    status = "Enabled"

    filter {}

    transition {
      days          = 90
      storage_class = "GLACIER_IR"
    }

    noncurrent_version_transition {
      noncurrent_days = 90
      storage_class   = "GLACIER_IR"
    }
  }
}

data "aws_iam_policy_document" "log_bucket" {
  statement {
    sid    = "CloudTrailAclCheck"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:GetBucketAcl"]
    resources = [aws_s3_bucket.logs.arn]

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:aws:cloudtrail:${var.home_region}:${var.management_account_id}:trail/${var.organization_name}-organization"]
    }
  }

  statement {
    sid    = "CloudTrailManagementAccountWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.logs.arn}/AWSLogs/${var.management_account_id}/*"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:aws:cloudtrail:${var.home_region}:${var.management_account_id}:trail/${var.organization_name}-organization"]
    }
  }

  statement {
    sid    = "CloudTrailOrganizationWrite"
    effect = "Allow"

    principals {
      type        = "Service"
      identifiers = ["cloudtrail.amazonaws.com"]
    }

    actions   = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.logs.arn}/AWSLogs/${aws_organizations_organization.this.id}/*"]

    condition {
      test     = "StringEquals"
      variable = "s3:x-amz-acl"
      values   = ["bucket-owner-full-control"]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceArn"
      values   = ["arn:aws:cloudtrail:${var.home_region}:${var.management_account_id}:trail/${var.organization_name}-organization"]
    }
  }

  statement {
    sid    = "DenyInsecureTransport"
    effect = "Deny"

    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions = ["s3:*"]
    resources = [
      aws_s3_bucket.logs.arn,
      "${aws_s3_bucket.logs.arn}/*",
    ]

    condition {
      test     = "Bool"
      variable = "aws:SecureTransport"
      values   = ["false"]
    }
  }
}

resource "aws_s3_bucket_policy" "logs" {
  bucket = aws_s3_bucket.logs.id
  policy = data.aws_iam_policy_document.log_bucket.json
}

resource "aws_cloudtrail" "organization" {
  name                          = "${var.organization_name}-organization"
  s3_bucket_name                = aws_s3_bucket.logs.id
  kms_key_id                    = aws_kms_key.logs.arn
  include_global_service_events = true
  is_multi_region_trail         = true
  is_organization_trail         = true
  enable_log_file_validation    = true
  enable_logging                = true

  depends_on = [aws_s3_bucket_policy.logs]
}

resource "aws_config_configuration_aggregator" "organization" {
  count = var.config_aggregator_role_arn == "" ? 0 : 1
  name  = "${var.organization_name}-organization"

  organization_aggregation_source {
    all_regions = true
    role_arn    = var.config_aggregator_role_arn
  }
}
