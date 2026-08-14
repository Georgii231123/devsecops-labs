project_name       = "platform-dev"
aws_region          = "eu-central-1"
enable_nat_gateway  = false
log_retention_days  = 14

common_tags = {
  Environment = "dev"
  Owner       = "platform-team"
  CostCenter  = "portfolio"
}
