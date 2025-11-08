# zk-balance-soundness

## Overview
A minimal CLI tool that verifies the on-chain ETH balance of an address, enabling fast and reproducible **balance soundness** checks for smart contracts, bridges, or wallets.  
It is useful for projects like **Aztec**, **Zama**, or any privacy/rollup protocol that relies on transparent base-layer accounting.

## Features
- Fetch ETH balance at the latest or a specific historical block  
- Compare actual vs. expected balance  
- JSON output for CI/CD integration  
- Lightweight and compatible with mainnet, L2s, or private RPCs  

## Installation
1. Install Python 3.9+  
2. Install dependencies:
   pip install web3
3. Optionally set your RPC endpoint:
   export RPC_URL=https://mainnet.infura.io/v3/YOUR_KEY

## Usage
Check current balance:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa

Check historical balance at a block:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa --block 21000000

Compare with an expected value:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa --expected 32.0

Output JSON for automation:
   python app.py --address 0x00000000219ab540356cBB839Cbe05303d7705Fa --json

## Example Output
🔧 zk-balance-soundness  
🔗 RPC: https://mainnet.infura.io/v3/YOUR_KEY  
🧭 Chain ID: 1  
🏷️ Address: 0x00000000219ab540356cBB839Cbe05303d7705Fa  
🧱 Block: latest  
💰 Balance: 32.0 ETH  
✅ MATCH  
⏱️ Completed in 0.31s

## Notes
- If the address is a contract, this checks its current ETH holdings.  
- For Aztec/Zama integrations, this can be combined with storage root checks to confirm end-to-end state soundness.  
- The comparison threshold uses a small epsilon (1e-12 ETH) to tolerate rounding differences.  
- Exit codes:  
  0 → soundness verified (match or no expected provided)  
  2 → mismatch or RPC failure.  
- Works for EOAs, smart contracts, and multi-sig wallets equally — it simply reads the on-chain balance.  
- Can be integrated into monitoring scripts for bridges, vaults, or rollup deposit contracts.  
- For reproducibility, always use a specific block number instead of “latest”.  
