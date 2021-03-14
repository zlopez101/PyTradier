import requests
import os
from datetime import datetime
import json
import PyTradier.error as e
from PyTradier.fundamental import FundamentalData
from PyTradier.account import Account
from PyTradier.response import OrderResponse
from PyTradier.base import BasePyTradier
from PyTradier.watchlist import WatchList


class PyTradier(BasePyTradier):
    """[summary]

    :param BasePyTradier: [description]
    :type BasePyTradier: [type]
    :raises Error: [description]
    :raises error: [description]
    :raises e.RequiredError: [description]
    :raises e.RequiredError: [description]
    :raises e.OrderError: [description]
    :raises e.OrderError: [description]
    :raises e.OrderError: [description]
    :raises e.OrderError: [description]
    :return: [description]
    :rtype: [type]
    """

    equitySide = ["buy", "buy_to_cover", "sell", "sell_short"]
    optionSide = ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"]
    complexTypes = ["market", "debit", "credit", "even"]
    equityTypes = ["market", "limit", "stop", "stop_limit"]
    duration = ["day", "gtc", "pre", "post"]
    comboleg = ["option_symbol", "side", "quantity"]
    classes = ["equity", "option", "multileg", "combo"]

    def __init__(self, paper=True):
        super().__init__(paper)
        self.account = Account(self.account_id, self.token, self.url)
        self.positions = self.account.positions
        self.fundamental = FundamentalData()
        self.watchlist = WatchList(self.account_id, self.token, self.url)
        self.orders = self.account.orders
        self.open_orders = []

    @staticmethod
    def _check(Error, *args) -> None:
        """
        Raises Error if arg[0] not in arg[1]
        """
        for pair in args:
            if pair[0] not in pair[1]:
                raise Error(f"{pair[0]} not in {pair[1]}")

    @staticmethod
    def _required(params) -> None:
        """
        TBD, would abstract any required logic for special orders and raise error if requirement not met
        """
        # limit prices
        if params["type"] == "limit" or params["type"] == "stop_limit":
            if not (params["price"]):
                raise e.RequiredError(
                    f"A price parameter is required with {params['type']} orders."
                )

        # stop prices
        if params["type"] == "limit" or params["type"] == "stop_limit":
            if not (params["stop"]):
                raise e.RequiredError(
                    f"A stop parameter is required with {params['type']} orders."
                )

    @staticmethod
    def make_params(namespace, *args):
        """
        simple dictionary creation
        """
        # copy the dictionary, possibly could change the local variables -> might have unintended consequences
        namespace = {k: str(v) for (k, v) in namespace.items() if v}
        # class is special, have to change manually
        namespace["class"] = namespace.pop("_class")

        # also remove unneccesary items
        namespace.pop("self")
        namespace.pop("args", None)

        # add in the arguments and index them accordingly
        if args:
            for i, dct in enumerate(args[0]):
                for key in dct.keys():
                    namespace[key + "[" + str(i) + "]"] = dct[key]

        return namespace

    def _valid_order(self, symbol, side, quantity, option=False):
        """
        Can the order be completed?
        """

        def get_position(symbol):
            """

            """
            return [dct for dct in self.positions if dct["symbol"] == "symbol"][0]

        def checkquantity(dct, quantity):
            """
            check the quantity
            """
            pos_amount = dct.get("quantity")

        def checkside(dct, quantity):
            """
            check the side
            """
            pass

        # options have different styles
        if option:
            # simple order?
            if side in ["buy_to_open", "sell_to_open"]:
                pass
            else:
                if symbol in [dct["symbol"] for dct in self.positions]:
                    pass
                else:
                    raise e.OrderError()

        # equities
        else:
            # simple order
            if side in ["buy", "sell_short"]:
                pass
            # complex order ('sell', 'buy_to_cover)
            else:
                # valid order
                if symbol in [dct["symbol"] for dct in self.positions]:
                    pass
                # invalid order
                else:
                    raise e.OrderError()

    def order(self, params):
        """
        Base method for placing orders
        """
        r = requests.post(
            self.url + f"accounts/{self.account_id}/orders",
            data=params,
            headers=self._headers(),
        )

        if r.status_code == 200:
            order = OrderResponse.from_order_conf(r.json())
            # if order is invalid
            if order.status == "rejected":
                raise e.OrderError(
                    f"Unable to {params['side']} {params['quantity']} {params['symbol']}"
                )

            return order
        else:
            raise e.OrderError(
                f"Unable to {params['side']} {params['quantity']} {params['symbol']}"
            )

    def modifyOrder(self, orderId, **kwargs):
        """
        Modify order of id orderId by specifying the new parameter change with kwargs
        """
        r = requests.put(
            self.url + f"accounts/{self.account_id}/orders/{orderId}",
            params=kwargs,
            headers=self._headers(),
        )
        return r.json()

    def deleteOrder(self, orderId):
        """ 
        Delete order of id orderId
        """
        r = requests.delete(
            self.url + f"accounts/{self.account_id}/orders/{orderId}",
            params={},
            headers=self._headers(),
        )
        return r.json()

    def Equity(
        self,
        symbol,
        side,
        quantity,
        type="market",
        duration="day",
        price=None,
        stop=None,
        preview=False,
        track=True,
    ):
        """
        Place an order to trade an equity security.

        Parameters

        * side: ['buy', 'buy_to_cover', 'sell', 'sell_short']
        * type: ['market', 'limit', 'stop', 'stop_limit']
        * duration: ['day', 'gtc', 'pre', 'post']
        """
        _class = "equity"
        # self._valid_order(symbol, side)
        # return self.make_params(locals())
        return self.order(self.make_params(locals()))

    def Option(
        self,
        symbol,
        optionSymbol,
        side,
        qty,
        type="market",
        duration="day",
        preview=False,
        price=None,
        stop=None,
        tag=None,
    ):
        """
        Place an order to trade a single option.

        Parameters 

        * side: ["buy_to_open", "buy_to_close", "sell_to_open", fghj."sell_to_close"]
        * type: ["market", "limit", "stop", "stop_limit"]
        * duration: ['day', 'gtc', 'pre', 'post']
        """
        self._check(e.OrderError, (_type, self.equityTypes))
        return self.order(self.make_params(locals()))

    def multileg(
        self,
        symbol,
        side,
        type,
        duration,
        *args,
        tag=None,
        preview=None,
        price=False,
        stop=None,
    ):
        """
        Place a multileg order with up to 4 legs. This order type allows for simple and complex option strategies.

        Parameters:
        
        * type: ["market", "debit", "credit", "even"]
        * duration: ['day', 'gtc', 'pre', 'post'] 
        * args: dictionary for each leg of form :

            {
                'option_symbol': OPTION_SYMBOL,
                'side': SIDE,
                'quantity': QTY,
            }

            parameters: 

            * side: ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"]
        """
        _class = "multileg"
        # internal checks for a valid request
        self._check(
            e.MultiLegKeyWordError,
            (type, self.complexTypes),
            (duration, self.duration),
        )

        [
            [
                self._check(e.MultiLegKeyWordError, (key, self.comboleg))
                for key in dct.keys()
            ]
            for dct in args
        ]
        return self.order(self.make_params(locals(), args))

    def Combo(
        self, symbol, *args, type="market", duration="day", price=None,
    ):
        """
        Place a combo order. This is a specialized type of order consisting of one equity leg and one option leg. It can optionally include a second option leg, for some strategies.

        The first dictionary doesn't include an option_symbol key, just the side and quantity. There is no option, its an equity trade
        """
        _class = "combo"
        return self.make_params(locals(), args)

    def oto(self, *args, duration="day"):
        """
        Place a one-triggers-other order. This order type is composed of two separate orders sent simultaneously. The property keys of each order are indexed.

        Parameters: 

        * duration: ['day', 'gtc', 'pre', 'post'] 
        * args: dictionary for each leg of form :

            {
                'symbol': SYMBOL,
                'quantity': QTY,
                'type': [
                    first order: ["limit", "stop", "stop_limit"],
                    second order: ["market","limit", "stop", "stop_limit"]]
                ]
                'option_symbol': OPTION_SYMBOL,
                'side': [
                    equity orders: ['buy', 'buy_to_cover', 'sell', 'sell_short']
                    option orders: ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"]
                ]
                'quantity': QTY,
                'price': PRICE,
                'stop': STOP
            }

        """
        _class = "oto"
        return self.order(self.make_params(locals(), args))

    def oco(self, *args, duration="day"):
        """
        Place a one-cancels-other order. This order type is composed of two separate orders sent simultaneously. The property keys of each order are indexed.
        
        Parameters: 

        * duration: ['day', 'gtc', 'pre', 'post'] 
        * args: dictionary for each leg of form :

            {
                'symbol': SYMBOL,
                'quantity': QTY,
                'type': [
                    first order: ["limit", "stop", "stop_limit"],
                    second order: ["market","limit", "stop", "stop_limit"]]
                    ***note: must be different for both legs
                ]
                'option_symbol': OPTION_SYMBOL,
                'side': [
                    equity orders: ['buy', 'buy_to_cover', 'sell', 'sell_short']
                    option orders: ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"]
                ]
                'quantity': QTY,
                'price': PRICE,
                'stop': STOP
            }
        """

        _class = "oco"
        return self.order(self.make_params(locals(), args))

    def otoco(self, *args):
        """
        Place a one-triggers-one-cancels-other order. This order type is composed of three separate orders sent simultaneously. The property keys of each order are indexed.
        
        Parameters: 
        args: dictionary for each leg of form :

            {
                'duration': ['day', 'gtc', 'pre', 'post'] 
                'symbol': SYMBOL,
                'quantity': QTY,
                'type': [
                    first order: ["limit", "stop", "stop_limit"],
                    second order:["limit", "stop", "stop_limit"],
                    third order: ["limit", "stop", "stop_limit"],
                ]
                'option_symbol': OPTION_SYMBOL,
                'side': [
                    equity orders: ['buy', 'buy_to_cover', 'sell', 'sell_short']
                    option orders: ["buy_to_open", "buy_to_close", "sell_to_open", "sell_to_close"]
                ]
                'quantity': QTY,
                'price': PRICE,
                'stop': STOP
            }
        """
        _class = "otoco"
        return self.order(self.make_params(locals(), args))


if __name__ == "__main__":
    pytrader = PyTradier()

