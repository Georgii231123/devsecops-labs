output "organization_id" {
  description = "AWS Organizations ID."
  value       = aws_organizations_organization.this.id
}

output "organizational_unit_ids" {
  description = "Landing-zone OU IDs by logical name."
  value       = local.ou_paths
}

output "security_baseline_policy_id" {
  description = "SCP protecting centralized security controls."
  value       = aws_organizations_policy.security_baseline.id
}

output "log_archive_bucket" {
  description = "Central audit log bucket name."
  value       = aws_s3_bucket.logs.id
}
