import pytest
import requests
from PyTradier.account import Account


def test_account_profile(monkeypatch):
    """
    GIVEN PyTradier API's access to the account module
    WHEN the account module doesn't require parameter input
    THEN appropriate return responses need to be retrieved
    """

    # account
    account = Account()
    profile = account.profile()
    print(profile.json())
