variable "organization_name" {
  description = "Human-readable landing-zone name used for tags and naming."
  type        = string
  default     = "engineering-platform"
}

variable "home_region" {
  description = "Primary region for centralized security services."
  type        = string
  default     = "eu-central-1"
}

variable "management_account_id" {
  description = "AWS Organizations management account ID."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.management_account_id))
    error_message = "management_account_id must be a 12-digit AWS account ID."
  }
}

variable "security_account_id" {
  description = "Delegated security tooling account ID."
  type        = string

  validation {
    condition     = can(regex("^[0-9]{12}$", var.security_account_id))
    error_message = "security_account_id must be a 12-digit AWS account ID."
  }
}

variable "log_archive_bucket_name" {
  description = "Globally unique S3 bucket used for organization audit logs."
  type        = string
}

variable "config_aggregator_role_arn" {
  description = "IAM role ARN used by AWS Config organization aggregation. Leave empty to disable the aggregator."
  type        = string
  default     = ""
}

variable "create_accounts" {
  description = "Explicit safety switch for aws_organizations_account resources."
  type        = bool
  default     = false
}

variable "accounts" {
  description = "Accounts to create when create_accounts is explicitly enabled."
  type = map(object({
    email     = string
    ou        = string
    role_name = optional(string, "OrganizationAccountAccessRole")
  }))
  default = {}
}

variable "tags" {
  description = "Additional tags applied by the AWS provider."
  type        = map(string)
  default     = {}
}
