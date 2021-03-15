import pytest
from PyTradier.data import MarketData


class TestMarketData:
    """Not implemented: 
    """

    marketData = MarketData()

    def test_quotes(self, patch_get):
        # need to update for greeks parameter
        # need to update for multiple symbols vs 1
        patch = patch_get(200, r"tests\Success_API_responses\data\quotes.json")
        quotes = self.marketData.quotes("TEST SYMBOL")
        assert patch.mocked.response == quotes

    def test_option_chain(self, patch_get):
        # need to update for greeks parameter
        # need to update for datetime, str choice
        patch = patch_get(200, r"tests\Success_API_responses\data\option_chain.json")
        option_chain = self.marketData.option_chain("TEST SYMBOL", "TEST DATE")
        assert patch.mocked.response == option_chain

    def test_option_strikes(self, patch_get):
        # need to update for datetime, str choice
        patch = patch_get(200, r"tests\Success_API_responses\data\option_strike.json")
        option_strike = self.marketData.option_strike("TEST SYMBOL", "TEST DATE")
        assert patch.mocked.response == option_strike

    def test_option_lookup(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\data\option_lookup.json")
        option_lookup = self.marketData.option_lookup("TEST SYMBOL")
        assert patch.mocked.response == option_lookup

    def test_option_expirations(self, patch_get):
        # need to update for strikes, bool or str
        patch = patch_get(
            200, r"tests\Success_API_responses\data\option_expirations.json"
        )
        option_expirations = self.marketData.option_expirations("TEST SYMBOL")
        assert patch.mocked.response == option_expirations
