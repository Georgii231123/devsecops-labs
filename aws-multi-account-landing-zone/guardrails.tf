locals {
  security_baseline_scp = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid      = "DenyLeavingOrganization"
        Effect   = "Deny"
        Action   = ["organizations:LeaveOrganization"]
        Resource = "*"
      },
      {
        Sid    = "ProtectCloudTrail"
        Effect = "Deny"
        Action = [
          "cloudtrail:DeleteTrail",
          "cloudtrail:StopLogging",
          "cloudtrail:UpdateTrail",
        ]
        Resource = "*"
      },
      {
        Sid    = "ProtectConfig"
        Effect = "Deny"
        Action = [
          "config:DeleteConfigurationRecorder",
          "config:DeleteDeliveryChannel",
          "config:StopConfigurationRecorder",
        ]
        Resource = "*"
      },
      {
        Sid    = "ProtectDetectionServices"
        Effect = "Deny"
        Action = [
          "guardduty:DeleteDetector",
          "guardduty:DisassociateFromAdministratorAccount",
          "securityhub:DisableSecurityHub",
          "securityhub:DisassociateFromAdministratorAccount",
        ]
        Resource = "*"
      },
    ]
  }
}

resource "aws_organizations_policy" "security_baseline" {
  name        = "SecurityBaseline"
  description = "Protect organization membership and centralized detection/audit controls."
  type        = "SERVICE_CONTROL_POLICY"
  content     = jsonencode(local.security_baseline_scp)
}

resource "aws_organizations_policy_attachment" "security" {
  policy_id = aws_organizations_policy.security_baseline.id
  target_id = aws_organizations_organizational_unit.security.id
}

resource "aws_organizations_policy_attachment" "infrastructure" {
  policy_id = aws_organizations_policy.security_baseline.id
  target_id = aws_organizations_organizational_unit.infrastructure.id
}

resource "aws_organizations_policy_attachment" "workloads" {
  policy_id = aws_organizations_policy.security_baseline.id
  target_id = aws_organizations_organizational_unit.workloads.id
}
