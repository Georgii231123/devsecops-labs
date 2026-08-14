project_name       = "platform-prod"
aws_region          = "eu-central-1"
enable_nat_gateway  = true
log_retention_days  = 90

common_tags = {
  Environment = "prod"
  Owner       = "platform-team"
  CostCenter  = "example"
}
