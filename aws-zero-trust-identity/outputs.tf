output "github_oidc_provider_arn" {
  value = aws_iam_openid_connect_provider.github.arn
}

output "github_deploy_role_arn" {
  value = aws_iam_role.github_deploy.arn
}

output "allowed_subject" {
  value = local.github_subject
}
