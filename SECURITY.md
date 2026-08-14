# Security Policy

This repository contains hardened examples alongside intentionally vulnerable fixtures used to prove that controls and detection rules actually block unsafe configurations.

## Safety boundaries

- Never deploy content under a `vulnerable/` or explicitly marked attack/fixture directory to a real environment.
- Cloud projects do not apply infrastructure automatically from CI. Static validation and mocked/native tests are used where possible.
- Real credentials, Terraform state, private keys and production data must not be committed.
- Example IAM, networking and runtime-security policies are scoped for the lab they belong to; review them before adapting them elsewhere.

## Reporting a problem

If a hardened example can be bypassed, a workflow exposes more privilege than intended, or a policy has a meaningful security weakness, use GitHub private vulnerability reporting when it is available. Avoid publishing working exploit details in a public issue before the problem is reviewed.

Intentionally vulnerable fixtures are not security defects unless the weakness escapes their documented boundary or affects another project unintentionally.
