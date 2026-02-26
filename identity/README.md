# Identity Toolkit

Tools for verifying and interacting with ToadAid ERC-8004 registry on Base.

## Tools

*   `verify_identity.py`: Check if a wallet has registered agent(s).
*   `forge_check.py`: Verify readiness to forge (MPASS balance + Router status).

## Contracts (Base Mainnet)

| Component | Address | Purpose |
| :--- | :--- | :--- |
| **Registry Proxy** | `0x8004A169F84a3325136EB29fA0ceB6D2e539a432` | Main identity registry |
| **Registry Router** | `0x17163e538029b04D4cC24f82aa6AC3B877Bd0e0` | Forging interface |
| **MPASS Token** | `0xdb9e64465d4b5fbc7ee9091c459094efc7df5cde` | Gating requirement (≥ 1.0) |
| **Reputation Router** | `0x94D7B431dD8eAFc9E1b71624DF0a90468622537a` | Attestation logic |

## Usage

**Check Readiness (Pre-Forge):**
```bash
python3 identity/forge_check.py 0xWalletAddress
```

**Check Status (Post-Forge):**
```bash
python3 identity/verify_identity.py 0xWalletAddress
```

## Safety

*   **Read-only**: No private keys required.
*   **Subprocess Isolation**: Uses `cast` for safe onchain reads.
*   **No API Keys**: Default RPC is public Base endpoint (rate limited).

## Contributing

See `docs/TOOLING_STANDARD.md` for CLI guidelines.
