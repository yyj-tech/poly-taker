"""Command-line demo for the poly-taker engine.

Runs a self-contained taker simulation against a seeded in-memory order book so the
project can be exercised end-to-end without live Polymarket credentials.
"""

from __future__ import annotations

import argparse

from poly_taker.orderbook import OrderBook
from poly_taker.taker import MarketOrder, OrderType, Side, Taker, TakeResult


def _seed_book(token_id: str) -> OrderBook:
    """Create a representative book for a ~40c outcome token."""
    book = OrderBook(token_id=token_id)
    for price, size in [(0.41, 200), (0.42, 350), (0.44, 500), (0.47, 1000)]:
        book.add_ask(price, size)
    for price, size in [(0.39, 250), (0.37, 400), (0.34, 800)]:
        book.add_bid(price, size)
    return book


def _format_result(result: TakeResult) -> str:
    lines = [
        f"status         : {result.status}",
        f"filled shares  : {result.filled_shares:.4f}",
        f"usdc exchanged : {result.spent:.4f}",
        f"average price  : {result.average_price:.4f}",
    ]
    if result.fills:
        lines.append("fills:")
        for fill in result.fills:
            lines.append(f"  {fill.shares:8.2f} shares @ {fill.price:.2f}  (${fill.cost:.2f})")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="poly-taker",
        description="Simulate taking liquidity against an in-memory Polymarket-style book.",
    )
    parser.add_argument("--token-id", default="demo-token", help="Market outcome token id.")
    parser.add_argument(
        "--side",
        choices=[s.value for s in Side],
        default=Side.BUY.value,
        help="BUY spends USDC by lifting asks; SELL sells shares into bids.",
    )
    parser.add_argument(
        "--amount",
        type=float,
        default=100.0,
        help="USDC to spend (BUY) or shares to sell (SELL).",
    )
    parser.add_argument(
        "--order-type",
        choices=[o.value for o in OrderType],
        default=OrderType.FAK.value,
        help="FOK must fill completely; FAK fills what it can.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    book = _seed_book(args.token_id)
    taker = Taker(book)

    order = MarketOrder(
        token_id=args.token_id,
        amount=args.amount,
        side=Side(args.side),
        order_type=OrderType(args.order_type),
    )

    print(f"Order book for {args.token_id!r}:")
    print(f"  best ask: {book.best_ask()}   (ask liquidity {book.ask_liquidity():.0f} shares)")
    print(f"  best bid: {book.best_bid()}   (bid liquidity {book.bid_liquidity():.0f} shares)")
    print()
    print(f"Submitting {order.order_type.value} {order.side.value} amount={order.amount} ...")
    print()

    result = taker.execute(order)
    print(_format_result(result))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
