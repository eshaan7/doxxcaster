from dataclasses import dataclass
from typing import List, Optional

__all__ = ["Socials", "ERC20Balance"]


@dataclass
class Socials:
    addresses: List[str]
    ens_names: List[str]
    twitter_usernames: List[str]
    lens_names: List[str]
    fc_names: List[str]


@dataclass
class ERC20Balance:
    amount: float
    amountStr: str
    symbol: str
    blockchain: Optional[str] = None
    price: Optional[float] = None
    priceChange24h: Optional[float] = None
