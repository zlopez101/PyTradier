from PyTradier.base import BasePyTradier
from typing import Union
from datetime import datetime
from PyTradier.exceptions import RequiredError
from PyTradier.order import LimitOrder, StopLimitOrder, StopOrder, MarketOrder


anyOrder = Union[MarketOrder, LimitOrder, StopOrder, StopLimitOrder]
limitOrder_stopOrder_stopLimitOrder = Union[LimitOrder, StopOrder, StopLimitOrder]


class REST(BasePyTradier):
    """Place equity and complex option trades including advanced orders. kwarg arguments passed to class initialization will define default values including preview, tag, and durations settings
    """

    def __init__(
        self, token: str = "TRADIER_SANDBOX_TOKEN", paper: bool = True, **kwargs
    ):
        super().__init__(token=token, paper=paper)
        for key, value in kwargs.items():
            setattr(self, key, value)

    def place_order(self, params) -> dict:
        """base order method for all trades

        :return: API response
        :rtype: dict
        """
        params = self.prepare_order(params)
        if params["preview"]:
            print("here")
            return self._post(f"/v1/accounts/{self.account_id}/orders", params=params)
        else:
            print("there")
            self._check_parameters(params)
            return self._post(f"/v1/accounts/{self.account_id}/orders", params=params)

    def trade(self, order: anyOrder) -> dict:
        """Place an order to trade an equity or option security.

        :param order: Market, Limit, Stop, or Stop-Limit order
        :type order: Any_Order_Type
        :return: Order Response dict
        :rtype: dict
        """
        return self.place_order(order.params())

    def one_trigger_other(self, index_order: limitOrder_stopOrder_stopLimitOrder, triggered_order: anyOrder):
        """Place a one-triggers-other order. This order type is composed of two separate orders sent simultaneously. The property keys of each order are indexed.
        """
        pass

    def one_cancels_other(self, order1: limitOrder_stopOrder_stopLimitOrder, order2: anyOrder):
        """Place a one-cancels-other order. This order type is composed of two separate orders sent simultaneously. The property keys of each order are indexed.

        type must be different for both legs.
        If both orders are equities, the symbol must be the same.
        If both orders are options, the option_symbol must be the same.
        If sending duration per leg, both orders must have the same duration.
        """
        pass

    def one_triggers_one_cancels_other(
        self, index_order: limitOrder_stopOrder_stopLimitOrder, triggered_order: limitOrder_stopOrder_stopLimitOrder, cancelled_order: limitOrder_stopOrder_stopLimitOrder
    ):
        """Place a one-triggers-one-cancels-other order. This order type is composed of three separate orders sent simultaneously. The property keys of each order are indexed.

        If all equity orders, second and third orders must have the same symbol.
        If all option orders, second and third orders must have the same option_symbol.
        Second and third orders must always have a different type.
        If sending duration per leg, second and third orders must have the same duration.
        """
        pass

    def combo_order(self, equity_order, *args):
        """Place a combo order. This is a specialized type of order consisting of one equity leg and one option leg. It can optionally include a second option leg, for some strategies.
        """
        pass

    def multileg_order(self, *args):
        """Place a multileg order with up to 4 legs. This order type allows for simple and complex option strategies.      
        """
        pass

if __name__ == "__main__":
    from utils import printer

    rest = REST()
    # rest.one_cancels_other("asdf")
    response = rest.trade(MarketOrder('equity', 'SPY', )
