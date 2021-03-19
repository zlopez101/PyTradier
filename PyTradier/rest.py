from PyTradier.base import BasePyTradier
from typing import Union
from itertools import groupby
from datetime import datetime
from PyTradier.exceptions import RequiredError
from PyTradier.order import LimitOrder, StopLimitOrder, StopOrder, MarketOrder


anyOrder = Union[MarketOrder, LimitOrder, StopOrder, StopLimitOrder]
limitOrder_stopOrder_stopLimitOrder = Union[LimitOrder, StopOrder, StopLimitOrder]


class REST(BasePyTradier):
    """Place equity and complex option trades including advanced orders. kwarg arguments passed to class initialization will define default values including preview, tag, and durations settings

    Order requirements are rather bespoke and I have no found a common pattern to unite them -> self validation is difficult, respond and adjust to error message where they arise
    """

    def __init__(
        self, token: str = "TRADIER_SANDBOX_TOKEN", paper: bool = True, **kwargs
    ):
        super().__init__(token=token, paper=paper)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def check_types(self, attr: str, *args) -> str:
        """confirm all durations are the same, or use default, or use one specified by specific order

        :return: duration of order
        :rtype: str
        """

        attributes = [
            getattr(order, attr) for order in args if getattr(order, attr, None)
        ]
        if attributes:
            grouped = groupby(attributes)
            if next(grouped, True) and not next(grouped, False):
                return attributes[0]
            else:
                raise RequiredError(
                    f"All the attributes {attr} need to be the same for this type"
                )
        elif getattr(self, attr, None):
            return getattr(self, attr, None)
        else:
            raise RequiredError(f"attribute {attr} was never specified")

    def order_details(self, *args, **kwargs) -> dict:
        """create the order details dictionary based on supplied orders (args) and specified keywords (duration, tags)

        :return: [description]
        :rtype: dict
        """
        pass

    def create_order_legs(self, *args) -> dict:
        """create the order legs

        :return: [description]
        :rtype: dict
        """
        legs = {}
        for i, order in enumerate(args):
            dct = order.make_legs(i)
            legs = {**legs, **dct}
        return legs

    def place_order(self, params: dict) -> dict:
        """base order method for all trades

        :param params: parameters determining the class, types, sides, symbols etc of the other
        :type params: dict
        :return: API response
        :rtype: dict
        """
        return self._post(f"/v1/accounts/{self.account_id}/orders", params=params)

    def equity(self, order: anyOrder) -> dict:
        """Place an order to trade an equity security.

        :param order: Order to place
        :type order: MarketOrder, LimitOrder, StopOrder, StopLimitOrder
        :return: Order Response dict
        :rtype: dict
        """
        params = order.params("equity")
        params["duration"] = self.check_types("duration", order)
        return self.place_order(params)

    def option(self, order: anyOrder) -> dict:
        """Place an order to trade an option security

        :param order: Order to place
        :type order: MarketOrder, LimitOrder, StopOrder, StopLimitOrder
        :return: order response dict
        :rtype: dict
        """
        params = order.params("option")
        params["duration"] = self.check_types("duration", order)

        return self.place_order(params)

    def one_trigger_other(
        self,
        index_order: limitOrder_stopOrder_stopLimitOrder,
        triggered_order: anyOrder,
    ):
        """Place a one-triggers-other order. This order type is composed of two separate orders sent simultaneously. The property keys of each order are indexed.
        """
        params = self.create_order_legs(index_order, triggered_order)
        params["duration"] = self.check_types("duration", index_order, triggered_order)
        params["class"] = "oto"
        return self.place_order(params)

    def one_cancels_other(
        self,
        order1: limitOrder_stopOrder_stopLimitOrder,
        order2: limitOrder_stopOrder_stopLimitOrder,
        **kwargs,
    ):
        """Place a one-cancels-other order. This order type is composed of two separate orders sent simultaneously. The property keys of each order are indexed.

        type must be different for both legs.
        If both orders are equities, the symbol must be the same.
        If both orders are options, the option_symbol must be the same.
        If sending duration per leg, both orders must have the same duration.
        """
        params = self.create_order_legs(order1, order2)
        params["class"] = "oco"
        # duration check
        params["duration"] = self.check_types("duration", order1, order2)

        # equity symbol check
        # check if they are both equity orders (no option_symbol attr) then run check_types
        if not hasattr(order1, "option_symbol") and not hasattr(
            order2, "option_symbol"
        ):
            self.check_types("symbol", order1, order2)

        # option symbol check
        # some code
        if hasattr(order1, "option_symbol") and hasattr(order2, "option_symbol"):
            self.check_types("option_symbol", order1, order2)

        return self.place_order(params)

    def one_triggers_one_cancels_other(
        self,
        index_order: limitOrder_stopOrder_stopLimitOrder,
        triggered_order: limitOrder_stopOrder_stopLimitOrder,
        cancelled_order: limitOrder_stopOrder_stopLimitOrder,
    ):
        """Place a one-triggers-one-cancels-other order. This order type is composed of three separate orders sent simultaneously. The property keys of each order are indexed. duration

        If all equity orders, second and third orders must have the same symbol.
        If all option orders, second and third orders must have the same option_symbol.
        Second and third orders must always have a different type.
        If sending duration per leg, second and third orders must have the same duration.
        """
        params = self.create_order_legs(index_order, triggered_order, cancelled_order)
        params["class"] = "otoco"
        # duration check
        params["duration"] = self.check_types(
            "duration", triggered_order, cancelled_order
        )

        # equity symbol check
        # some code

        # option symbol check
        # some code

        return self.place_order(params)

    def combo_order(self, equity_order, option_order, *order):
        """Place a combo order. This is a specialized type of order consisting of one equity leg and one option leg. It can optionally include a second option leg, for some strategies.
        """
        params = self.create_order_legs(equity_order, option_order)
        params["class"] = "combo"

        params["duration"] = self.check_types(equity_order, option_order)
        return self.place_order(params)

    def multileg_order(self, *orders):
        """Place a multileg order with up to 4 legs. This order type allows for simple and complex option strategies.      
        """
        params = self.create_order_legs(orders)
        params["class"] = "multileg"

        params["duration"] = self.check_types(orders)

        return self.place_order(params)


if __name__ == "__main__":
    from utils import printer

    rest = REST()
    response = rest.one_cancels_other(
        LimitOrder("AAPL", "buy", 1, 10, duration="gtc"),
        StopOrder("AAPL", "buy", 1, 12.0),
    )

    printer(response)
    # rest.one_cancels_other("asdf")
