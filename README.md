# poly-taker

A small, self-contained **liquidity-taking (market order) engine** modeled on the
[Polymarket CLOB](https://github.com/Polymarket/py-clob-client-v2).

It simulates *taking* liquidity by crossing the spread against an in-memory order book,
so it runs and is fully testable **without live credentials, funds, or network access**.
The vocabulary (`Side.BUY`/`Side.SELL`, `OrderType.FOK`/`FAK`, USDC-denominated market
buys) mirrors the Polymarket v2 client so the core logic maps cleanly onto a real
integration later.

## Requirements

- Python >= 3.10

## Setup

Ubuntu 24.04 marks the system Python as externally managed (PEP 668), so dependencies
install into a project-local virtual environment:

```bash
./.cursor/install.sh
source .venv/bin/activate
```

This installs the package in editable mode along with the dev tools (`pytest`, `ruff`).

## Run the demo

The CLI seeds a representative order book and executes a market order against it:

```bash
poly-taker --side BUY --amount 100 --order-type FAK
```

Options:

- `--side` — `BUY` spends a USDC `--amount` by lifting the best asks; `SELL` sells that
  many shares into the best bids.
- `--amount` — USDC to spend (BUY) or shares to sell (SELL).
- `--order-type` — `FOK` (fill-or-kill) must fill completely or is rejected; `FAK`
  (fill-and-kill) fills what it can and cancels the remainder.

## Library usage

```python
from poly_taker import MarketOrder, OrderBook, OrderType, Side, Taker

book = OrderBook(token_id="my-token")
book.add_ask(0.41, 200)
book.add_ask(0.44, 500)

result = Taker(book).execute(
    MarketOrder(token_id="my-token", amount=100.0, side=Side.BUY, order_type=OrderType.FAK)
)
print(result.status, result.filled_shares, result.average_price)
```

## Development

```bash
source .venv/bin/activate
pytest        # run the test suite
ruff check .  # lint
```
