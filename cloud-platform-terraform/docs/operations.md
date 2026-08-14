# Operations notes

## State

For a real team, move Terraform state to a remote backend with locking and encryption. Keep the backend bootstrap separate from the workload state to avoid circular dependencies.

## Cost controls

- NAT Gateway is disabled by default.
- ECR lifecycle policy limits retained images.
- CloudWatch retention is explicit rather than infinite.
- `terraform plan` is the expected default workflow; apply requires human review.

## Production extensions

A production rollout would normally add an ALB, ECS service/task definition, WAF, VPC endpoints, CloudTrail, centralized logs and remote state. Those are intentionally separated from this baseline so each control can be reviewed independently.
