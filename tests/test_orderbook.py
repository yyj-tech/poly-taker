import pytest

from poly_taker.orderbook import OrderBook, PriceLevel


def test_levels_stay_sorted_best_first():
    book = OrderBook(token_id="t")
    book.add_ask(0.44, 100)
    book.add_ask(0.41, 100)
    book.add_ask(0.47, 100)
    book.add_bid(0.34, 100)
    book.add_bid(0.39, 100)

    assert [level.price for level in book.asks] == [0.41, 0.44, 0.47]
    assert [level.price for level in book.bids] == [0.39, 0.34]
    assert book.best_ask() == PriceLevel(0.41, 100)
    assert book.best_bid() == PriceLevel(0.39, 100)


def test_liquidity_totals():
    book = OrderBook(token_id="t")
    book.add_ask(0.42, 350)
    book.add_ask(0.44, 500)
    book.add_bid(0.39, 250)

    assert book.ask_liquidity() == 850
    assert book.bid_liquidity() == 250


@pytest.mark.parametrize("price", [0.0, 1.0, -0.1, 1.5])
def test_price_out_of_range_rejected(price):
    with pytest.raises(ValueError):
        PriceLevel(price, 10)


def test_non_positive_size_rejected():
    with pytest.raises(ValueError):
        PriceLevel(0.5, 0)
