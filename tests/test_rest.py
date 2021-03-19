import pytest
from PyTradier.rest import REST
from PyTradier.exceptions import *
from PyTradier.order import *


class TestRest:

    rest = REST()
    # create a rest with various defaults
    defaulted_rest = REST(duration="gtc", preview=True,)

    def test_equity_order(self, randomTicker, randomOption, post_return_parameters):
        """
        GIVEN a rest client with no defaults
        WHEN the user submits a properly formatted request
        THEN the correct order_details dictionary should be created
        """
        # equity
        equity = self.rest.equity(LimitOrder(randomTicker[0], "buy", 1, 10.0, "gtc"))
        assert equity.params.get("symbol") == randomTicker[0]
        assert not equity.params.get("option_symbol"), "no option symbol"
        assert equity.params.get("class") == "equity"

        # option
        option = self.rest.option(
            StopOrder(randomOption[1], "sell_to_open", 1, 1000.00, "gtc")
        )
        assert (
            option.params.get("symbol") == randomTicker[1]
        ), "the underlying symbol should match"
        assert option.params.get("option_symbol") == randomOption[1]

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
        assert oco.params.get("symbol[0]") == oco.params.get("symbol[1]")
        assert oco.params.get("option_symbol[0]") == oco.params.get("option_symbol[1]")
        assert oco.params.get("duration") == "day"
        assert oco.params.get("class") == "oco"
        """
        GIVEN a rest client with no defaults
        WHEN the user submits improperly formatted request
        THEN a useful error should be raised altering user of the issue
        """
        with pytest.raise(RequiredError) as excInfo:
            oco = self.rest.one_cancels_other(
                LimitOrder(randomOption[0], "buy_to_open", 1, 10.0),
                MarketOrder(randomOption[0], "buy_to_open", 1, duration="day"),
            )
            assert oco.params.get("symbol[0]") == oco.params.get("symbol[1]")
            assert oco.params.get("option_symbol[0]") == oco.params.get("option_symbol[1]")
            assert oco.params.get("duration") == "day"
            assert oco.params.get("class") == "oco"

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

    def test_one_cancels_other_triggers_other(
        self, randomTicker, randomOption, post_return_parameters
    ):
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
