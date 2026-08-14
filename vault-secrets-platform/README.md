# Vault Secrets Platform

A secrets-management lab showing how application credentials move out of source code and into a policy-controlled secrets platform.

## Scope

- HashiCorp Vault development environment for reproducible local testing;
- production-style server configuration example with file storage and TLS expectations;
- KV v2 secret engine;
- least-privilege application policy;
- short-lived token workflow;
- Kubernetes auth role example;
- audit-device bootstrap example;
- real CI smoke test that writes and reads a secret through Vault.

## Local smoke test

```bash
cd vault-secrets-platform
docker compose up -d vault
./scripts/bootstrap-dev.sh
```

The `dev-root` token exists only for this isolated lab. It is deliberately not presented as a production pattern.

## Production design notes

For a real deployment use integrated Raft storage or a managed backend, TLS, auto-unseal/KMS, audit devices, Kubernetes or OIDC auth, short TTLs, secret rotation and no long-lived root token in automation.
