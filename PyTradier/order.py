"""
This module is trying to anticipate the more complex orders that will be placed in the future.
Any algorithmic trading that occurs with this platform won't have time to preview each trade.
The program ought to evaluate its own trades


"""


from typing import Union
from PyTradier.exceptions import RequiredError
import re


class baseOrder:

    accepted_durations = ["day", "gtc", "pre", "post"]
    option_sides = ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"]
    equity_sides = ["buy", "buy_to_cover", "sell", "sell_short"]

    def __init__(
        self,
        symbol: str,
        side,
        duration: str = "",
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        if duration and duration not in baseOrder.accepted_durations:
            raise RequiredError(
                f'duration "{duration}" not one of {baseOrder.accepted_durations}'
            )

        self.symbol_process(symbol)
        self.duration = duration
        if self.option_symbol:
            if side not in baseOrder.option_sides:
                raise RequiredError(
                    f"side {side} is not accepted side for option orders. Please choose from {baseOrder.option_sides}"
                )
        else:
            if side not in baseOrder.equity_sides:
                raise RequiredError(
                    f"side {side} is not accepted side for equity orders. Please choose from {baseOrder.equity_sides}"
                )
        self.side = side
        self.preview = preview
        self.tag = tag

    def symbol_process(self, symbol: str):
        if len(symbol) > 10:
            # we got an option
            self.option_symbol = symbol
            self.symbol = next(filter(None, re.split(r"(\d+)", symbol)))
        else:
            self.symbol = symbol
            self.option_symbol = None

    def __repr__(self):
        return f"order(Symbol: {self.symbol})"

    def params(self, _class: str) -> dict:
        """create the order parameter details in a form that Tradier API will understand

        :param _class: the class of the order. Ex equity 
        :type _class: str
        :return: order details dictionary dictionary
        :rtype: dict
        """
        details = {}
        for key, value in {
            key: value for key, value in self.__dict__.items() if value
        }.items():
            if key.startswith("_"):
                details[key[1:]] = value
            else:
                details[key] = value
        details["class"] = _class
        return details

    def make_legs(self, index: int) -> dict:
        """[summary]

        don't include duration, tags, preview, 

        :param index: index of the order dictionary
        :type index: int
        :return: dictionary reference for the order
        :rtype: dict
        """
        leg = {}
        for key, value in {
            key: value
            for key, value in self.__dict__.items()
            if value and key != "duration"
        }.items():
            if key.startswith("_"):
                leg[key[1:] + f"[{index}]"] = value
            else:
                leg[key + f"[{index}]"] = value
        return leg

        return {
            f"option_symbol[{index}]": "option_symbol",
            f"side[{index}]": "side",
            f"quantity[{index}]": "quantity",
        }


class SpecialOrder(baseOrder):
    """Special Orders for combo and multileg styles
    """

    pass


class LimitOrder(baseOrder):
    """A limit order is an order to buy or sell a stock at a specific price or better.
    """

    _type = "limit"

    def __init__(
        self,
        symbol: str,
        side: str,
        quantity: int,
        limit_price: float,
        duration: str = "",
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        super().__init__(symbol, side, duration=duration, preview=preview, tag=tag)
        self._type = "limit"
        self.limit_price = limit_price


class StopOrder(baseOrder):
    """A stop order, also referred to as a stop-loss order, is an order to buy or sell a stock once the price of the stock reaches a specified price, known as the stop price.
    """

    def __init__(
        self,
        symbol: str,
        side: str,
        quantity: int,
        stop_price: float,
        duration: str = "",
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        super().__init__(symbol, side, duration=duration, preview=preview, tag=tag)
        self.type = "stop"
        self.stop_price = stop_price


class StopLimitOrder(baseOrder):
    """A stop-limit order is an order to buy or sell a stock that combines the features of a stop order and a limit order
    """

    def __init__(
        self,
        symbol: str,
        side: str,
        quantity: int,
        stop_price: float,
        limit_price: float,
        duration: str = "",
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        super().__init__(symbol, side, duration=duration, preview=preview, tag=tag)

        self.type = "stop_limit"
        self.stop_price = stop_price
        self.limit_price = limit_price


class MarketOrder(baseOrder):
    def __init__(
        self,
        symbol: str,
        side: str,
        quantity: int,
        duration: str = "",
        preview: Union[str, bool] = "",
        tag: str = "",
    ):
        super().__init__(symbol, side, duration=duration, preview=preview, tag=tag)
        self.type = "market"


if __name__ == "__main__":
    order = LimitOrder("AAPL210605C000123000", "buy", 1, 2, "gtc")
    print(order.params())
