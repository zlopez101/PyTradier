from PyTradier.base import BasePyTradier
from typing import Union
from itertools import groupby
from datetime import datetime
from PyTradier.exceptions import RequiredError
from PyTradier.order import (
    LimitOrder,
    StopLimitOrder,
    StopOrder,
    MarketOrder,
    SpecOrder,
)


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

    def check_types(self, attr: str, *args, shouldBeDifferent: bool = False) -> str:
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
                if shouldBeDifferent:
                    # this field is required to be different so everything is ok
                    pass
                else:
                    raise RequiredError(
                        f"All the attributes {attr} need to be the same for this type of order."
                    )
        elif getattr(self, attr, None):
            return getattr(self, attr, None)
        else:
            raise RequiredError(f"attribute {attr} was never specified")

    def all_equity(self, *args) -> bool:
        """Returns True if all the orders are Equity orders (no order in args has value in key: "option_symbol")

        :return: True or False
        :rtype: bool
        """
        return not (all([getattr(order, "option_symbol") for order in args]))

    def all_option(self, *args) -> bool:
        """Returns True if all the orders are Option orders (all orders provided have value in key: "option_symbol")

        :return: True or False
        :rtype: bool
        """
        return all([getattr(order, "option_symbol") for order in args])

    def create_order_legs(self, *args, exclude="") -> dict:
        """create the order legs

        :return: combined dict from each order's make_legs() method
        :rtype: dict
        """
        legs = {}
        for i, order in enumerate(args):
            dct = order.make_legs(i, exclude=exclude)
            legs = {**legs, **dct}
        return legs

    def place_order(self, params: dict) -> dict:
        """base order method for all trades

        :param params: parameters determining the class, types, sides, symbols etc of the other
        :type params: dict
        :return: API response
        :rtype: dict
        """
        return self._post(
            f"/v1/accounts/{self.account_id}/orders",
            params=params,
            dict_args=("order",),
        )

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

        # types must be different for both legs
        self.check_types("type", order1, order2, shouldBeDifferent=True)

        # equity symbol check
        if self.all_equity(order1, order2):
            self.check_types("symbol", order1, order2)

        # option symbol check
        if self.all_option(order1, order2):
            self.check_types("option_symbol", order1, order2)

        # duration check
        params["duration"] = self.check_types("duration", order1, order2)

        return self.place_order(params)

    def one_triggers_one_cancels_other(
        self,
        index_order: limitOrder_stopOrder_stopLimitOrder,
        triggered_order: limitOrder_stopOrder_stopLimitOrder,
        cancelled_order: limitOrder_stopOrder_stopLimitOrder,
    ):
        """Place a one-triggers-one-cancels-other order. This order type is composed of three separate orders sent simultaneously. The property keys of each order are indexed. Duration must be specifed on at least one order

        If all equity orders, second and third orders must have the same symbol.
        If all option orders, second and third orders must have the same option_symbol.
        Second and third orders must always have a different type.
        If sending duration per leg, second and third orders must have the same duration.
        """
        params = self.create_order_legs(index_order, triggered_order, cancelled_order)
        params["class"] = "otoco"

        # type check on second/third order
        self.check_types(
            "type", triggered_order, cancelled_order, shouldBeDifferent=True
        )

        # equity symbol check if all equity
        if self.all_equity(index_order, triggered_order, cancelled_order):
            self.check_types("symbol", index_order, triggered_order, cancelled_order)

        # option symbol check
        if self.all_option(index_order, triggered_order, cancelled_order):
            self.check_types(
                "option_symbol", index_order, triggered_order, cancelled_order
            )

        # duration check
        params["duration"] = self.check_types(
            "duration", triggered_order, cancelled_order
        )

        return self.place_order(params)

    def combo_order(self, *orders, **kwargs):
        """Place a combo order. This is a specialized type of order consisting of one equity leg and one option leg. It can optionally include a second option leg, for some strategies. Pass the type, duration, and price as keywords

        :param orders: Orders to be placed
        :type orders: limitOrder_stopOrder_stopLimitOrder
        :param type: The type of order, one of ['market', 'debit', 'credit', 'even']
        :type type: str
        :param duration: duration of order, one of ['day', 'gtc', 'pre', 'post']
        :type duration: str
        :param price: the limit price of the order, required for 'debit' and 'credit' orders
        :type price: float
        :return: API order response
        :rtype: dict
        """
        params = self.create_order_legs(*orders, exclude="symbol")

        params["symbol"] = self.check_types("symbol", *orders)
        # need to remove the symbol[0], symbol[1], type[0], type[1], price[]
        params["class"] = "combo"
        params = {**params, **kwargs}

        return self.place_order(params)

    def multileg_order(self, *orders, **kwargs):
        """Place a multileg order with up to 4 legs. This order type allows for simple and complex option strategies.
        """
        params = self.create_order_legs(*orders, exclude="symbol")
        params["symbol"] = self.check_types("symbol", *orders)
        params["class"] = "multileg"
        params = {**params, **kwargs}
        return self.place_order(params)


if __name__ == "__main__":
    from utils import printer

    rest = REST()
    print(
        rest.combo_order(
            SpecOrder("AAPL", 1, "buy"),
            SpecOrder("AAPL201220C00400", 1, "buy_to_open"),
            type="market",
            duration="gtc",
        )
    )

