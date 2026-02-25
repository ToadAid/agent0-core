# Tooling Standard

Standard CLI contract for ToadAid Agent0 Core tools.

## Design Principles

1. **Read-only by default** — No wallet mutations unless explicitly requested
2. **Subprocess-safe** — Tools use external CLI (cast, curl) via subprocess
3. **Clear output** — Structured, parseable, human-readable
4. **Safe defaults** — Fail closed, warn clearly, require opt-in for risk
5. **No secrets in code** — Environment variables or secure vaults only

## CLI Contract

Every tool follows this interface:

### Arguments

```bash
# Primary argument: wallet address
tool_name 0xWalletAddress [options]

# Flags for alternative modes
tool_name --show-config      # Display configuration
tool_name --help             # Usage information
```

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success, expected result |
| 1 | Error (invalid input, execution failure) |
| 2 | Warning (low balance, not found) |

### Output Format

```
=== Header ===

Status: [OK | NOT_FOUND | ERROR]
Details: Human-readable explanation

Key: Value
Key: Value

=== Footer ===

Next steps or recommendations
```

## Subprocess Pattern

Tools use `cast` (Foundry) for onchain reads:

```python
import subprocess

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
```

## Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `ETH_RPC_URL` | Base Mainnet RPC endpoint | Yes |
| `GITHUB_TOKEN` | For repo operations | For CI only |
| `PRIVATE_KEY` | **Never stored** | N/A |

## Validation

All addresses validated before use:

```python
import re

def is_valid_address(addr):
    """Validate Ethereum address format."""
    if not addr:
        return False
    addr = addr.lower()
    return bool(re.match(r'^0x[a-f0-9]{40}$', addr))
```

## Error Handling

- Catch all exceptions
- Print friendly error message
- Return exit code 1
- Never expose stack traces to user

## Testing

Each tool includes:
- `--dry-run` flag where applicable
- Mock responses for CI
- Syntax validation via `py_compile`

## Dependencies

- Python 3.8+
- `cast` (Foundry CLI)
- Standard library only (no pip deps for runtime)

## Example

```python
#!/usr/bin/env python3
"""Example tool following standard."""

import sys
import subprocess
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: tool 0xAddress")
        sys.exit(1)
    
    addr = sys.argv[1]
    
    if not is_valid_address(addr):
        print(f"Error: Invalid address: {addr}")
        sys.exit(1)
    
    try:
        result = call_cast(CONTRACT, "balanceOf(address)", [addr])
        print(f"Balance: {result}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

## Future Extensions

- JSON output mode (`--json`)
- Config file support (`~/.toad/config`)
- Caching layer for repeated queries
