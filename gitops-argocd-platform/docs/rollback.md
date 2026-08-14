# Rollback

Rollback is a desired-state change, not an emergency sequence of undocumented kubectl commands.

1. Identify the last known-good image tag or Git commit.
2. Revert the environment values commit (or create a reviewed PR restoring the prior tag).
3. Merge the change.
4. Confirm Argo CD reports the application Synced/Healthy.
5. Verify user-facing SLOs before closing the incident.

If GitOps reconciliation itself is unavailable, use break-glass access only under the incident procedure and reconcile Git with the cluster afterwards.
