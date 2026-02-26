#!/usr/bin/env python3
"""
forge_check.py - Verify readiness to forge a ToadAid identity.

Design:
- Read-only checks against Base Mainnet.
- Verifies MPASS balance (gating requirement).
- Verifies Router contract availability.
- Exit codes: 0=Ready, 2=Not Ready, 3=Error.

Usage:
  python3 identity/forge_check.py 0xWalletAddress [options]
"""

import sys
import subprocess
import json
import re
import argparse

# Contract Addresses (Base Mainnet)
CONTRACTS = {
    "REGISTRY_ROUTER": "0x17163e538029b04D4cC24f82aa6AC3B877Bd0e0",
    "REPUTATION_ROUTER": "0x94D7B431dD8eAFc9E1b71624DF0a90468622537a",
    "MPASS_TOKEN": "0xdb9e64465d4b5fbc7ee9091c459094efc7df5cde",
    "REGISTRY_PROXY": "0x8004A169F84a3325136EB29fA0ceB6D2e539a432"  # Canonical Agent 0 Registry
}

# Gate Requirements
MPASS_MIN_BALANCE = 1.0

def is_valid_address(addr):
    """Validate Ethereum address format."""
    if not addr: return False
    return bool(re.match(r'^0x[a-fA-F0-9]{40}$', addr))

def call_cast(args, rpc_url=None):
    """Safe cast call wrapper."""
    cmd = ["cast"] + args
    if rpc_url:
        cmd.extend(["--rpc-url", rpc_url])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            raise RuntimeError(f"cast failed: {result.stderr.strip()}")
        return result.stdout.strip()
    except FileNotFoundError:
        raise RuntimeError("cast not found. Install Foundry: https://book.getfoundry.sh/")
    except subprocess.TimeoutExpired:
        raise RuntimeError("RPC request timed out")

def get_balance(token, wallet, rpc_url=None):
    """Get ERC-20 balance (formatted)."""
    # 1. Get decimals
    try:
        decimals = int(call_cast(["call", token, "decimals()(uint8)"], rpc_url))
    except Exception:
        decimals = 18 # Default if fails
    
    # 2. Get balance
    raw = call_cast(["call", token, "balanceOf(address)(uint256)", wallet], rpc_url)
    return int(raw) / (10 ** decimals)

def check_contract_code(address, rpc_url=None):
    """Verify contract exists on chain."""
    code = call_cast(["code", address], rpc_url)
    return code != "0x"

def main():
    parser = argparse.ArgumentParser(description="Check ToadAid Forge readiness.")
    parser.add_argument("wallet", help="Wallet address to check")
    parser.add_argument("--rpc-url", help="Base Mainnet RPC URL", default="https://mainnet.base.org")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    args = parser.parse_args()

    if not is_valid_address(args.wallet):
        print(f"Error: Invalid wallet address: {args.wallet}", file=sys.stderr)
        sys.exit(3)

    results = {
        "wallet": args.wallet,
        "ready": False,
        "checks": {},
        "contracts": CONTRACTS
    }

    try:
        # 1. Check Router Status
        router_ok = check_contract_code(CONTRACTS["REGISTRY_ROUTER"], args.rpc_url)
        results["checks"]["router_active"] = router_ok

        # 2. Check MPASS Balance
        mpass_bal = get_balance(CONTRACTS["MPASS_TOKEN"], args.wallet, args.rpc_url)
        results["checks"]["mpass_balance"] = mpass_bal
        results["checks"]["mpass_sufficient"] = mpass_bal >= MPASS_MIN_BALANCE

        # 3. Determine Readiness
        if router_ok and (mpass_bal >= MPASS_MIN_BALANCE):
            results["ready"] = True
            exit_code = 0
            status_msg = "READY TO FORGE"
        else:
            exit_code = 2
            status_msg = "NOT READY"

    except Exception as e:
        if args.json:
            print(json.dumps({"error": str(e)}))
        else:
            print(f"Error: {e}", file=sys.stderr)
        sys.exit(3)

    # Output
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("=" * 50)
        print(f"ToadAid Forge Check: {status_msg}")
        print("=" * 50)
        print(f"Wallet: {args.wallet}")
        print("-" * 50)
        print(f"Router Status:   {'✓ Active' if results['checks']['router_active'] else '✗ Inactive/Unreachable'}")
        print(f"MPASS Balance:   {results['checks']['mpass_balance']:.4f} (Min: {MPASS_MIN_BALANCE})")
        print(f"Gate Check:      {'✓ Pass' if results['checks']['mpass_sufficient'] else '✗ Fail'}")
        print("-" * 50)
        if results["ready"]:
            print("Next Step: Visit https://toadaid.github.io/forge")
        else:
            print("Action Required: Acquire >= 1.0 MPASS to forge identity.")
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
