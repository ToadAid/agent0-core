# Identity Quickstart

Quick guide for verifying ToadAid identity status and registry participation.

## Overview

ToadAid uses ERC-8004 for agent identity registration on Base Mainnet.
This guide shows how to verify identity status without needing private keys.

## Prerequisites

- Python 3.8+
- Internet connection
- Wallet address (to check)

## Quick Check

```bash
# Check if a wallet has a registered agent
python identity/verify_identity.py 0xYourWalletAddress

# Verify MPASS gating status
python identity/forge_check.py 0xYourWalletAddress
```

## Registry Contracts

| Component | Address | Purpose |
|-----------|---------|---------|
| Registry Proxy | `0x8004A169F84a3325136EB29fA0ceB6D2e539a432` | Main entry point |
| Base Implementation | `0x7274e874CA62410a93Bd8bf61c69d8045e399c02` | Reference implementation |
| Registry Router | `0x17163e538029b04D4cC24f82aa6AC3B877Bd0e0` | Forge operations |

## What Each Tool Does

### verify_identity.py
- Checks if wallet has registered agent(s)
- Shows agentId(s) if registered
- Links to registry explorer
- Safe defaults: read-only, no wallet required

### forge_check.py
- Verifies MPASS token balance (gating requirement)
- Shows minimum required balance
- Displays router contract status
- Helps determine eligibility to forge

## Output Format

```
Wallet: 0x...
Status: [Registered | Not Registered]
Agent ID: #12345 (if registered)
Registry URL: https://...
```

## Troubleshooting

**"No agent found for wallet"**
- Wallet has not registered through the forge
- Check /forge portal to create identity

**"MPASS balance below threshold"**
- Need ≥ 1.0 MPASS to forge new agent
- Acquire MPASS before registration

**"Registry unreachable"**
- Check internet connection
- Verify Base Mainnet RPC endpoints

## Next Steps

- Visit https://toadaid.github.io/forge to register
- Check https://toadaid.github.io/agent to browse directory
- Read AGENT_POLICY.md for operational guidelines

## Safety Reminders

- Never share private keys
- These tools are read-only
- Verify contract addresses independently
- Report suspicious activity
