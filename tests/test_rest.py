import pytest
from PyTradier.rest import REST
from PyTradier.exceptions import *
from PyTradier.order import *


class TestRest:
    """All tests accept the post_return_parameters fixture to replace requests.post with a mocked response that just returns the submitted parameters
    """

    rest = REST()
    # create a rest with various defaults
    defaulted_rest = REST(duration="gtc", preview=True,)

    def test_all_equity(self, randomTicker, randomOption):
        """Test the utility function all_equity
        """
        order = LimitOrder(randomTicker[0], "buy", 1, 10)
        assert order.option_symbol == None
        res = self.rest.all_equity(
            LimitOrder(randomTicker[0], "buy", 1, 10),
            LimitOrder(randomTicker[0], "buy", 1, 10),
            LimitOrder(randomTicker[0], "buy", 1, 10),
        )
        assert res == True, "all the orders are equity"

        res = self.rest.all_option(
            LimitOrder(randomOption[0], "buy_to_close", 1, 10),
            LimitOrder(randomOption[0], "buy_to_close", 1, 10),
            LimitOrder(randomOption[0], "buy_to_close", 1, 10),
        )
        assert res == True, "all these orders are option"

    def test_equity_order(self, randomTicker, randomOption, post_return_parameters):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """
        # equity
        equity = self.rest.equity(LimitOrder(randomTicker[0], "buy", 1, 10.0, "gtc"))
        assert equity.get("symbol") == randomTicker[0]
        assert not equity.get("option_symbol"), "no option symbol"
        assert equity.get("class") == "equity"

        # option
        option = self.rest.option(
            StopOrder(randomOption[1], "sell_to_open", 1, 1000.00, "gtc")
        )
        assert (
            option.get("symbol") == randomTicker[1]
        ), "the underlying symbol should match"
        assert option.get("option_symbol") == randomOption[1]

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_one_cancels_other(
        self, randomTicker, randomOption, post_return_parameters
    ):
        """
        GIVEN a rest client with no defaults 
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """
        oco = self.rest.one_cancels_other(
            LimitOrder(randomOption[0], "buy_to_open", 1, 10.0),
            MarketOrder(randomOption[0], "buy_to_open", 1, duration="day"),
        )
        assert oco.get("symbol[0]") == oco.get("symbol[1]")
        assert oco.get("option_symbol[0]") == oco.get("option_symbol[1]")
        assert oco.get("duration") == "day"
        assert oco.get("class") == "oco"

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        # check not the same type error

        # not the the same symbol error
        with pytest.raises(RequiredError) as excInfo:
            oco = self.rest.one_cancels_other(
                LimitOrder(randomTicker[0], "buy", 1, 10.0),
                MarketOrder(randomTicker[1], "buy", 1, duration="day"),
            )
        assert "attributes symbol need to be the same" in str(excInfo.value)

        # not the same option symbol
        with pytest.raises(RequiredError) as excInfo:
            oco = self.rest.one_cancels_other(
                LimitOrder(randomOption[0], "buy_to_open", 1, 10.0),
                MarketOrder(randomOption[1], "buy_to_open", 1, duration="day"),
            )
        assert "attributes option_symbol need to be the same" in str(excInfo.value)

        # not the same duration error
        with pytest.raises(RequiredError) as excInfo:
            oco = self.rest.one_cancels_other(
                LimitOrder(randomTicker[0], "buy", 1, 10.0, duration="gtc"),
                MarketOrder(randomTicker[1], "buy", 1, duration="day"),
            )
        assert "attributes duration need to be the same" in str(excInfo.value)

        # no duration specified
        with pytest.raises(RequiredError) as excInfo:
            oco = self.rest.one_cancels_other(
                LimitOrder(randomTicker[0], "buy", 1, 10.0),
                MarketOrder(randomTicker[1], "buy", 1),
            )
        assert "attribute duration was never specified" in str(excInfo.value)

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """

    def test_one_triggers_other(
        self, randomTicker, randomOption, post_return_parameters
    ):
        # this one, the API documentation doesn't include any
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """
        oto = self.rest.one_trigger_other(
            LimitOrder(randomTicker[0], "sell", 100, 100.00, duration="day"),
            StopOrder(randomTicker[1], "buy", 100, 100.00),
        )
        assert oto.get("class") == "oto"
        assert oto.get("quantity[1]") == 100
        assert oto.get("duration") == "day"
        assert not oto.get("duration[0]"), "there should be no indexed duration"
        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_one_cancels_other_triggers_other(
        self, randomTicker, randomOption, post_return_parameters
    ):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """
        otoco = self.rest.one_triggers_one_cancels_other(
            LimitOrder(randomTicker[0], "buy", 1, 10.0),
            StopOrder(randomTicker[0], "sell", 1, 10),
            LimitOrder(randomTicker[0], "sell_short", 1, 10, duration="day"),
        )
        assert otoco.get("symbol[0]") == otoco.get("symbol[2]")
        assert otoco.get("symbol[1]") == randomTicker[0]
        assert otoco.get("type[0]") == "limit"
        assert otoco.get("stop[1]") == 10
        assert otoco.get("side[2]") == "sell_short"

        otoco = self.rest.one_triggers_one_cancels_other(
            LimitOrder(randomOption[1], "buy_to_open", 1, 10.0),
            StopOrder(randomOption[1], "sell_to_close", 1, 10),
            LimitOrder(randomOption[1], "sell_to_open", 1, 10, duration="day"),
        )
        assert otoco.get("symbol[0]") == otoco.get("symbol[2]")
        assert otoco.get("option_symbol[1]") == randomOption[1]
        assert otoco.get("symbol[0]") == randomTicker[1]
        assert otoco.get("type[0]") == "limit"
        assert otoco.get("stop[1]") == 10
        assert otoco.get("side[2]") == "sell_to_open"

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """
        # different option symbols in the second/third leg
        with pytest.raises(RequiredError) as excInfo:
            otoco = self.rest.one_triggers_one_cancels_other(
                LimitOrder(randomOption[1], "buy_to_open", 1, 10.0),
                StopOrder(randomOption[0], "sell_to_close", 1, 10),
                LimitOrder(randomOption[1], "sell_to_open", 1, 10, duration="day"),
            )
        assert "attributes option_symbol" in str(excInfo.value)

        # different equity symbols in the second/third leg
        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_combo_order(self, randomTicker, randomOption, post_return_parameters):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass

    def test_multileg_order(self, randomTicker, randomOption, post_return_parameters):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """

        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created and sent to trade endpoint        
        """

        """
        GIVEN a rest client with some default settings
        WHEN the user submits an improperly formatted request
        THEN a useful error should be raised altering user of the issue 
        """
        pass
