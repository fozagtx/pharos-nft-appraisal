# NFT Appraisal IO Schema

## Input

```json
{
  "prompt": "Appraise this Base NFT collection: 0x0000000000000000000000000000000000000000",
  "contract_address": "0x0000000000000000000000000000000000000000",
  "chain": "eth",
  "openai_api_key": "optional",
  "alchemy_api_key": "optional",
  "api_keys": {
    "openai": "optional",
    "alchemy": "optional"
  },
  "include_raw_alchemy": false,
  "timeout_seconds": 15
}
```

## Output

```json
{
  "schema_version": "1.0",
  "status": "success",
  "skill": "nft_appraisal_skill",
  "source": "alchemy",
  "target": {
    "chain": "eth",
    "network": "eth-mainnet",
    "contract_address": "0x..."
  },
  "collection": {
    "name": "string",
    "symbol": "string",
    "token_type": "ERC721",
    "total_supply": "10000",
    "opensea": {
      "floor_price": 1.23,
      "collection_name": "string"
    }
  },
  "appraisal": {
    "summary": "Non-financial appraisal.",
    "confidence": "low",
    "risk_flags": [],
    "limitations": []
  }
}
```

