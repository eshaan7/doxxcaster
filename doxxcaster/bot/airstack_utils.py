from typing import Any, Dict, List, Optional

from airstack.execute_query import AirstackClient

from doxxcaster.bot.models import ERC20Balance, Socials
from doxxcaster.bot.powerloom_utils import fetch_top_token_prices
from doxxcaster.bot.settings import AIRSTACK_API_KEY
from doxxcaster.bot.uniswap_default_tokens import UNISWAP_DEFAULT_TOKENS

__all__ = ["get_socials_of_fc_user", "get_erc20_token_balances_of_fc_user"]


def _filter_socials(data: Optional[Dict[str, Any]]) -> Socials:
    addresses, twitter_usernames, lens_names, fc_names, ens_names = (
        set(),
        set(),
        set(),
        set(),
        set(),
    )

    if isinstance(data, dict):
        socials = data.get("Socials", {}).get("Social", [])
        for social in socials:
            if social.get("userAddress"):
                addresses.add(social["userAddress"])
            if social.get("twitterUserName"):
                twitter_usernames.add(f"{social['twitterUserName']}.twitter")
            if social.get("dappName") == "lens" and social.get("profileName"):
                lens_names.add(social["profileName"].removeprefix("lens/@") + ".lens")
            elif social.get("dappName") == "farcaster" and social.get("fnames"):
                fc_names.update(f"@{fname}" for fname in social["fnames"])

        domains = data.get("Domains", {}).get("Domain", [])
        for domain in domains:
            if domain.get("dappName") == "ens" and domain.get("name"):
                ens_names.add(domain["name"])

    return Socials(
        addresses=list(addresses),
        ens_names=list(sorted(ens_names, key=lambda x: len(x.split(".")))),
        twitter_usernames=list(twitter_usernames),
        lens_names=list(lens_names),
        fc_names=list(fc_names),
    )


def _filter_spam_erc20_tokens(data: Optional[Dict[str, Any]]) -> List[ERC20Balance]:
    erc20_tokens = []

    if isinstance(data, dict):
        tokenprice_map = fetch_top_token_prices()
        eth_erc20_tokens = [
            {
                **erc20_token,
                **tokenprice_map.get(erc20_token["token"]["symbol"], {}),
                "blockchain": "ethereum",
            }
            for erc20_token in data.get("Ethereum", {}).get("TokenBalance", [])
            if erc20_token
            and "token" in erc20_token
            and not erc20_token["token"]["isSpam"]
            and erc20_token["token"]["symbol"] in UNISWAP_DEFAULT_TOKENS
        ]
        # sort heavy bags first 🤑
        erc20_tokens = sorted(
            eth_erc20_tokens,
            key=lambda x: x["formattedAmount"] * x.get("price", 1),
            reverse=True,
        )

    return [
        ERC20Balance(
            amount=erc20_token["formattedAmount"],
            amountStr=erc20_token["amount"],
            symbol=erc20_token["token"]["symbol"],
            blockchain=erc20_token["blockchain"],
            price=erc20_token.get("price"),
            priceChange24h=erc20_token.get("priceChange24h"),
        )
        for erc20_token in erc20_tokens
        if erc20_token
    ]


async def get_socials_of_fc_user(
    fc_name: str,
) -> Socials:
    query = """
query GetSocialsOfFcUser($fcName: Identity!) {
	Socials(input: {filter: {identity: {_in: [$fcName]}}, blockchain: ethereum}) {
		Social {
			dappName
			userAddress
			twitterUserName
			profileName
            fnames
		}
	}
	Domains(input: {filter: {owner: {_in: [$fcName]}}, blockchain: ethereum}) {
		Domain {
			dappName
			name
		}
	}
}
"""
    api_client = AirstackClient(api_key=AIRSTACK_API_KEY)
    execute_query_client = api_client.create_execute_query_object(
        query=query, variables={"fcName": f"fc_fname:{fc_name}"}
    )
    response = await execute_query_client.execute_query()

    return _filter_socials(response.data)


async def get_erc20_token_balances_of_fc_user(fc_name: str) -> List[ERC20Balance]:
    query = """
query GetERC20TokenBalancesForFcUser($fcName: Identity!) {
	Ethereum: TokenBalances(
		input: {filter: {owner: {_in: [$fcName]}, tokenType: {_eq: ERC20}}, blockchain: ethereum, limit: 100}
	) {
		TokenBalance {
			amount
			formattedAmount
			token {
				symbol
				isSpam
			}
		}
		pageInfo {
			nextCursor
			prevCursor
		}
	}
}
"""

    api_client = AirstackClient(api_key=AIRSTACK_API_KEY)
    execute_query_client = api_client.create_execute_query_object(
        query=query, variables={"fcName": f"fc_fname:{fc_name}"}
    )
    response = await execute_query_client.execute_paginated_query()

    return _filter_spam_erc20_tokens(response.data)
