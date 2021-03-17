"""
This module is trying to anticipate the more complex orders that will be placed in the future.
Any algorithmic trading that occurs with this platform won't have time to preview each trade.
The program ought to evaluate its own trades


"""


from typing import Union
from PyTradier.exceptions import RequiredError


class baseOrder:

    accepted_durations = ["day", "gtc", "pre", "post"]

    def __init__(
        self,
        symbol: str,
        quantity: int,
        duration: str,
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        if duration not in baseOrder.accepted_durations:
            raise RequiredError(
                f'duration "{duration}" not one of {baseOrder.accepted_durations}'
            )
        self.symbol = symbol
        self.quantity = quantity
        self.duration = duration
        self.preview = preview
        self.tag = tag

    def __repr__(self):
        return f"Order(Symbol: {self.symbol})"

    def params(self):
        params = {}
        for key, value in {
            key: value for key, value in self.__dict__.items() if value
        }.items():
            if key.startswith("_"):
                params[key[1:]] = value
            else:
                params[key] = value
        return params

    def make_legs(self, index: str) -> dict:
        return {
            f"option_symbol[{index}]": "option_symbol",
            f"side[{index}]": "side",
            f"quantity[{index}]": "quantity",
        }


class MarketOrder(baseOrder):
    pass


class Stop:
    """requires stop price

    Stop, Stop Limit, 
    """

    def __init__(self, stop_price):
        self.stop_price = stop_price


class StopLimit:
    """requires stop and limit price
    """

    def __init__(self, stop_price, limit_price):
        self.stop_price = stop_price
        self.limit_price = limit_price


class Limit:
    """requires limit price

    Limit, Stop Limit, Debit, Credit
    """

    def __init__(self, limit_price):
        self.limit_price = limit_price


class LimitOrder(baseOrder, Limit):
    _type = "limit"

    def __init__(
        self,
        _class: str,
        symbol: str,
        quantity: int,
        limit_price: float,
        duration: str,
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        baseOrder.__init__(self, symbol, quantity, duration, preview=preview, tag=tag)
        Limit.__init__(self, limit_price)
        self._class = _class
        self._type = "limit"


class StopOrder(baseOrder, Stop):
    def __init__(
        self,
        _class: str,
        symbol: str,
        quantity: int,
        stop_price: float,
        duration: str,
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        self._class = _class
        self.type = "stop"
        baseOrder.__init__(self, symbol, quantity, duration, preview=preview, tag=tag)
        Stop.__init__(self, stop_price)


class StopLimitOrder(baseOrder, StopLimit):
    _type = "stop_limit"

    def __init__(
        self,
        _class: str,
        symbol: str,
        quantity: int,
        limit_price: float,
        stop_price: float,
        duration: str,
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        self._class = _class
        self.type = "stop_limit"
        baseOrder.__init__(self, symbol, quantity, duration, preview=preview, tag=tag)
        StopLimit.__init__(self, stop_price, limit_price)


if __name__ == "__main__":

    l = LimitOrder("equitys", "hello", 1, 2, "sdfs")
    print(l.params())
