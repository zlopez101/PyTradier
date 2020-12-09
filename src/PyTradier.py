import requests
import os
import websockets, asyncio
from datetime import datetime
import json
from fundamental import FundamentalData
from account import Account
from error import RequiredError
from base import BasePyTradier


class PyTradier(BasePyTradier):
    def __init__(self, paper=True):
        super().__init__(paper)
        self.account = Account(self.accountId, self.token, self.url)
        self.positions = self.account.positions
        self.fundamental = FundamentalData()

    def _params(
        self,
        _class,
        symbol,
        side,
        quantity,
        _type,
        duration,
        preview,
        limitPrice=None,
        stopPrice=None,
        tag=None,
    ):
        """
        create parameters for an equity order
        also used to build base dictionary for option order

        Required

        Str symbol
        Str side: ['buy', 'buy_to_cover', 'sell', 'sell_short']
        Str quantity
        Str type: ['market', 'limit', 'stop', 'stop_limit']
        Str duration: ['day', 'gtc', 'pre', 'post']

        Optional

        Str Limit: required for limit and stop_limit orders
        Str Stop: required for stop and stop_limit orders
        Str tag: descripter for the order
        """
        params = {
            "class": _class,
            "symbol": symbol,
            "side": side,
            "quantity": str(quantity),
            "type": _type,
            "duration": duration,
            "preview": preview,
        }
        # optional parameters
        if limitPrice:
            params["price"] = limitPrice
        if stopPrice:
            params["stop"] = stopPrice
        if tag:
            params["tag"] = tag

        # if limit, stop, or stop_limit order -> check requirements
        if params["type"] == "limit":
            if not params.get("price", None):
                raise RequiredError
        if params["type"] == "stop":
            if not params.get("stop", None):
                raise RequiredError
        if params["type"] == "stop_limit":
            if not params.get("stop", None) or params.get("price", None):
                raise RequiredError
        return params

    def createEquityOrder(
        self, symbol, side, qty, _type="market", duration="day", preview=False
    ):
        params = self._params(symbol, "equity", side, qty, _type, duration, preview)
        return requests.post(
            self.url + f"accounts/{self.accountId}/orders",
            params=params,
            headers=self._headers(),
        ).json()

    def createOptionOrder(
        self,
        symbol,
        optionSymbol,
        side,
        qty,
        _type="market",
        duration="day",
        preview=False,
    ):
        params = self._params(symbol, "option", side, qty, _type, duration, preview)
        params["option_symbol"] = optionSymbol
        return requests.post(
            self.url + f"accounts/{self.accountId}/orders",
            params=params,
            headers=self._headers(),
        )

    def _createLeg(self, sym, side, qty, _type):
        """
        create a leg 
        """
        raise NotImplementedError


if __name__ == "__main__":
    pytrader = Tradier()
