variable "project_name" {
  type        = string
  description = "Short project identifier used in resource names."
  default     = "platform-lab"
}

variable "aws_region" {
  type    = string
  default = "eu-central-1"
}

variable "vpc_cidr" {
  type    = string
  default = "10.42.0.0/16"
}

variable "enable_nat_gateway" {
  type        = bool
  description = "Create a NAT Gateway for private subnet egress. Disabled by default to avoid unnecessary cost."
  default     = false
}

variable "log_retention_days" {
  type    = number
  default = 30
}

variable "common_tags" {
  type = map(string)
  default = {
    Environment = "lab"
    Owner       = "platform-team"
  }
}
