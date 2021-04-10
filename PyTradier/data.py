from PyTradier.base import BasePyTradier
from typing import Union
from datetime import datetime


class MarketData(BasePyTradier):
    """All Methods currently only support string API calls, no datetime, bools, etc
    """

    def quotes(self, symbols: Union[str, list], greeks: bool = False) -> dict:
        """Get a list of symbols using a keyword lookup on the symbols description. Results are in descending order by average volume of the security. This can be used for simple search functions

        :param symbols: Comma-delimited list of symbols (equity or option)
        :type symbols: Union[str, list]
        :param greeks: Add greeks and volatility information (option only), defaults to False
        :type greeks: bool, optional
        :return: quotes for requested symbols
        :rtype: dict
        """
        symbols = self._symbol_prep(symbols)
        return self._get(
            "/v1/markets/quotes",
            params=self.create_params(locals()),
            dict_args=("quotes", "quotes"),
        )

    def option_chain(
        self,
        symbol: str,
        expiration: Union[str, datetime],
        greeks: Union[str, bool] = "false",
    ) -> dict:
        """Get all quotes in an option chain. Greek and IV data is included courtesy of ORATS. Please check out their APIs for more in-depth options data.

        :param symbol: Underlying symbol of the chain
        :type symbol: str
        :param expiration: Expiration for the chain
        :type expiration: Union[str, datetime]
        :param greeks: Add greeks and volatility information, defaults to "false"
        :type greeks: Union[str, bool], optional
        :return: Get all quotes in an option chain 
        :rtype: dict
        """
        return self._get(
            "/v1/markets/options/chains", params=self.create_params(locals())
        )

    def option_strike(self, symbol: str, expiration: Union[str, datetime]) -> list:
        """Get an options strike prices for a specified expiration date.

        :param symbol: Underlying symbol of the chain
        :type symbol: str
        :param expiration: Expiration for the chain
        :type expiration: Union[str, datetime]
        :return: [description]
        :rtype: list
        """

        return self._get(
            "/v1/markets/options/strikes", params=self.create_params(locals())
        )

    def option_lookup(self, underlying: str) -> dict:
        """Get all options symbols for the given underlying. This will include additional option roots (ex. SPXW, RUTW) if applicable.

        :param underlying: Underlying symbol of the chain
        :type underlying: str
        :return: dict {"rootSymbol": underlying, "options": [list of option symbols]}
        :rtype: dict
        """
        return self._get(
            "/v1/markets/options/lookup", params=self.create_params(locals())
        )

    def option_expirations(
        self,
        symbol: str,
        includeAllRoots: Union[str, bool] = "",
        strikes: Union[str, bool] = "",
    ) -> list:
        """Get expiration dates for a particular underlying.

        Note that some underlying securities use a different symbol for their weekly options (RUT/RUTW, SPX/SPXW). To make sure you see all expirations, make sure to send the includeAllRoots parameter. This will also ensure any unique options due to corporate actions (AAPL1) are returned.

        :param symbol: Underlying symbol of the chain
        :type symbol: str
        :param includeAllRoots: Send expirations related to all option roots, defaults to ''
        :type includeAllRoots: Union[str, bool], optional
        :param strikes: Add strike prices to each expiration, defaults to ''
        :type strikes: Union[str, bool], optional
        :return: list of expiration dates as str %Y-%m-%d
        :rtype: list
        """
        response = self._get(
            "/v1/markets/options/expirations", params=self.create_params(locals())
        )
        return response

    def historic_quotes(
        self, symbol: str, interval: str = "daily", start: str = None, end: str = None
    ) -> list:
        """Get historical pricing for a security. This data will usually cover the entire lifetime of the company if sending reasonable start/end times. You can fetch historical pricing for options by passing the OCC option symbol (ex. AAPL220617C00270000) as the symbol.

        :param symbol: Symbol to query
        :type symbol: str
        :param interval: Interval of time per timesale. One of: daily, weekly, monthly, defaults to "daily"
        :type interval: str, optional
        :param start: Start date represented as YYYY-MM-DD, defaults to None
        :type start: str, optional
        :param end: End date represented as YYYY-MM-DD, defaults to None
        :type end: str, optional
        :return: [description]
        :rtype: list
        """
        return self._get(
            "/v1/markets/history",
            params=self.create_params(locals()),
            dict_args=("history", "day"),
        )

    def time_and_sales(
        self, symbol: str, start: str, end: str, interval: str = "1min"
    ) -> list:
        """Time and Sales (timesales) is typically used for charting purposes. It captures pricing across a time slice at predefined intervals.

        Tick data is also available through this endpoint. This results in a very large data set for high-volume symbols, so the time slice needs to be much smaller to keep downloads time reasonable.`

        :param symbol: A single security symbol.
        :type symbol: str
        :param start: Start date/time for timesales range represented as YYYY-MM-DD HH:MM
        :type start: str
        :param end: Start date/time for timesales range represented as YYYY-MM-DD HH:MM
        :type end: str
        :param interval: Interval of time per timesale. One of: tick, 1min, 5min, 15min, defaults to "1min"
        :type interval: str, optional
        :return: list of dictionaries containing keys of ['time', 'timestamp', 'price', 'open', 'high', 'close', low', 'volume', 'vwap']
        :rtype: list
        """
        return self._get(
            "/v1/markets/timesales",
            params=self.create_params(locals()),
            dict_args=("series", "data"),
        )


if __name__ == "__main__":
    from utils import printer

    data = MarketData()
    symbol = "AAPL"
    response = data.option_lookup(symbol)
    # response = data.option_strike(symbol, dates[0])
    printer(response)
