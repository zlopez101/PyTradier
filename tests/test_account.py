import pytest
import requests
import PyTradier
from PyTradier.account import Account
import json


class TestAccount:

    account = Account()

    def test_profile(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\profile.json")
        profile = self.account.profile()
        assert patch.mocked.response == profile.json()

    def test_balances(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\balances.json")
        balances = self.account.balances()
        assert patch.mocked.response == balances.json()

    def test_positions(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\positions.json")
        positions = self.account.positions()
        assert patch.mocked.response == positions.json()

    def test_orders(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\orders.json")
        orders = self.account.orders()
        assert patch.mocked.response == orders.json()

    def test_history(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\history.json")
        history = self.account.history()
        assert patch.mocked.response == history.json()

    def test_gainloss(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\gainloss.json")
        gainloss = self.account.gainloss()
        assert patch.mocked.response == gainloss.json()

    def test_order(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\account\order.json")
        order = self.account.order("OrderId")
        assert patch.mocked.response == order.json()
