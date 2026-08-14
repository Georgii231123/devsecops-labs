# Internal Developer Portal

A Backstage-compatible platform-engineering lab built around **Backstage 1.53.1** catalog and scaffolder contracts.

## What this demonstrates

- software catalog relationships across Group, Domain, System, Component, API and Resource entities;
- explicit ownership and production lifecycle metadata;
- TechDocs and repository annotations;
- a secure Python-service golden path using `fetch:template`, `publish:github` and `catalog:register`;
- hardened Kubernetes defaults embedded in the generated service, not left to individual developers;
- service scorecard controls for ownership, documentation, repository metadata and API registration;
- a CI-enforced portal contract that catches broken references, missing ownership and template drift.

`app-config.yaml` registers the catalog and service template. `catalog/` models organization and software topology. `templates/python-service/` is the self-service golden path. `scripts/validate_portal.py` acts as a platform governance gate and validates cross-entity references plus security defaults.
