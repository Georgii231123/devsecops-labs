variable "aws_region" {
  type        = string
  description = "AWS region for the platform."
  default     = "eu-central-1"
}

variable "cluster_name" {
  type        = string
  description = "EKS cluster name."
  default     = "production-platform"
}

variable "kubernetes_version" {
  type        = string
  description = "EKS Kubernetes version. Pin deliberately during real deployments."
  default     = "1.34"
}

variable "environment" {
  type        = string
  description = "Environment tag."
  default     = "production"
}

variable "vpc_cidr" {
  type        = string
  description = "VPC CIDR."
  default     = "10.42.0.0/16"
}

variable "admin_principal_arn" {
  type        = string
  description = "IAM role/user ARN granted EKS cluster-admin through an Access Entry."
}

variable "node_instance_types" {
  type        = list(string)
  description = "Allowed managed-node instance types."
  default     = ["m7i.large"]
}
