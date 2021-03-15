import pytest
from PyTradier.fundamental import FundamentalData
from PyTradier.exceptions import AuthError


class TestFundamental:
    """Need to work multiple symbols
    """

    paper_fundamental = FundamentalData()

    brokerage_fundamental = FundamentalData(paper=False)  # in production

    def test_company_info(self, patch_get):
        patch = patch_get(
            200, r"tests\Success_API_responses\fundamental\company_info.json"
        )

        with pytest.raises(AuthError):
            company_info = self.paper_fundamental.company_info()
            # assert patch.mocked.response["company_info"] == company_info

        company_info = self.brokerage_fundamental.company_info("SYBMOL")
        assert patch.mocked.response == company_info

    def test_corporate_calendar(self, patch_get):
        patch = patch_get(
            200, r"tests\Success_API_responses\fundamental\corporate_calendar.json"
        )

        with pytest.raises(AuthError):
            corporate_calendar = self.paper_fundamental.corporate_calendar()
            # assert patch.mocked.response == corporate_calendar

        corporate_calendar = self.brokerage_fundamental.corporate_calendar("SYBMOL")
        assert patch.mocked.response == corporate_calendar

    def test_dividends(self, patch_get):
        patch = patch_get(
            200, r"tests\Success_API_responses\fundamental\dividends.json"
        )

        with pytest.raises(AuthError):
            dividends = self.paper_fundamental.dividends()
            # assert patch.mocked.response == dividends

        dividends = self.brokerage_fundamental.dividends("SYBMOL")
        assert patch.mocked.response == dividends

    def test_corporate_actions(self, patch_get):
        patch = patch_get(
            200, r"tests\Success_API_responses\fundamental\corporate_actions.json"
        )

        with pytest.raises(AuthError):
            corporate_actions = self.paper_fundamental.corporate_actions()
            # assert patch.mocked.response == corporate_actions

        corporate_actions = self.brokerage_fundamental.corporate_actions("SYBMOL")
        assert patch.mocked.response == corporate_actions

    def test_ratios(self, patch_get):
        patch = patch_get(200, r"tests\Success_API_responses\fundamental\ratios.json")

        with pytest.raises(AuthError):
            ratios = self.paper_fundamental.ratios()
            # assert patch.mocked.response == ratios

        ratios = self.brokerage_fundamental.ratios("SYBMOL")
        assert patch.mocked.response == ratios

    def test_financial_reports(self, patch_get):
        patch = patch_get(
            200, r"tests\Success_API_responses\fundamental\financial_reports.json"
        )

        with pytest.raises(AuthError):
            financial_reports = self.paper_fundamental.financial_reports()
            # assert patch.mocked.response == financial_reports

        financial_reports = self.brokerage_fundamental.financial_reports("SYBMOL")
        assert patch.mocked.response == financial_reports

    def test_price_statistics(self, patch_get):
        patch = patch_get(
            200, r"tests\Success_API_responses\fundamental\price_statistics.json"
        )

        with pytest.raises(AuthError):
            price_statistics = self.paper_fundamental.price_statistics()
            # assert patch.mocked.response == price_statistics

        price_statistics = self.brokerage_fundamental.price_statistics("SYBMOL")
        assert patch.mocked.response == price_statistics
