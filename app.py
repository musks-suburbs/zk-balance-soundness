# app.py
import os
import sys
import time
import json
import argparse
from typing import Optional
from web3 import Web3

DEFAULT_RPC = os.environ.get("RPC_URL", "https://mainnet.infura.io/v3/YOUR_INFURA_KEY")

def fetch_balance(w3: Web3, address: str, block: Optional[int]) -> int:
    """
    Fetches the ETH balance of an address at a specific block.
    """
    try:
        address = Web3.to_checksum_address(address)
        balance = w3.eth.get_balance(address, block_identifier=block)
        return balance
    except Exception as e:
        print(f"❌ Failed to fetch balance for {address}: {e}")
        return -1

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="zk-balance-soundness — verify ETH balance soundness for contracts and wallets (useful for Aztec/Zama projects and general Web3 audits)."
    )
    p.add_argument("--rpc", default=DEFAULT_RPC, help="EVM RPC URL (default from RPC_URL)")
    p.add_argument("--address", required=True, help="Ethereum address to check")
    p.add_argument("--block", type=int, help="Optional block number for historical balance check")
    p.add_argument("--expected", type=float, help="Expected balance in ETH for comparison")
    p.add_argument("--json", action="store_true", help="Output result as JSON")
    p.add_argument("--timeout", type=int, default=30, help="RPC timeout (seconds)")
    return p.parse_args()

def main() -> None:
    start_time = time.time()
    args = parse_args()

    w3 = Web3(Web3.HTTPProvider(args.rpc, request_kwargs={"timeout": args.timeout}))
    if not w3.is_connected():
        print("❌ RPC connection failed. Check your RPC_URL or --rpc parameter.")
        sys.exit(1)

    print("🔧 zk-balance-soundness")
    print(f"🔗 RPC: {args.rpc}")
    try:
        print(f"🧭 Chain ID: {w3.eth.chain_id}")
    except Exception:
        pass
    print(f"🏷️ Address: {args.address}")
    block_label = args.block if args.block is not None else "latest"
    print(f"🧱 Block: {block_label}")

    wei_balance = fetch_balance(w3, args.address, args.block)
    if wei_balance < 0:
        sys.exit(2)

    eth_balance = w3.from_wei(wei_balance, "ether")
    print(f"💰 Balance: {eth_balance} ETH")

    result_match = None
    if args.expected is not None:
        result_match = abs(float(eth_balance) - args.expected) < 1e-12
        status = "✅ MATCH" if result_match else "❌ MISMATCH"
        print(f"Expected: {args.expected} ETH | {status}")

    elapsed = time.time() - start_time
    print(f"⏱️ Completed in {elapsed:.2f}s")

    if args.json:
        output = {
            "rpc": args.rpc,
            "chain_id": None,
            "address": Web3.to_checksum_address(args.address),
            "block": block_label,
            "balance_eth": float(eth_balance),
            "expected_eth": args.expected,
            "match": result_match,
            "elapsed_seconds": round(elapsed, 2),
        }
        try:
            output["chain_id"] = w3.eth.chain_id
        except Exception:
            pass
        print(json.dumps(output, ensure_ascii=False, indent=2))

    sys.exit(0 if (result_match is None or result_match) else 2)

if __name__ == "__main__":
    main()
