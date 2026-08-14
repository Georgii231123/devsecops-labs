locals {
  oidc_host      = "token.actions.githubusercontent.com"
  github_subject = "repo:${var.github_repository}:ref:refs/heads/${var.allowed_branch}"

  tags = {
    ManagedBy = "terraform"
    Purpose   = "github-oidc"
  }
}

resource "aws_iam_openid_connect_provider" "github" {
  url = "https://${local.oidc_host}"

  client_id_list = [
    "sts.amazonaws.com",
  ]

  tags = local.tags
}

data "aws_iam_policy_document" "github_trust" {
  statement {
    sid     = "GitHubActionsOIDC"
    effect  = "Allow"
    actions = ["sts:AssumeRoleWithWebIdentity"]

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.github.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.oidc_host}:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringEquals"
      variable = "${local.oidc_host}:sub"
      values   = [local.github_subject]
    }
  }
}

data "aws_iam_policy_document" "boundary" {
  statement {
    sid    = "DeploymentBucketOnly"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
      "s3:DeleteObject",
    ]
    resources = ["${var.deployment_bucket_arn}/*"]
  }

  statement {
    sid       = "ListDeploymentBucket"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [var.deployment_bucket_arn]
  }
}

resource "aws_iam_policy" "github_boundary" {
  name        = "${var.role_name}-boundary"
  description = "Maximum permissions available to the GitHub OIDC deployment role."
  policy      = data.aws_iam_policy_document.boundary.json
  tags        = local.tags
}

resource "aws_iam_role" "github_deploy" {
  name                 = var.role_name
  assume_role_policy   = data.aws_iam_policy_document.github_trust.json
  permissions_boundary = aws_iam_policy.github_boundary.arn
  max_session_duration = 3600
  tags                 = local.tags
}

data "aws_iam_policy_document" "deploy_permissions" {
  statement {
    sid    = "PublishArtifacts"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = ["${var.deployment_bucket_arn}/*"]
  }

  statement {
    sid       = "ListArtifacts"
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = [var.deployment_bucket_arn]
  }
}

resource "aws_iam_role_policy" "deploy" {
  name   = "deployment-artifacts"
  role   = aws_iam_role.github_deploy.id
  policy = data.aws_iam_policy_document.deploy_permissions.json
}
