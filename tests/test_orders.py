import pytest
from PyTradier.order import *
from PyTradier.exceptions import *


def test_successful_orders(randomTicker, randomOption):
    """
    GIVEN properly formatted orders of all types
    THEN appropriate initialization and associated methods (params, make_legs)
    """

    equity = StopLimitOrder(randomTicker[0], "buy", 10, 10.5, 9, "gtc")
    equity_details = equity.params()
    assert not (equity_details.get("option_symbol")), "No option symbol"
    assert not (equity_details.get("preview")), "No preview"
    assert not (equity_details.get("tag")), "no tag"

    option = LimitOrder(randomOption[0], "sell_to_open", 1, 10.0, "gtc")
    option_details = option.params()
    assert option_details.get("option_symbol") == randomOption[0]
    assert option_details.get("symbol"), "symbol should be the underlying option"

    """
    make_legs() method. Takes in an index -> will be used in for loops of *args in complex order types
    """
    makeLegs = StopOrder(randomTicker[1], "buy", 10, 100.00, "gtc")
    leg_0 = makeLegs.make_legs(0)
    assert leg_0.get("type[0]") == "stop", "type should be stop order"
    assert leg_0.get("side[0]")


def test_failure_orders(randomTicker, randomOption):
    """
    GIVEN improperly formatted orders
    THEN error messages regarding the problem and potential solutions should be raised
    """
    with pytest.raises(RequiredError) as excInfo:
        
        # bad duration
        MarketOrder('equit)

