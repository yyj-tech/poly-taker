"""poly-taker: a liquidity-taking (market order) engine modeled on the Polymarket CLOB.

The package is intentionally self-contained: it simulates taking liquidity against an
in-memory order book so it can run and be tested without live credentials, funds, or
network access. The order/side/fill vocabulary mirrors the Polymarket CLOB v2 client
(``MarketOrderArgs``, ``Side``, ``OrderType.FOK``/``FAK``) so it maps cleanly onto a
real integration later.
"""

from poly_taker.orderbook import OrderBook, PriceLevel
from poly_taker.taker import (
    Fill,
    MarketOrder,
    OrderType,
    Side,
    Taker,
    TakeResult,
)

__all__ = [
    "OrderBook",
    "PriceLevel",
    "Fill",
    "MarketOrder",
    "OrderType",
    "Side",
    "Taker",
    "TakeResult",
]

__version__ = "0.1.0"
