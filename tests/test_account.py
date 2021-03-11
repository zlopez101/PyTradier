import pytest
from src.response import OrderResponse


def test_properties(pytrader):
    """
    GIVEN PyTradier API's access to the account module
    WHEN the account module doesn't require parameter input
    THEN appropriate return responses need to be retrieved
    """
    # account
    account = pytrader.account.account
    assert account["account"]
    assert account["id"]
    assert account["name"]

    # balance
    balance = pytrader.account.balance
    assert balance["balances"]
    assert balance["balances"]["account_number"]

    # positions
    positions = pytrader.account.positions
    if positions["positions"] != "null":
        assert positions["positions"]["position"]

    # orders
    orders = pytrader.account.orders
    assert isinstance(orders, list)

    # specifc orders
    if len(orders) > 0:
        firstOrder = orders[0]
        assert isinstance(firstOrder, OrderResponse)
        print(firstOrder)
        retreived = pytrader.account.order(firstOrder.id)
        assert firstOrder.id == retreived.id, "these should match"

    # history

    # gainloss

