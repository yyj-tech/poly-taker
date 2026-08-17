"""A minimal in-memory order book for a single market outcome (token).

Prices are probabilities in the ``(0, 1)`` range, matching how Polymarket quotes
outcome tokens. Sizes are expressed in shares.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PriceLevel:
    """A single resting level in the book: ``size`` shares available at ``price``."""

    price: float
    size: float

    def __post_init__(self) -> None:
        if not 0.0 < self.price < 1.0:
            raise ValueError(f"price must be within (0, 1), got {self.price}")
        if self.size <= 0.0:
            raise ValueError(f"size must be positive, got {self.size}")


@dataclass
class OrderBook:
    """Resting bids and asks for one token.

    ``asks`` are levels a taker buys from (best = lowest price); ``bids`` are levels a
    taker sells into (best = highest price). Levels are kept sorted so the best price is
    always first.
    """

    token_id: str
    bids: list[PriceLevel] = field(default_factory=list)
    asks: list[PriceLevel] = field(default_factory=list)

    def add_ask(self, price: float, size: float) -> None:
        """Add resting sell liquidity (a taker BUY consumes this)."""
        self.asks.append(PriceLevel(price, size))
        self.asks.sort(key=lambda level: level.price)

    def add_bid(self, price: float, size: float) -> None:
        """Add resting buy liquidity (a taker SELL consumes this)."""
        self.bids.append(PriceLevel(price, size))
        self.bids.sort(key=lambda level: level.price, reverse=True)

    def best_ask(self) -> PriceLevel | None:
        return self.asks[0] if self.asks else None

    def best_bid(self) -> PriceLevel | None:
        return self.bids[0] if self.bids else None

    def ask_liquidity(self) -> float:
        """Total shares resting on the ask side."""
        return sum(level.size for level in self.asks)

    def bid_liquidity(self) -> float:
        """Total shares resting on the bid side."""
        return sum(level.size for level in self.bids)
