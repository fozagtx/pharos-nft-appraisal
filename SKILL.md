---
name: pharos-nft-appraisal
description: >
  Use this skill to appraise an NFT contract on Pharos by extracting a contract
  address from a user prompt, inspecting the contract through Pharos JSON-RPC,
  checking common NFT interfaces, and returning a cautious JSON appraisal.
  Supports Pharos networks only.
version: 0.1.0
requires:
  env: []
---

# Pharos NFT Appraisal

Appraise an NFT contract from a user prompt or explicit contract address. This skill is Pharos-only.

## Install

```bash
npx skills add https://github.com/fozagtx/pharos-nft-appraisal
```

## Run

```bash
python3 scripts/run_appraisal.py --metadata examples/nft-appraisal-input.json --pretty
```

Or through stdin:

```bash
printf '%s\n' '{"prompt":"appraise this Pharos Atlantic NFT contract: 0x22614Ca3393E83DA6411A45f012239Bafc258ABD","network":"pharos-atlantic"}' \
  | python3 scripts/run_appraisal.py --pretty
```

## Input

```json
{
  "prompt": "appraise this Pharos Atlantic NFT contract: 0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
  "network": "pharos-atlantic",
  "rpc_url": "optional custom Pharos RPC URL",
  "openai_api_key": "optional, prefer OPENAI_API_KEY"
}
```

You can also bypass extraction:

```json
{
  "contract_address": "0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
  "network": "pharos-atlantic"
}
```

## Output

Returns extracted target, Pharos RPC network details, contract bytecode presence, ERC721/ERC1155 interface checks, standard metadata reads, risk flags, limitations, and a non-financial appraisal summary.

## Guardrails

- Supports Pharos networks only.
- No buy, sell, hold, price-target, profit, or investment advice.
- No invented floor price, volume, rarity, ownership, or sales data.
- Do not claim market value unless a Pharos marketplace data source is explicitly added later.
- API keys and RPC secrets must not be logged or returned.
