from PyTradier.base import BasePyTradier
from typing import Union


def paperCheck(func):
    def _check(*args, **kwargs):
        if args[0].paper == False:
            return func(*args, **kwargs)
        else:
            print("Fundamental data is only possible with a Brokerage account")

    return _check


class FundamentalData(BasePyTradier):
    """This API is presently in Beta. It is only available to Tradier Brokerage account holders and should only be used in production applications with caution
    """

    @paperCheck
    def fundamentals(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Get the company fundamental information. This will print a massive list

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        return self._get(
            "/beta/markets/fundamentals/company",
            params={"symbols": self._symbol_prep(symbol)},
        )

    @paperCheck
    def corporateCalendar(self, symbol: Union[str, list]) -> Union[dict, list]:
        """
        Get Corporate calendar information for securities. Does not include dividend information
        """
        return self._get(
            "/beta/markets/fundamentals/calendars",
            params={"symbols": self._symbol_prep(symbol)},
        )
        # return Response("corporateCalendar", r)

    @paperCheck
    def dividend(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Get dividend information for a security. This will include previous dividends as well as formally announced future dividend dates.

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        return self._get(
            "/beta/markets/fundamentals/dividends",
            params={"symbols": self._symbol_prep(symbol)},
        )

    @paperCheck
    def CorporateActionInformation(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Retrieve corporate action information. This will include both historical and scheduled future actions.

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        return self._get(
            "/beta/markets/fundamentals/corporate_actions",
            params={"symbols": self._symbol_prep(symbol)},
        )

    @paperCheck
    def financialRatios(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Get standard financial ratios for a company.

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        return self._get(
            "/beta/markets/fundamentals/ratios",
            params={"symbols": self._symbol_prep(symbol)},
        )

    @paperCheck
    def financialInfo(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Retrieve corporate financial information and statements.

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        return self._get(
            "/beta/markets/fundamentals/financials",
            params={"symbols": self._symbol_prep(symbol)},
        )

    @paperCheck
    def priceStatistics(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Retrieve price statistic Information.

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        return self._get(
            "/beta/markets/fundamentals/statistics",
            params={"symbols": self._symbol_prep(symbol)},
        )


if __name__ == "__main__":
    from utils import printer

    fundamentals = FundamentalData(token="TRADIER_BROKERAGE_TOKEN", paper=False)
    response = fundamentals.fundamentals("AAPL")
    print("success\n\n")

    paper = FundamentalData()
    response = paper.fundamentals("AAPL")
