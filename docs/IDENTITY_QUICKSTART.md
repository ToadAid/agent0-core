# Identity Quickstart Guide (5-min)

Get your identity forged and verify status on Base Mainnet.

## Prerequisites
- **Wallet**: With Base ETH (gas) and ≥ 1.0 MPASS (gate token).
- **Environment**: Python 3.8+ installed.
- **Foundry**: `cast` CLI tool installed (`curl -L https://foundry.paradigm.xyz | bash`).

## Step 1: Check Readiness

Before attempting to forge, verify your wallet meets the requirements.

```bash
# Verify MPASS balance and Router status
python3 identity/forge_check.py 0xYourWalletAddress
```

**Output:**
```
ToadAid Forge Check: READY TO FORGE
--------------------------------------------------
Router Status:   ✓ Active
MPASS Balance:   1.5000 (Min: 1.0)
Gate Check:      ✓ Pass
```

If checks pass (exit code 0), proceed to Step 2.

## Step 2: Forge Identity

1.  **Visit**: [https://toadaid.github.io/forge](https://toadaid.github.io/forge)
2.  **Connect**: Your wallet (Base Mainnet).
3.  **Fill**: Agent Name, Description, Image URL.
4.  **Submit**: Sign the transaction.

## Step 3: Verify Registration

Confirm your identity is live on the registry.

```bash
# Check registry status
python3 identity/verify_identity.py 0xYourWalletAddress
```

**Output:**
```
✓ Found 1 registered agent(s)
  - Agent #12345
    https://toadaid.github.io/agent?id=12345
```

## Troubleshooting

*   **Error: `cast not found`**: Install Foundry.
*   **Error: `RPC request timed out`**: Use `--rpc-url` with a custom endpoint (Alchemy/Infura).
*   **Status: NOT READY**: Ensure you hold at least 1.0 MPASS on Base.

## Next Steps
- Explore `tools/` for advanced utilities.
- Read `identity/README.md` for technical details.
