# Findings and remediation

The vulnerable deployment is intentionally unsafe. It exists to demonstrate that the CI policy gate can detect configuration that should never reach a production cluster.

| Finding | Risk | Remediation in hardened manifest |
|---|---|---|
| Privileged container | Container can gain broad host-level privileges | `privileged: false` |
| Privilege escalation enabled | Process may gain more privileges than its parent | `allowPrivilegeEscalation: false` |
| Root execution | Increases impact of container escape or application compromise | `runAsNonRoot: true` with explicit UID/GID |
| Writable root filesystem | Compromised process can modify container filesystem | `readOnlyRootFilesystem: true` |
| Linux capabilities retained | Unnecessary kernel privileges increase attack surface | `capabilities.drop: [ALL]` |
| No CPU/memory limits | Resource exhaustion can affect other workloads | Requests and limits are configured |
| `latest` image tag | Deployment is not deterministic | Explicit image version is used |
| Host networking / PID | Breaks workload isolation | Host namespaces are not enabled |
| `hostPath` mount | Exposes host filesystem to the container | Only an `emptyDir` temporary volume is used |
| Missing seccomp profile | More syscalls remain available to the process | `RuntimeDefault` seccomp is required |
| Unrestricted traffic | Compromised pod can communicate broadly | NetworkPolicy restricts ingress and DNS egress |
| Service account token | Token can be exposed unnecessarily | Automount is disabled |

## Security model

The custom OPA policy is the blocking organizational control. Trivy and Checkov are included as additional scanner visibility. This mirrors a practical DevSecOps model: deterministic internal requirements are enforced as a gate while general-purpose scanners provide broader findings for review.
