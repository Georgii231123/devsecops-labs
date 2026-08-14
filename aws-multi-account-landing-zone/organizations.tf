resource "aws_organizations_organization" "this" {
  feature_set = "ALL"

  aws_service_access_principals = [
    "cloudtrail.amazonaws.com",
    "config.amazonaws.com",
    "guardduty.amazonaws.com",
    "securityhub.amazonaws.com",
  ]

  enabled_policy_types = ["SERVICE_CONTROL_POLICY"]
}

resource "aws_organizations_organizational_unit" "security" {
  name      = "Security"
  parent_id = aws_organizations_organization.this.roots[0].id
}

resource "aws_organizations_organizational_unit" "infrastructure" {
  name      = "Infrastructure"
  parent_id = aws_organizations_organization.this.roots[0].id
}

resource "aws_organizations_organizational_unit" "workloads" {
  name      = "Workloads"
  parent_id = aws_organizations_organization.this.roots[0].id
}

resource "aws_organizations_organizational_unit" "prod" {
  name      = "Prod"
  parent_id = aws_organizations_organizational_unit.workloads.id
}

resource "aws_organizations_organizational_unit" "nonprod" {
  name      = "NonProd"
  parent_id = aws_organizations_organizational_unit.workloads.id
}

resource "aws_organizations_account" "managed" {
  for_each = var.create_accounts ? var.accounts : {}

  name      = each.key
  email     = each.value.email
  parent_id = local.ou_paths[each.value.ou]
  role_name = each.value.role_name

  close_on_deletion = false

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_guardduty_organization_admin_account" "security" {
  admin_account_id = var.security_account_id
}

resource "aws_securityhub_organization_admin_account" "security" {
  admin_account_id = var.security_account_id
}
