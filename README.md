<p align="center">
  <img src="assets/logo.svg" alt="Pharos NFT Appraisal logo" width="180">
</p>

# Pharos NFT Appraisal

A Pharos-compatible skill for appraising NFT contracts on Pharos. It extracts a contract address from a user prompt, inspects the contract through Pharos JSON-RPC, checks common NFT interfaces, reads standard collection metadata when available, and returns a cautious appraisal.

This skill is built for the Skill-to-Agent Dual Cascade Hackathon as a reusable module that any agent can call.

## Features

- Extracts an NFT contract address from natural-language prompts
- Uses Pharos JSON-RPC, not off-network NFT APIs
- Defaults to the live Pharos RPC at `https://rpc.pharos.xyz/`
- Supports Pharos mainnet, Pharos Atlantic, and configurable Pharos RPC URLs
- Checks ERC721 and ERC1155 interface support through `eth_call`
- Reads `name`, `symbol`, `totalSupply`, and `contractURI` when the contract exposes them
- Produces risk flags, limitations, citations, and a non-financial appraisal summary

## Requirements

- Python 3.10+
- Pharos RPC access

Optional environment variables:

- `PHAROS_RPC_URL` - override the default Pharos RPC endpoint
- `OPENAI_API_KEY` - optional structured prompt extraction
- `OPENAI_EXTRACT_MODEL` - optional extraction model override

No third-party Python package is required; the skill uses Python standard-library HTTP utilities.

## Install as a Skill

```bash
npx skills add https://github.com/fozagtx/pharos-nft-appraisal
```

Optional runtime configuration:

```bash
export PHAROS_RPC_URL="https://rpc.pharos.xyz/"
export OPENAI_API_KEY="optional_openai_key"
```

## Quick Start

```bash
python3 scripts/run_appraisal.py --metadata examples/nft-appraisal-input.json --pretty
```

Or pipe JSON through stdin:

```bash
printf '%s\n' '{"prompt":"appraise this Pharos Atlantic NFT contract: 0x22614Ca3393E83DA6411A45f012239Bafc258ABD","network":"pharos-atlantic"}' \
  | python3 scripts/run_appraisal.py --pretty
```

## Input

Natural-language prompt:

```json
{
  "prompt": "appraise this Pharos Atlantic NFT contract: 0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
  "network": "pharos-atlantic"
}
```

Explicit target:

```json
{
  "contract_address": "0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
  "network": "pharos-atlantic"
}
```

Supported network values:

- `pharos`
- `pharos-atlantic`
- `pharos-mainnet`

If no network is supplied, the skill defaults to live Pharos mainnet RPC.

## Output

The skill returns JSON containing:

- extracted `target`
- extraction method
- Pharos RPC network details
- detected NFT interfaces
- collection metadata available from contract reads
- cautious appraisal summary
- confidence level
- risk flags
- limitations
- provider citation

Example shape:

```json
{
  "status": "success",
  "skill": "nft_appraisal_skill",
  "source": "pharos-json-rpc",
  "target": {
    "network": "pharos-atlantic",
    "chain_id": 688689,
    "contract_address": "0x22614Ca3393E83DA6411A45f012239Bafc258ABD"
  },
  "collection": {
    "name": "Pharos Atlantic Testnet Badge",
    "symbol": "PATB",
    "token_standard": "ERC721",
    "total_supply": 658217,
    "contract_uri": "ipfs://..."
  },
  "appraisal": {
    "summary": "Source-grounded, non-financial appraisal.",
    "confidence": "medium",
    "risk_flags": [],
    "limitations": []
  }
}
```

## Error Behavior

Common errors:

- `MISSING_CONTRACT_ADDRESS`
- `INVALID_CONTRACT_ADDRESS`
- `UNSUPPORTED_NETWORK`
- `NOT_CONTRACT`
- `RPC_ERROR`

Unsupported network names are rejected. Address-only prompts default to Pharos testnet.

## Safety Notes

This skill does not provide buy, sell, hold, price-target, profit, or investment advice. It does not invent sales, volume, ownership, rarity, floor price, or liquidity data. Appraisal claims are limited to Pharos contract reads.

## Skill Files

- `SKILL.md` - Pharos skill manifest and agent instructions
- `scripts/nft_appraisal_skill.py` - reusable `run(metadata)` implementation
- `scripts/run_appraisal.py` - CLI wrapper
- `references/io-schema.md` - detailed input/output schema
- `examples/nft-appraisal-input.json` - sample request
