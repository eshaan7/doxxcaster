import requests

from doxxcaster.bot.logger import LOGGER

__all__ = ["fetch_top_token_prices"]


def fetch_top_token_prices() -> dict[str, dict[str, float]]:
    """
    Fetch top tokens from Powerloom's Uniswap V2 snapshotter API.
    """
    base_url = "https://uniswapv2.powerloom.io"
    resource_id = "aggregate_24h_top_tokens_lite:10ecae2f52160690abffff26efeb45568e5d67ea0bc7d4485d9ffb10ef437f33:UNISWAPV2"
    try:
        resp = requests.get(f"{base_url}/api/last_finalized_epoch/{resource_id}")
        resp.raise_for_status()
        epoch_id = resp.json()["epochId"]

        resp2 = requests.get(f"{base_url}/api/data/{epoch_id}/{resource_id}/")
        resp2.raise_for_status()
        tokens = resp2.json()["tokens"]

        return {
            token["symbol"]: {
                "price": token["price"],
                "priceChange24h": token["priceChange24h"],
            }
            for token in tokens
        }
    except Exception as exc:
        LOGGER.exception("[fetch_top_token_prices] Failed sending message: %s", exc)
        return {}
