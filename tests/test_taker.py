import pytest

from poly_taker.orderbook import OrderBook
from poly_taker.taker import MarketOrder, OrderType, Side, Taker


def make_book() -> OrderBook:
    book = OrderBook(token_id="demo")
    book.add_ask(0.40, 100)
    book.add_ask(0.50, 100)
    book.add_bid(0.30, 100)
    book.add_bid(0.20, 100)
    return book


def test_buy_fills_from_cheapest_asks_first():
    book = make_book()
    taker = Taker(book)

    # $40 buys exactly 100 shares at 0.40.
    result = taker.execute(
        MarketOrder(token_id="demo", amount=40.0, side=Side.BUY, order_type=OrderType.FOK)
    )

    assert result.status == "FILLED"
    assert result.filled_shares == pytest.approx(100.0)
    assert result.average_price == pytest.approx(0.40)
    # Best ask level fully consumed.
    assert book.best_ask().price == pytest.approx(0.50)


def test_buy_walks_multiple_levels():
    book = make_book()
    taker = Taker(book)

    # $40 -> 100 shares @0.40; remaining $20 -> 40 shares @0.50.
    result = taker.execute(
        MarketOrder(token_id="demo", amount=60.0, side=Side.BUY, order_type=OrderType.FAK)
    )

    assert result.status == "FILLED"
    assert result.filled_shares == pytest.approx(140.0)
    assert result.spent == pytest.approx(60.0)
    assert book.best_ask().size == pytest.approx(60.0)  # 100 - 40 consumed


def test_fok_rejected_when_insufficient_liquidity():
    book = make_book()
    taker = Taker(book)

    # Total ask liquidity is worth $40 + $50 = $90; asking for $200 cannot fully fill.
    result = taker.execute(
        MarketOrder(token_id="demo", amount=200.0, side=Side.BUY, order_type=OrderType.FOK)
    )

    assert result.status == "REJECTED"
    assert result.fills == []
    # Book left untouched on rejection.
    assert book.ask_liquidity() == pytest.approx(200.0)


def test_fak_partial_fill_consumes_available_liquidity():
    book = make_book()
    taker = Taker(book)

    result = taker.execute(
        MarketOrder(token_id="demo", amount=200.0, side=Side.BUY, order_type=OrderType.FAK)
    )

    assert result.status == "PARTIAL"
    assert result.spent == pytest.approx(90.0)  # only $90 of liquidity available
    assert result.filled_shares == pytest.approx(200.0)
    assert book.ask_liquidity() == pytest.approx(0.0)


def test_sell_consumes_highest_bids_first():
    book = make_book()
    taker = Taker(book)

    result = taker.execute(
        MarketOrder(token_id="demo", amount=150.0, side=Side.SELL, order_type=OrderType.FAK)
    )

    assert result.status == "FILLED"
    assert result.filled_shares == pytest.approx(150.0)
    # 100 @0.30 + 50 @0.20 = 40 USDC.
    assert result.spent == pytest.approx(40.0)
    assert book.best_bid().price == pytest.approx(0.20)
    assert book.best_bid().size == pytest.approx(50.0)


def test_token_mismatch_raises():
    book = make_book()
    taker = Taker(book)
    with pytest.raises(ValueError):
        taker.execute(MarketOrder(token_id="other", amount=10.0, side=Side.BUY))


def test_negative_amount_rejected():
    with pytest.raises(ValueError):
        MarketOrder(token_id="demo", amount=-1.0, side=Side.BUY)
