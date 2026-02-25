#!/usr/bin/env python3
"""
verify_identity.py

Check wallet registration status in ToadAid ERC-8004 registry.
Read-only. No private keys required.

Uses `cast` (Foundry) for onchain reads via subprocess.

Usage:
    python identity/verify_identity.py 0xWalletAddress
    python identity/verify_identity.py --agent-id 19173
"""

import sys
import subprocess
import os
import re

# Registry contracts (Base Mainnet)
REGISTRY_PROXY = "0x8004A169F84a3325136EB29fA0ceB6D2e539a432"
BASE_IMPL = "0x7274e874CA62410a93Bd8bf61c69d8045E399c02"


def is_valid_address(addr):
    """Validate Ethereum address format."""
    if not addr:
        return False
    addr = addr.lower()
    return bool(re.match(r'^0x[a-f0-9]{40}$', addr))


def call_cast(contract, function, args=None):
    """Safe cast call wrapper."""
    cmd = ["cast", "call", contract, function]
    if args:
        cmd.extend(args)
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    if result.returncode != 0:
        raise RuntimeError(f"cast failed: {result.stderr}")
    
    return result.stdout.strip()


def check_registry_by_address(address):
    """
    Check if wallet has registered agents via ERC-8004.
    Returns list of agent IDs or empty list.
    """
    print(f"Checking registry for: {address}")
    print(f"Registry Proxy: {REGISTRY_PROXY}")
    print(f"Base Implementation: {BASE_IMPL}")
    print("")
    
    agents = []
    
    # Try to get token count for this address
    try:
        # balanceOf(address) returns uint256
        balance = call_cast(
            REGISTRY_PROXY,
            "balanceOf(address)",
            [address]
        )
        balance_int = int(balance)
        print(f"Registered agents: {balance_int}")
        print("")
        
        if balance_int > 0:
            # Get each token ID owned
            for i in range(balance_int):
                try:
                    token_id = call_cast(
                        REGISTRY_PROXY,
                        "tokenOfOwnerByIndex(address,uint256)",
                        [address, str(i)]
                    )
                    agents.append(int(token_id))
                except RuntimeError as e:
                    print(f"Warning: Could not fetch token {i}: {e}")
                    continue
    except RuntimeError as e:
        print(f"[!] Registry query failed: {e}")
        print("[!] Ensure ETH_RPC_URL is set to a Base Mainnet endpoint")
        return []
    except Exception as e:
        print(f"[!] Unexpected error: {e}")
        return []
    
    return agents


def check_agent_by_id(agent_id):
    """Check specific agent ID details."""
    print(f"Looking up Agent #{agent_id}")
    print(f"Base Implementation: {BASE_IMPL}")
    print("")
    
    try:
        # Try to get tokenURI
        token_uri = call_cast(
            REGISTRY_PROXY,
            "tokenURI(uint256)",
            [str(agent_id)]
        )
        print(f"Token URI: {token_uri}")
        
        # Try to get owner
        owner = call_cast(
            REGISTRY_PROXY,
            "ownerOf(uint256)",
            [str(agent_id)]
        )
        print(f"Owner: {owner}")
        
    except RuntimeError as e:
        print(f"[!] Agent query failed: {e}")
        print("[!] Agent may not exist or RPC may be unavailable")


def print_registry_links(address=None, agent_id=None):
    """Print useful registry links."""
    print("=" * 50)
    print("Useful Links:")
    print("=" * 50)
    print(f"Registry Contract: https://basescan.org/address/{REGISTRY_PROXY}")
    print(f"Implementation:    https://basescan.org/address/{BASE_IMPL}")
    print(f"Agent Directory:   https://toadaid.github.io/agent")
    print(f"Forge Portal:      https://toadaid.github.io/forge")
    
    if address:
        print(f"Wallet Explorer:   https://basescan.org/address/{address}")
    
    if agent_id:
        print(f"Token Explorer:    https://basescan.org/token/{BASE_IMPL}?a={agent_id}")
    
    print("")


def main():
    """Main entry point."""
    print("=" * 50)
    print("ToadAid Identity Verification")
    print("=" * 50)
    print("")
    
    # Check for cast
    try:
        subprocess.run(["cast", "--version"], capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        print("[!] Error: `cast` not found")
        print("[!] Install Foundry: https://book.getfoundry.sh/getting-started/installation")
        sys.exit(1)
    
    # Parse arguments
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python identity/verify_identity.py 0xWalletAddress")
        print("  python identity/verify_identity.py --agent-id 19173")
        print("")
        print_registry_links()
        sys.exit(0)
    
    arg = sys.argv[1]
    
    if arg == "--agent-id":
        if len(sys.argv) < 3:
            print("Error: --agent-id requires an ID number")
            sys.exit(1)
        try:
            agent_id = int(sys.argv[2])
            check_agent_by_id(agent_id)
            print_registry_links(agent_id=agent_id)
        except ValueError:
            print(f"Error: Invalid agent ID: {sys.argv[2]}")
            sys.exit(1)
    elif is_valid_address(arg):
        agents = check_registry_by_address(arg)
        print_registry_links(address=arg)
        
        if agents:
            print(f"✓ Found {len(agents)} registered agent(s)")
            for agent in agents:
                print(f"  - Agent #{agent}")
                print(f"    https://toadaid.github.io/agent?id={agent}")
        else:
            print("✗ No agents found for this wallet")
            print("")
            print("To register:")
            print("  1. Visit https://toadaid.github.io/forge")
            print("  2. Connect wallet")
            print("  3. Complete registration")
    else:
        print(f"Error: Invalid argument: {arg}")
        print("Expected: 0x... wallet address or --agent-id NUMBER")
        sys.exit(1)
    
    print("")
    print("Done.")


if __name__ == "__main__":
    main()
