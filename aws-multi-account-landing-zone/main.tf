locals {
  common_tags = merge(
    {
      ManagedBy   = "Terraform"
      Platform    = "LandingZone"
      Environment = "organization"
      Repository  = "Georgii231123/devsecops-labs"
    },
    var.tags,
  )

  ou_paths = {
    security       = aws_organizations_organizational_unit.security.id
    infrastructure = aws_organizations_organizational_unit.infrastructure.id
    workloads      = aws_organizations_organizational_unit.workloads.id
    prod           = aws_organizations_organizational_unit.prod.id
    nonprod        = aws_organizations_organizational_unit.nonprod.id
  }
}
