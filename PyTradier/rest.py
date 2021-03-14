from PyTradier.base import BasePyTradier
from typing import Union
from datetime import datetime
from PyTradier.exceptions import RequiredError


class REST(BasePyTradier):
    """Place equity and complex option trades including advanced orders.
    """

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

    def _check_parameters(self, _class: str, **kwargs) -> None:
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

    def prepare_order(self, params: dict) -> dict:
        """Because the API requires the use of reserved python keywords, need to handle before API calls

        :param params: parameters created by `self.create_params`
        :type params: dict
        :return: corrected parameters
        :rtype: dict
        """
        params["class"] = params.pop("_class")
        params["type"] = params.pop("_type")
        return params

    def place_equity_order(
        self,
        symbol: str,
        side: str,
        quantity: Union[str, int],
        _type: str,
        duration: str,
        price: Union[int, float, str] = "",
        stop: Union[int, float, str] = "",
        preview: str = "true",
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
        params = self.create_params(locals())
        params = self.prepare_order(params)
        return self._post(f"/v1/accounts/{self.account_id}/orders", params=params)


if __name__ == "__main__":
    from utils import printer

    rest = REST()
    order = rest.place_equity_order("AAPL", "buy", 1, "buy", "gtc")
    printer(order)
