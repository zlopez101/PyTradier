from PyTradier.base import BasePyTradier
from typing import Union


class FundamentalData(BasePyTradier):
    """This API is presently in Beta. It is only available to Tradier Brokerage account holders and should only be used in production applications with caution
    """

    def fundamentals(self, symbol: Union[str, list]) -> Union[dict, list]:
        """Get the company fundamental information

        :param symbol: single symbol or list of symbols to retrieve information on
        :type symbol: Union[str, list]
        :return: either a dict with single symbol response or list of dictionaries
        :rtype: Union[dict, list]
        """
        print(locals())
        return self._get(
            "/beta/markets/fundamentals/company",
            params={"symbols": self._symbol_prep(symbol)},
        )

    def corporateCalendar(self, symbol: Union[str, list]) -> Union[dict, list]:
        """
        Get Corporate calendar information for securities. Does not include dividend information
        """
        return self._get(
            "/beta/markets/fundamentals/calendars",
            params={"symbols": self._symbol_prep(symbol)},
        )
        # return Response("corporateCalendar", r)

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

    fundamentals = FundamentalData()
    response = fundamentals.fundamentalss("AAPL")

