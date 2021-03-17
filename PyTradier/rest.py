from PyTradier.base import BasePyTradier
from typing import Union
from datetime import datetime
from PyTradier.exceptions import RequiredError
from PyTradier.order import LimitOrder, StopLimitOrder, StopOrder, MarketOrder


class REST(BasePyTradier):
    """Place equity and complex option trades including advanced orders.


    Using the preview=True keyword for any order interaction will ensure that order request is properly formatted
    """

    def __init__(self, token: str="TRADIER_SANDBOX_TOKEN", paper: bool=True, default_duration: str: '', add_to_watchlist: bool=False):
        super().__init__(self, token=token, paper=paper)
        if default_duration:
            self.default_duration = default_duration
        if add_to_watchlist:
            self.add_to_watchlist = True

    equity = {
        "side": ["buy", "buy_to_cover", "sell", "sell_to_cover"],
        "_type": ["market", "limit", "stop", "stop_limit"],
        "duration": ["day", "gtc", "pre", "post"],
    }
    option = {
        "side": ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"],
        "_type": ["market", "limit", "stop", "stop_limit"],
        "duration": ["day", "gtc", "pre", "post"],
    }
    multileg = {
        "_type": ["market", "debit", "credit", "even"],
        "duration": ["day", "gtc", "pre", "post"],
        "side": ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"],
    }
    _type = ["market", "limit", "stop", "stop_limit"]
    duration = ["day", "gtc", "pre", "post"]

    def _check_parameters(self, _class: str, params: dict) -> None:
        """check the parameters supplied for any errors before sending a request

        :param _class: type of order, one of ['equity', 'option', 'multileg']
        :type _class: str
        :return: 
        :rtype: bool
        """
        correct_dict = getattr(self, _class)
        print(correct_dict)
        # for key, value in kwargs.items():
        #     if value not in correct_dict[key]:
        #         raise RequireError

    def create_limit_order(self):
        return LimitOrder()

    def create_stop_order(self):
        return StopOrder()

    def create_stop_limit_order(self):
        return StopLimitOrder()

    def prepare_order(self, params: dict) -> dict:
        """Because the API requires the use of reserved python keywords, need to handle before API calls

        :param params: parameters to supply
        :type params: dict
        :return: corrected parameters
        :rtype: dict
        """
        params = self.create_params(params)
        params["preview"] = self._bool_prep(params.pop("preview"))
        params["class"] = params.pop("_class")
        params["type"] = params.pop("_type")
        return params

    def order(self, *args):
        """
        """

    def _create_equity_order():
        pass

    def _create_option_order():
        pass

    def _create_order_legs():
        pass

    def trade_equity(
        self,
        symbol: str,
        side: str,
        quantity: Union[str, int],
        _type: str,
        duration: str,
        price: Union[int, float, str] = "",
        stop: Union[int, float, str] = "",
        preview: Union[str, bool] = "true",
        tag: str = "",
    ) -> dict:
        """Place an order to trade an equity security.

        :param symbol: Security symbol to be traded
        :type symbol: str
        :param side: the side of the order, One of ['buy', 'buy_to_cover', 'sell', 'sell_to_cover']
        :type side: str
        :param quantity: the number of shares ordered
        :type quantity: Union[str, int]
        :param _type: the type of order to be placed, One of ['market', 'limit', 'stop', 'stop_limit']
        :type _type: str
        :param duration: [description]
        :type duration: str
        :param price: [description], defaults to ""
        :type price: Union[int, float, str], optional
        :param stop: [description], defaults to ""
        :type stop: Union[int, float, str], optional
        :param tag: [description], defaults to ""
        :type tag: str, optional
        :return: [description]
        :rtype: dict
        """
        _class = "equity"
        params = self.prepare_order(params)
        if params["preview"]:
            return self._post(f"/v1/accounts/{self.account_id}/orders", params=params)

        # perform internal checks
        else:
            self._check_parameters(_class, params)
            return self._post(f"/v1/accounts/{self.account_id}/orders", params=params)

    def one_cancels_other(self, Order: LimitOrder):
        """
        type must be different for both legs.
        If both orders are equities, the symbol must be the same.
        If both orders are options, the option_symbol must be the same.
        If sending duration per leg, both orders must have the same duration.
        """

        print("hello")

    def one_triggers_one_cancels_other(self):
        """
        If all equity orders, second and third orders must have the same symbol.
        If all option orders, second and third orders must have the same option_symbol.
        Second and third orders must always have a different type.
        If sending duration per leg, second and third orders must have the same duration.
        """
        pass

    def combo_order(self):
        """Place a combo order. This is a specialized type of order consisting of one equity leg and one option leg. It can optionally include a second option leg, for some strategies.
        """
        pass

    def multileg_order(self):
        """Place a multileg order with up to 4 legs. This order type allows for simple and complex option strategies.      
        """
        pass

    def equity_order(self):
        """Place an order to trade an equity security.
        """
        pass

    def option_order(self):
        """Place an order to trade a single option.
        """
        pass


if __name__ == "__main__":
    from utils import printer

    rest = REST()
    rest.one_cancels_other()
