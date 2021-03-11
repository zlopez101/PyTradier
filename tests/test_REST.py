import pytest
import random
from src.error import OrderError
from src.response import OrderResponse


def test_invalid_orders(randomTicker, pytrader):
    """
    GIVEN faulty order placement
    WHEN 
    THEN an orderError should be raised detailing the issues
    """
    # invalid symbol
    with pytest.raises(OrderError):
        buyOrder = pytrader.Equity("randomTicker[0]", "buy", 1)

    # invalid side
    with pytest.raises(OrderError):
        buyOrder = pytrader.Equity(randomTicker[0], "aeaery", 1)

    # can't sell if no shares / can't cover if no sell short
    with pytest.raises(OrderError) as error:
        # pass
        buy_to_cover_Order = pytrader.Equity(randomTicker[0], "buy_to_cover", 1)
        print(buy_to_cover_Order)
        assert f"Unable to buy_to_cover 1 {randomTicker[0]}"

    # invalid quantity
    with pytest.raises(OrderError):
        pass

    # order quantity exceeds buying power
    with pytest.raises(OrderError):
        pass


def test_equity(randomTicker, pytrader):
    """
    GIVEN a random ticker 
    THEN execute a series of trades    
    """

    # buy first
    # buyOrder = pytrader.Equity(randomTicker[0], "buy_to_cover", 1)
    # print(buyOrder)

    # buyOrder = OrderResponse.from_order_conf(buyOrder)
    # print(buyOrder)
    # assert buyOrder.id
    # assert buyOrder.status
    # assert buyOrder.partner_id

    # # sell the same stock you bought
    # sellOrder = OrderResponse(pytrader.Equity(randomTicker[0], "sell", 1))

    # # sell short the same stock
    # shortSell = OrderResponse(pytrader.Equity(randomTicker[0], "sell_short", 1))

    # # buy to cover
    # buyCover = OrderResponse(pytrader.Equity(randomTicker[0], "buy_to_cover", 1))

    # show all orders
    pass


def test_options(randomTicker, pytrader):
    """
    GIVEN
    THEN
    WHEN
    """
    pass


def test_multileg(randomTicker, pytrader):
    """
    GIVEN
    THEN
    WHEN
    """
    pass


def test_combo(randomTicker, pytrader):
    """
    GIVEN
    THEN
    WHEN
    """
    pass


def test_oto(randomTicker, pytrader):
    """
    GIVEN
    THEN
    WHEN
    """
    pass


def test_oco(randomTicker, pytrader):
    """
    GIVEN
    THEN
    WHEN
    """
    pass


def test_otoco(randomTicker, pytrader):
    """
    GIVENAD
    THEN
    WHEN
    """
    pass
