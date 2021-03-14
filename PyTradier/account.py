import requests
from PyTradier.base import BasePyTradier
from PyTradier.utils import process_response
from functools import wraps
from typing import Union
from datetime import datetime


def selectArgs(func):
    @wraps(func)
    def wrapper(self, *args):
        result = func(self, *args)
        try:
            result.raise_for_status()
            if args:
                return {
                    key: value for key, value in result.json().items() if key in args
                }
            else:
                return result.json()
        except requests.exceptions.HTTPError as requesterror:
            print(
                f"there was an {response.status_code} error handling this response: {response.text}"
            )
        except KeyError as keyerror:
            print("key")
            print(keyerror)
        except TypeError as typerror:
            print(
                f"there was a TypeError handling this response, check function parameters {args[1:]} are compatible with {func.__annotations__}"
            )

    return wrapper


class Account(BasePyTradier):
    def profile(self, *args) -> dict:
        """returns requested information about a user's account

        :param keys: The keys to include in the response, defaults to ["profile", "id", "name"]
        :type keys: list, optional
        :return: Information requested, either a string or dict
        :rtype: Union[dict, str]
        """
        return self._get("/v1/user/profile")

    def balances(self) -> dict:
        """Get balances information for a specific user account. Account balances are calculated on each request during market hours. Each night, balance figures are reconciled with our clearing firm and used as starting point for the following market session.

        see more at https://documentation.tradier.com/brokerage-api/reference/response/balances

        :return: Balance dict
        :rtype: dict
        """
        return self._get(f"/v1/accounts/{self.account_id}/balances")

    def positions(self) -> list:
        """Return the positions of the account

        :return: list of position objects
        :rtype: list
        """
        return self._get(f"/v1/accounts/{self.account_id}/positions")

    def orders(self) -> list:
        """Retrieve orders placed within an account. This API will return orders placed for the market session of the present calendar day.
        """
        return self._get(f"/v1/accounts/{self.account_id}/orders")

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

        return self._get(f"/v1/accounts/{self.account_id}/orders/{str(orderId)}")


if __name__ == "__main__":
    from utils import printer

    account = Account()
    profile = account.profile("account")
    printer(profile)
