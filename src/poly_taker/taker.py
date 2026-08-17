"""The taking engine: cross the spread and consume resting liquidity.

The vocabulary mirrors the Polymarket CLOB v2 client:

* ``Side.BUY`` spends a USDC ``amount`` by lifting the best asks.
* ``Side.SELL`` sells a ``amount`` of shares into the best bids.
* ``OrderType.FOK`` (fill-or-kill) must fill completely or it is rejected.
* ``OrderType.FAK`` (fill-and-kill) fills what it can and cancels the remainder.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from poly_taker.orderbook import OrderBook, PriceLevel

# Rounding tolerance so float dust does not cause spurious partial fills.
_EPSILON = 1e-9


class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class OrderType(str, Enum):
    FOK = "FOK"  # fill-or-kill
    FAK = "FAK"  # fill-and-kill


@dataclass(frozen=True)
class MarketOrder:
    """A taker market order.

    For ``Side.BUY`` the ``amount`` is USDC to spend; for ``Side.SELL`` it is the number
    of shares to sell.
    """

    token_id: str
    amount: float
    side: Side
    order_type: OrderType = OrderType.FOK

    def __post_init__(self) -> None:
        if self.amount <= 0.0:
            raise ValueError(f"amount must be positive, got {self.amount}")


@dataclass(frozen=True)
class Fill:
    """A single execution against one price level."""

    price: float
    shares: float

    @property
    def cost(self) -> float:
        """USDC value of this fill."""
        return self.price * self.shares


@dataclass
class TakeResult:
    order: MarketOrder
    fills: list[Fill] = field(default_factory=list)
    status: str = "UNFILLED"

    @property
    def filled_shares(self) -> float:
        return sum(f.shares for f in self.fills)

    @property
    def spent(self) -> float:
        """Total USDC exchanged across all fills."""
        return sum(f.cost for f in self.fills)

    @property
    def average_price(self) -> float:
        shares = self.filled_shares
        return self.spent / shares if shares > 0 else 0.0


class Taker:
    """Executes market orders against an :class:`OrderBook`."""

    def __init__(self, book: OrderBook) -> None:
        self.book = book

    def execute(self, order: MarketOrder) -> TakeResult:
        if order.token_id != self.book.token_id:
            raise ValueError(
                f"order token {order.token_id!r} does not match book token "
                f"{self.book.token_id!r}"
            )

        levels = self.book.asks if order.side is Side.BUY else self.book.bids
        planned = self._plan_fills(order, levels)

        if order.order_type is OrderType.FOK and not self._fully_filled(order, planned):
            return TakeResult(order=order, fills=[], status="REJECTED")

        if not planned:
            return TakeResult(order=order, fills=[], status="REJECTED")

        self._consume(levels, planned)
        result = TakeResult(order=order, fills=planned)
        result.status = "FILLED" if self._fully_filled(order, planned) else "PARTIAL"
        return result

    def _plan_fills(self, order: MarketOrder, levels: list[PriceLevel]) -> list[Fill]:
        """Walk the book best-price-first without mutating it, returning planned fills."""
        remaining = order.amount
        fills: list[Fill] = []
        for level in levels:
            if remaining <= _EPSILON:
                break
            if order.side is Side.BUY:
                # ``remaining`` is USDC; buy as many shares as budget/price allows.
                affordable = remaining / level.price
                take = min(affordable, level.size)
                if take <= _EPSILON:
                    continue
                fills.append(Fill(price=level.price, shares=take))
                remaining -= take * level.price
            else:
                # ``remaining`` is shares to sell.
                take = min(remaining, level.size)
                fills.append(Fill(price=level.price, shares=take))
                remaining -= take
        return fills

    @staticmethod
    def _fully_filled(order: MarketOrder, fills: list[Fill]) -> bool:
        if order.side is Side.BUY:
            spent = sum(f.cost for f in fills)
            return spent >= order.amount - _EPSILON
        filled = sum(f.shares for f in fills)
        return filled >= order.amount - _EPSILON

    @staticmethod
    def _consume(levels: list[PriceLevel], fills: list[Fill]) -> None:
        """Deduct the planned fills from the resting levels in place."""
        by_price: dict[float, float] = {}
        for fill in fills:
            by_price[fill.price] = by_price.get(fill.price, 0.0) + fill.shares
        idx = 0
        while idx < len(levels):
            level = levels[idx]
            taken = by_price.get(level.price, 0.0)
            remaining_size = level.size - taken
            if remaining_size <= _EPSILON:
                levels.pop(idx)
                continue
            if taken > 0.0:
                levels[idx] = PriceLevel(price=level.price, size=remaining_size)
            idx += 1
