import requests
from PyTradier.base import BasePyTradier
from functools import wraps
from typing import Union
from datetime import datetime


class Account(BasePyTradier):
    """class for gathering all account related API calls
    """

    def profile(self) -> dict:
        """returns requested information about a user's account

        :return: Information requested, either a string or dict
        :rtype: Union[dict, str]
        """
        return self._get("/v1/user/profile", dict_args=("profile",))

    def balances(self) -> dict:
        """Get balances information for a specific user account. Account balances are calculated on each request during market hours. Each night, balance figures are reconciled with our clearing firm and used as starting point for the following market session.

        see more at https://documentation.tradier.com/brokerage-api/reference/response/balances

        :return: Balance dict
        :rtype: dict
        """
        return self._get(
            f"/v1/accounts/{self.account_id}/balances", dict_args=("balances",)
        )

    def positions(self) -> list:
        """Return the positions of the account

        :return: list of position objects
        :rtype: list
        """
        return self._get(
            f"/v1/accounts/{self.account_id}/positions",
            dict_args=("positions", "position"),
        )

    def orders(self) -> list:
        """Retrieve orders placed within an account. This API will return orders placed for the market session of the present calendar day.

        :return: list of Order dictionaries
        :rtype: list
        """
        return self._get(
            f"/v1/accounts/{self.account_id}/orders", dict_args=("orders", "order")
        )

    def history(
        self,
        page: int = 1,
        limit: int = 25,
        activity_type: list = [],
        start: str = "",
        end: str = "",
        symbol: str = "",
    ) -> list:
        """Get historical activity for an account. This data originates with our clearing firm and inherently has a few limitations:

        Updated nightly (not intraday)
        Will not include specific time (hours/minutes) a position or order was created or closed
        Will not include order numbers

        :param page: Used for paginated results. Page to start results, defaults to 1
        :type page: int, optional
        :param limit: Number of results to return per page, defaults to 25
        :type limit: int, optional
        :param activity_type: Activity type, defaults to []
        :type activity_type: list, optional
        :param start: start date, empty string will default to account opening date, defaults to ""
        :type start: str, optional
        :param end: end date, empty string will default to end of current day, defaults to ""
        :type end: str, optional
        :param symbol: Filter by security symbol, defaults to ""
        :type symbol: str, optional
        :return: list of events
        :rtype: list
        """
        return self._get(
            f"/v1/accounts/{self.account_id}/history",
            params=self.create_params(locals()),
            dict_args=("history", "event"),
        )

    def gainloss(
        self,
        symbol: str = None,
        page: int = 1,
        limit: int = 100,
        sortby: str = "closedate",
        sort: str = "desc",
        start: Union[str, datetime] = None,
        end: Union[str, datetime] = None,
    ) -> dict:
        """Get cost basis information for a specific user account. This includes information for all closed positions. Cost basis information is updated through a nightly batch reconciliation process with our clearing firm.

        :param symbol: Filter by security symbol, defaults to None
        :type symbol: str, optional
        :param page: Used for paginated results - Page to start results, defaults to 1
        :type page: int, optional
        :param limit: Number of results to return per page, defaults to 100
        :type limit: int, optional
        :param sortby: Field to sort the results. One of ['openDate', 'closeDate'], defaults to "closedate"
        :type sortby: str, optional
        :param sort: Sort directions, One of ['asc', 'desc'], defaults to "desc"
        :type sort: str, optional
        :param start: Start Date, defaults to None
        :type start: Union[str, datetime], optional
        :param end: End Date, defaults to None
        :type end: Union[str, datetime], optional
        :return: list of positions
        :rtype: dict
        """

        return self._get(
            self.url + f"/v1/accounts/{self.account_id}/gainloss",
            params=self.create_params(locals()),
            dict_args=("gainloss", "closed_position"),
        )

    def order(self, orderId: str, includeTags=False) -> dict:
        """Get detailed information about a previously placed order.

        :param orderId: OrderId of the order you want more information on
        :type orderId: str
        :param includeTags: Include order tag on response, defaults to False
        :type includeTags: bool, optional
        :return: dict with detailed information
        :rtype: dict
        """

        return self._get(
            f"/v1/accounts/{self.account_id}/orders/{str(orderId)}",
            dict_args=("order",),
        )


if __name__ == "__main__":
    from utils import printer

    account = Account()
    profile = account.profile("account")
    printer(profile)
