# Pharos NFT Appraisal IO Schema

## Input

```json
{
  "prompt": "Appraise this Pharos Atlantic NFT contract: 0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
  "contract_address": "0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
  "network": "pharos-atlantic",
  "rpc_url": "optional custom Pharos RPC URL",
  "openai_api_key": "optional",
  "timeout_seconds": 20
}
```

Supported networks:

- `pharos`
- `pharos-atlantic`
- `pharos-mainnet`

Default network: live Pharos mainnet RPC.

## Output

```json
{
  "schema_version": "1.0",
  "status": "success",
  "skill": "nft_appraisal_skill",
  "source": "pharos-json-rpc",
  "target": {
    "network": "pharos-atlantic",
    "chain_id": 688689,
    "contract_address": "0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
    "rpc_url": "https://atlantic.dplabs-internal.com",
    "explorer_url": "https://atlantic.pharosscan.xyz"
  },
  "collection": {
    "address": "0x22614Ca3393E83DA6411A45f012239Bafc258ABD",
    "name": "Pharos Atlantic Testnet Badge",
    "symbol": "PATB",
    "token_standard": "ERC721",
    "total_supply": 658217,
    "contract_uri": "ipfs://QmcH9u5J2yLCv3AyhHBQ6yVcJT58Ts5wbzxBsB3CmrVTLV/0",
    "metadata_available": true
  },
  "interfaces": {
    "ERC721": true,
    "ERC721Metadata": true,
    "ERC1155": false,
    "ERC1155MetadataURI": false
  },
  "appraisal": {
    "summary": "Source-grounded, non-financial Pharos contract appraisal.",
    "confidence": "low|medium",
    "risk_flags": [],
    "limitations": [],
    "market_data": {
      "floor_price": null,
      "currency": null,
      "note": "No Pharos marketplace data source is queried by this skill."
    }
  }
}
```

## Error Codes

- `MISSING_CONTRACT_ADDRESS`
- `INVALID_CONTRACT_ADDRESS`
- `UNSUPPORTED_NETWORK`
- `NOT_CONTRACT`
- `RPC_ERROR`
- `UNSAFE_INPUT`
- `UNEXPECTED_ERROR`
