# Security Policy

## Scope

Agent0 Core is infrastructure-level automation software for the ToadAid ecosystem.

This repository does **not**:

- Custody private keys
- Control treasury assets
- Execute multisig transactions
- Store sensitive production secrets

All sensitive onchain operations require external governance approval via ToadAid multisig.

---

## Reporting a Vulnerability

If you discover a security vulnerability:

1. Do **not** open a public issue.
2. Contact ToadAid maintainers directly.
3. Provide detailed reproduction steps.
4. Allow reasonable time for remediation before disclosure.

Responsible disclosure is expected.

---

## Threat Model

Agent0 Core is designed under the following assumptions:

- All onchain authority remains with multisig governance.
- No autonomous irreversible actions are permitted.
- Secrets must never be committed to this repository.
- CI/CD pipelines must not expose sensitive credentials.
- All automation must remain auditable.

---

## Sensitive Areas

Particular care should be taken when reviewing:

- Scripts that prepare onchain transactions
- Registry integration logic
- Identity-layer enforcement
- Environment variable usage
- CI/CD workflow permissions

Pull requests affecting these areas require elevated review.

---

## Secret Handling

- No private keys in code.
- No plaintext secrets in commits.
- Use environment variables for credentials.
- Use scoped tokens with minimal permissions.
- Rotate credentials if exposure is suspected.

---

## Governance Alignment

Agent0 may prepare transaction payloads.  
Agent0 may not execute transactions.

All critical onchain activity must be reviewed and signed by ToadAid multisig signers.

Automation assists.  
Governance authorizes.

---

## License

Security practices align with the Apache License 2.0 and open infrastructure transparency standards.
