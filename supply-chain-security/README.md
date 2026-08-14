# Software Supply Chain Security

A build-security lab focused on provenance, reproducibility, SBOMs, cryptographic signatures and hardened reusable CI.

## Pipeline

```mermaid
flowchart LR
    Source[Reviewed source] --> Test[Go tests]
    Test --> Repro[Reproducible build check]
    Repro --> Hash[SHA-256]
    Hash --> SBOM[CycloneDX SBOM / Syft]
    SBOM --> Sign[Cosign blob signature]
    Sign --> Verify[Cosign verification]
    Verify --> Provenance[GitHub artifact attestation]
    Provenance --> Evidence[Immutable CI evidence]
```

## Security properties

- the build runs in a reusable workflow rather than an ad-hoc caller;
- third-party actions are pinned to full commit SHAs;
- the Go binary is built with `-trimpath` and an empty build ID;
- two independent builds must produce the same SHA-256 digest;
- Syft generates a CycloneDX SBOM;
- Cosign signs the distributable and verifies the signature before upload;
- GitHub artifact attestation establishes build provenance using OIDC;
- the private signing key is ephemeral and never uploaded as an artifact;
- only read access to repository contents is granted, plus the minimum OIDC/attestation write permissions.

GitHub documents reusable workflows plus artifact attestations as a path to SLSA v1 Build Level 3. This lab implements that architecture for a small deterministic artifact so every stage can be tested in CI.

## Repository layout

```text
supply-chain-security/
├── cmd/provenance-demo/main.go
├── scripts/
│   ├── reproducible_build.sh
│   └── verify_workflow.py
├── go.mod
└── README.md

.github/workflows/
├── reusable-supply-chain-build.yml
└── supply-chain-security.yml
```

## Local build

```bash
cd supply-chain-security
go test ./...
bash scripts/reproducible_build.sh
```

The generated `dist/` directory contains the binary archive, checksum, public signing key, Sigstore bundle and CycloneDX SBOM when run in CI.

## Interview walkthrough

The main point is not that a checksum exists. The point is that build identity, artifact contents and dependency inventory are all independently verifiable: reproducibility checks the builder output, Cosign checks artifact integrity, the SBOM describes contents, and GitHub attestation binds the artifact back to the trusted workflow execution.
