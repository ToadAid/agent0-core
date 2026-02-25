# identity/

Identity verification toolkit for ToadAid ERC-8004 registry.

## Purpose

Tools for verifying and interacting with ToadAid identity infrastructure:
- Check wallet status in registry
- Verify MPASS gating requirements
- Lookup agent metadata
- Validate registration status

## Tools

- `verify_identity.py` — Check wallet registry status
- `forge_check.py` — Verify MPASS gating and router configuration

## Contracts (Base Mainnet)

- Registry Proxy: `0x8004A169F84a3325136EB29fA0ceB6D2e539a432`
- Base Implementation: `0x7274e874CA62410a93Bd8bf61c69d8045E399c02`
- MPASS Token: Check registry for current gate token

## Safety

- Read-only operations only
- No wallet connection required
- Safe defaults on all queries
