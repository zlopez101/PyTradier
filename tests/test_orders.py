import pytest
from PyTradier.order import *


def test_equity_orders(randomTicker):

    stoplimit = StopLimitOrder("equity", randomTicker[0], 10, 10.5, 9, "gtc")

    limit = LimitOrder


def test_option_order(randomTicker):
    pass


def test_combo_order(randomTicker):
    pass


def test_multileg_order(randomTicker):
    pass


def test_one_cancels_other(randomTicker):
    pass


def test_one_triggers_other(randomTicker):
    pass


def test_one_cancels_other_triggers_other(randomTicker):
    pass
