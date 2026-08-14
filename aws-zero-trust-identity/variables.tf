variable "aws_region" {
  description = "AWS region used by the provider."
  type        = string
  default     = "eu-central-1"
}

variable "github_repository" {
  description = "GitHub repository allowed to assume the role, owner/name."
  type        = string
  default     = "Georgii231123/devsecops-labs"
}

variable "allowed_branch" {
  description = "Only this branch ref may assume the deployment role."
  type        = string
  default     = "main"
}

variable "role_name" {
  description = "Name of the short-lived GitHub Actions role."
  type        = string
  default     = "github-oidc-deploy"
}

variable "deployment_bucket_arn" {
  description = "Existing S3 bucket used by the example deployment identity."
  type        = string
  default     = "arn:aws:s3:::example-deployment-artifacts"
}
