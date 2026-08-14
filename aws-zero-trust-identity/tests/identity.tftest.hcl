mock_provider "aws" {}

override_data {
  target = data.aws_iam_policy_document.github_trust
  values = {
    json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}"
  }
}

override_data {
  target = data.aws_iam_policy_document.boundary
  values = {
    json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}"
  }
}

override_data {
  target = data.aws_iam_policy_document.deploy_permissions
  values = {
    json = "{\"Version\":\"2012-10-17\",\"Statement\":[]}"
  }
}

variables {
  github_repository     = "Georgii231123/devsecops-labs"
  allowed_branch        = "main"
  deployment_bucket_arn = "arn:aws:s3:::ci-artifacts-example"
}

run "zero_trust_contract" {
  command = plan

  assert {
    condition     = aws_iam_openid_connect_provider.github.url == "https://token.actions.githubusercontent.com"
    error_message = "GitHub must be the configured OIDC issuer."
  }

  assert {
    condition     = contains(aws_iam_openid_connect_provider.github.client_id_list, "sts.amazonaws.com")
    error_message = "STS audience must remain configured."
  }

  assert {
    condition     = local.github_subject == "repo:Georgii231123/devsecops-labs:ref:refs/heads/main"
    error_message = "OIDC subject must remain repository and branch scoped."
  }

  assert {
    condition     = aws_iam_role.github_deploy.max_session_duration == 3600
    error_message = "GitHub STS session must remain limited to one hour."
  }

  assert {
    condition     = aws_iam_role.github_deploy.permissions_boundary == aws_iam_policy.github_boundary.arn
    error_message = "Deployment role must retain its permissions boundary."
  }
}
