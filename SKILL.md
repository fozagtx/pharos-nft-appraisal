---
name: pharos-nft-appraisal
description: >
  Use this skill to appraise an NFT collection by extracting an Ethereum or Base
  contract address and chain from a user prompt, fetching collection metadata
  from Alchemy, and returning a cautious JSON appraisal. Supports ETH and BASE
  only. Requires Alchemy and optionally uses OpenAI for prompt extraction.
version: 0.1.0
requires:
  env:
    - ALCHEMY_API_KEY
---

# Pharos NFT Appraisal

Appraise an NFT project from a user prompt or explicit contract metadata. This skill supports only Ethereum mainnet and Base mainnet.

## Run

```bash
python3 scripts/run_appraisal.py --metadata examples/nft-appraisal-input.json --pretty
```

Or through stdin:

```bash
printf '%s\n' '{"prompt":"tell me about 0xed5af388653567af2f388e6224dc7c4b3241c544 on eth"}' \
  | python3 scripts/run_appraisal.py --pretty
```

## Input

```json
{
  "prompt": "tell me about 0xed5af388653567af2f388e6224dc7c4b3241c544, which is on eth",
  "openai_api_key": "optional, prefer OPENAI_API_KEY",
  "alchemy_api_key": "optional, prefer ALCHEMY_API_KEY"
}
```

You can also bypass extraction:

```json
{
  "contract_address": "0xed5af388653567af2f388e6224dc7c4b3241c544",
  "chain": "eth"
}
```

## Output

Returns extracted target, Alchemy collection metadata, floor-price data when present, risk flags, limitations, and a non-financial appraisal summary.

## Guardrails

- Supports only `eth` and `base`.
- No buy, sell, hold, price-target, profit, or investment advice.
- No invented floor price, volume, rarity, ownership, or sales data.
- If chain is missing, return `NEEDS_CHAIN`; do not guess.
- API keys must not be logged or returned.

