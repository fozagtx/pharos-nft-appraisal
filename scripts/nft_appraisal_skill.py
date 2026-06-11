"""NFT appraisal skill for ETH and Base collections using Alchemy."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from typing import Any, Dict, Mapping, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


SKILL_NAME = "nft_appraisal_skill"
ALCHEMY_NETWORKS = {
    "eth": {"network": "eth-mainnet", "host": "eth-mainnet.g.alchemy.com"},
    "base": {"network": "base-mainnet", "host": "base-mainnet.g.alchemy.com"},
}
CHAIN_ALIASES = {
    "eth": "eth",
    "ethereum": "eth",
    "mainnet": "eth",
    "ethereum mainnet": "eth",
    "base": "base",
    "base mainnet": "base",
}
UNSUPPORTED_CHAIN_TERMS = {"polygon", "matic", "arbitrum", "optimism", "solana", "bnb", "avalanche"}
ADDRESS_RE = re.compile(r"0x[a-fA-F0-9]{40}")
UNSAFE_KEYS = {"headers", "cookies", "proxy", "proxies", "private_key", "seed_phrase", "shell", "command", "file_path"}


class SkillError(Exception):
    """Stable skill error."""

    def __init__(self, code: str, message: str, status: str = "error", retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.status = status
        self.retryable = retryable


def run(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    """Run NFT collection appraisal."""

    generated_at = _now_iso()
    try:
        metadata = _coerce_metadata(args, kwargs)
        _reject_unsafe(metadata)
        alchemy_api_key = _api_key(metadata, "alchemy", "ALCHEMY_API_KEY")
        if not alchemy_api_key:
            raise SkillError("MISSING_API_KEY", "Provide ALCHEMY_API_KEY, alchemy_api_key, or api_keys.alchemy.")

        target, extraction = _extract_target(metadata)
        network = ALCHEMY_NETWORKS[target["chain"]]
        collection = _fetch_contract_metadata(
            alchemy_api_key,
            network["host"],
            target["contract_address"],
            timeout=_clamp_int(metadata.get("timeout_seconds", 15), 5, 60),
        )
        normalized = _normalize_collection(collection)
        appraisal = _appraise(normalized, target)

        output: Dict[str, Any] = {
            "schema_version": "1.0",
            "status": "success",
            "skill": SKILL_NAME,
            "source": "alchemy",
            "request_id": metadata.get("request_id"),
            "generated_at": generated_at,
            "extraction": extraction,
            "target": {
                "chain": target["chain"],
                "network": network["network"],
                "contract_address": target["contract_address"],
            },
            "collection": normalized,
            "appraisal": appraisal,
            "citations": [
                {
                    "provider": "Alchemy",
                    "endpoint": "getContractMetadata",
                    "network": network["network"],
                    "contract_address": target["contract_address"],
                }
            ],
            "errors": [],
        }
        if bool(metadata.get("include_raw_alchemy", False)):
            output["raw_alchemy"] = collection
        return output
    except SkillError as exc:
        return _error(exc.code, exc.message, exc.status, exc.retryable, generated_at)
    except Exception as exc:  # pragma: no cover
        return _error("UNEXPECTED_ERROR", str(exc), "error", False, generated_at)


def _coerce_metadata(args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> Dict[str, Any]:
    metadata: Dict[str, Any] = {}
    if args:
        if len(args) == 1 and isinstance(args[0], Mapping):
            metadata.update(dict(args[0]))
        elif len(args) == 1 and isinstance(args[0], str):
            metadata["prompt"] = args[0]
        else:
            raise SkillError("INVALID_METADATA", "run accepts a metadata dict or prompt string.")
    nested = kwargs.get("metadata")
    if isinstance(nested, Mapping):
        metadata.update(dict(nested))
    for key, value in kwargs.items():
        if key != "metadata":
            metadata[key] = value
    return metadata


def _reject_unsafe(metadata: Mapping[str, Any]) -> None:
    found = sorted(key for key in metadata if key in UNSAFE_KEYS)
    if found:
        raise SkillError("UNSAFE_INPUT", f"Unsupported metadata keys: {', '.join(found)}")


def _extract_target(metadata: Mapping[str, Any]) -> Tuple[Dict[str, str], Dict[str, Any]]:
    direct_address = str(metadata.get("contract_address") or "").strip()
    direct_chain = str(metadata.get("chain") or "").strip()
    if direct_address or direct_chain:
        address = _validate_address(direct_address)
        chain = _normalize_chain(direct_chain)
        return {"contract_address": address, "chain": chain}, {"method": "metadata", "warnings": []}

    prompt = str(metadata.get("prompt") or metadata.get("user_prompt") or "").strip()
    if not prompt:
        raise SkillError("MISSING_CONTRACT_ADDRESS", "Provide prompt or contract_address and chain.")

    openai_key = _api_key(metadata, "openai", "OPENAI_API_KEY")
    if openai_key:
        extracted = _extract_with_openai(prompt, openai_key)
        if extracted:
            try:
                return {
                    "contract_address": _validate_address(str(extracted.get("contract_address") or "")),
                    "chain": _normalize_chain(str(extracted.get("chain") or "")),
                }, {"method": "openai", "warnings": []}
            except SkillError:
                pass

    address_match = ADDRESS_RE.search(prompt)
    if not address_match:
        raise SkillError("MISSING_CONTRACT_ADDRESS", "Could not find an NFT contract address in the prompt.")
    chain = _detect_chain(prompt)
    if not chain:
        raise SkillError("NEEDS_CHAIN", "Address found, but chain is missing. Specify eth or base.", status="needs_input")
    return {
        "contract_address": _validate_address(address_match.group(0)),
        "chain": chain,
    }, {"method": "regex", "warnings": ["OpenAI extraction unavailable or unnecessary; used regex fallback."]}


def _extract_with_openai(prompt: str, api_key: str) -> Optional[Dict[str, str]]:
    payload = {
        "model": os.getenv("OPENAI_EXTRACT_MODEL", "gpt-4o-mini"),
        "response_format": {"type": "json_object"},
        "messages": [
            {
                "role": "system",
                "content": "Extract JSON only: {\"contract_address\": string|null, \"chain\": \"eth\"|\"base\"|null}. Supports only Ethereum mainnet and Base.",
            },
            {"role": "user", "content": prompt},
        ],
        "temperature": 0,
    }
    request = Request(
        "https://api.openai.com/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {api_key}", "User-Agent": f"{SKILL_NAME}/0.1.0"},
        method="POST",
    )
    try:
        with urlopen(request, timeout=20) as response:
            body = json.loads(response.read().decode("utf-8"))
        content = body["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception:
        return None


def _validate_address(address: str) -> str:
    if not ADDRESS_RE.fullmatch(address or ""):
        raise SkillError("INVALID_CONTRACT_ADDRESS", "Contract address must be 0x followed by 40 hex characters.")
    return address


def _normalize_chain(chain: str) -> str:
    raw = " ".join(str(chain or "").lower().replace("-", " ").replace("_", " ").split())
    if raw in CHAIN_ALIASES:
        return CHAIN_ALIASES[raw]
    if raw in UNSUPPORTED_CHAIN_TERMS:
        raise SkillError("UNSUPPORTED_CHAIN", "Only eth and base are supported.")
    if not raw:
        raise SkillError("NEEDS_CHAIN", "Specify chain as eth or base.", status="needs_input")
    raise SkillError("UNSUPPORTED_CHAIN", "Only eth and base are supported.")


def _detect_chain(prompt: str) -> Optional[str]:
    lowered = prompt.lower()
    for term in UNSUPPORTED_CHAIN_TERMS:
        if re.search(rf"\b{re.escape(term)}\b", lowered):
            raise SkillError("UNSUPPORTED_CHAIN", "Only eth and base are supported.")
    if re.search(r"\bbase\b", lowered):
        return "base"
    if re.search(r"\b(eth|ethereum|mainnet)\b", lowered):
        return "eth"
    return None


def _fetch_contract_metadata(api_key: str, host: str, contract_address: str, timeout: int) -> Dict[str, Any]:
    url = f"https://{host}/nft/v3/{api_key}/getContractMetadata?{urlencode({'contractAddress': contract_address})}"
    request = Request(url, headers={"User-Agent": f"{SKILL_NAME}/0.1.0"}, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            data = json.loads(response.read().decode("utf-8"))
        if not data or not (data.get("name") or data.get("openseaMetadata") or data.get("tokenType")):
            raise SkillError("NOT_FOUND", "Alchemy returned no usable contract metadata.")
        return data
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        if exc.code in {401, 403}:
            raise SkillError("ALCHEMY_AUTH_FAILED", "Alchemy rejected the API key.")
        if exc.code == 404:
            raise SkillError("NOT_FOUND", "NFT contract metadata was not found.")
        if exc.code == 429:
            raise SkillError("PROVIDER_ERROR", "Alchemy rate limit reached.", retryable=True)
        raise SkillError("PROVIDER_ERROR", f"Alchemy HTTP {exc.code}: {detail}", retryable=500 <= exc.code < 600)
    except URLError as exc:
        raise SkillError("PROVIDER_ERROR", f"Alchemy request failed or timed out: {exc.reason}", retryable=True)
    except json.JSONDecodeError:
        raise SkillError("PROVIDER_ERROR", "Alchemy returned invalid JSON.", retryable=True)


def _normalize_collection(data: Mapping[str, Any]) -> Dict[str, Any]:
    opensea = data.get("openseaMetadata") if isinstance(data.get("openseaMetadata"), Mapping) else {}
    return {
        "address": data.get("address"),
        "name": data.get("name"),
        "symbol": data.get("symbol"),
        "token_type": data.get("tokenType"),
        "total_supply": data.get("totalSupply"),
        "contract_deployer": data.get("contractDeployer"),
        "deployed_block_number": data.get("deployedBlockNumber"),
        "opensea": {
            "collection_name": opensea.get("collectionName"),
            "floor_price": opensea.get("floorPrice"),
            "safelist_request_status": opensea.get("safelistRequestStatus"),
            "image_url": opensea.get("imageUrl"),
            "description": opensea.get("description"),
            "external_url": opensea.get("externalUrl"),
            "twitter_username": opensea.get("twitterUsername"),
            "discord_url": opensea.get("discordUrl"),
            "last_ingested_at": opensea.get("lastIngestedAt"),
        },
    }


def _appraise(collection: Mapping[str, Any], target: Mapping[str, str]) -> Dict[str, Any]:
    opensea = collection.get("opensea") if isinstance(collection.get("opensea"), Mapping) else {}
    floor = opensea.get("floor_price")
    risk_flags = []
    limitations = [
        "This is not financial advice.",
        "Appraisal is limited to Alchemy collection metadata.",
        "No independent sales, rarity, holder, or volume analysis is performed.",
    ]
    if floor in {None, "", 0}:
        risk_flags.append("missing_floor_price")
        limitations.append("Alchemy/OpenSea metadata did not provide a floor price.")
    if not opensea.get("safelist_request_status"):
        risk_flags.append("unknown_safelist_status")
    if not collection.get("total_supply"):
        risk_flags.append("unknown_total_supply")

    name = collection.get("name") or opensea.get("collection_name") or "this NFT collection"
    floor_text = f"reported floor price is {floor} ETH" if floor not in {None, "", 0} else "floor price is not available from Alchemy metadata"
    confidence = "medium" if floor not in {None, "", 0} and collection.get("total_supply") else "low"
    return {
        "summary": (
            f"{name} on {target['chain']} was identified from Alchemy contract metadata. "
            f"The {floor_text}. Treat this as a metadata appraisal, not an investment recommendation."
        ),
        "floor_price": {"value": floor, "currency": "ETH", "source": "alchemy.openseaMetadata.floorPrice"},
        "confidence": confidence,
        "risk_flags": risk_flags,
        "limitations": limitations,
    }


def _api_key(metadata: Mapping[str, Any], name: str, env_name: str) -> str:
    api_keys = metadata.get("api_keys")
    nested = ""
    if isinstance(api_keys, Mapping):
        nested = str(api_keys.get(name) or api_keys.get(f"{name}_api_key") or "").strip()
    return str(metadata.get(f"{name}_api_key") or nested or os.getenv(env_name) or "").strip()


def _clamp_int(value: Any, low: int, high: int) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = low
    return max(low, min(number, high))


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _error(code: str, message: str, status: str, retryable: bool, generated_at: str) -> Dict[str, Any]:
    return {
        "schema_version": "1.0",
        "status": status,
        "skill": SKILL_NAME,
        "generated_at": generated_at,
        "error": {"code": code, "message": message, "retryable": retryable},
        "errors": [{"code": code, "message": message}],
    }

