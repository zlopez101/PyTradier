import requests
import os
from src.response import *


class FundamentalData:
    def __init__(self):
        self.accountId = "6YA14703"
        self.token = os.environ.get("TRADIER_BROKERAGE_TOKEN")
        self.url = "https://api.tradier.com/v1/"

    def _createHeaders(self):
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    def baseQuery(self, symbol, apiEndpoint) -> list:
        """
        build the base query for all fundamental data requests
        """
        return requests.get(
            "https://api.tradier.com/" + apiEndpoint,
            params={"symbols": symbol},
            headers=self._createHeaders(),
        ).json()

    def fundamentals(self, symbol):
        """
        Get the company fundamental information
        """
        return FundamentalResponse(
            "Fundamental Data",
            self.baseQuery(symbol, "beta/markets/fundamentals/company")[0],
        )
        # return Response("fundamentals", r)

    def corporateCalendar(self, symbol):
        """
        Get Corporate calendar information for securities. Does not include dividend information
        """
        return self.baseQuery(symbol, "beta/markets/fundamentals/calendars")[0]
        # return Response("corporateCalendar", r)

    def dividends(self, symbol) -> DividendResponse:
        """
        Get dividend information for a security. This will include previous dividends as well as formally announced future dividend dates

        Returns a DividendResponse Object
        """
        return DividendResponse(
            self.baseQuery(symbol, "beta/markets/fundamentals/dividends")[0]
        )
        # return Response("dividends", r)

    def CorporateActionInformation(self, symbol):
        """
        Retrieve corporate action information. This will include both historical and scheduled future actions.
        """
        return self.baseQuery(symbol, "beta/markets/fundamentals/corporate_actions")[0]
        # return Response("CorporateActionInformation", r)

    def financialRatios(self, symbol):
        """
        Get standard financial ratios for a company 
        """
        return self.baseQuery(symbol, "beta/markets/fundamentals/ratios")[0]
        # return Response("financialRatios", r)

    def financialInfo(self, symbol):
        """
        Retrieve corporate financial information and statements
        """
        return self.baseQuery(symbol, "beta/markets/fundamentals/financials")[0]
        # return Response("financialInfo", r)

    def priceStatistics(self, symbol):
        """
        Retrieve price statistic Information
        """
        return self.baseQuery(symbol, "beta/markets/fundamentals/statistics")[0]
        # return Response("priceStatistics", r)


if __name__ == "__main__":
    import pprint

    dt = FundamentalData()
    resp = dt.dividends("GE")
    print(resp.find("2020-01-01", "2020-12-01"))

