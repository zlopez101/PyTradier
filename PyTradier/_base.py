import os
import requests
from typing import Union


class BasePyTradier:
    def __init__(
        self, token: str = "TRADIER_SANDBOX_TOKEN", paper: bool = True,
    ):
        self.token = os.environ.get(token)
        if paper:
            self.url = "https://sandbox.tradier.com/v1/"
        else:
            self.url = "https://api.tradier.com/v1/"

        self.accountId = self._retrieve_account_id()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json",
        }

    def _retrieve_account_id(self) -> str:
        """Get the Account ID and set it as an attribute, needed for placing order and interacting with API

        :return: account ID number
        :rtype: str
        """
        response = self._get("user/profile")
        if response.status_code == 200:
            json_response = response.json()
            return json_response["profile"]["account"]["account_number"]

    def _get(self, endpoint: str, params: dict = {}) -> requests.Response:
        """base GET requests method for all subsequent API calls

        :param endpoint: the endpoint being requested. No need to add a prefix "/"
        :type endpoint: str
        :param params: dictionary with parameters to be sent
        :type params: dict
        :return: API response
        :rtype: request.Response
        """
        return requests.get(self.url + endpoint, params=params, headers=self._headers())

    def _post(self, endpoint: str, params: dict = {}):
        """base POST requests method for all subsequent API calls

        :param endpoint: the endpoint being requested. No need to add a prefix "/"
        :type endpoint: str
        :param params: dictionary with parameters to be sent
        :type params: dict
        :return: API response
        :rtype: request.Response
        """
        return self._process_response(
            requests.get(self.url + endpoint, params=params, headers=self._headers())
        )

    def _process_response(self, response: requests.Response) -> requests.Response:
        """Helper method that alerts user of rate limiting, invalid API calls, etc

        :param response: the raw response from API calls from self._get() and self._post()
        :type response: requests.Response
        :return: API response
        :rtype: request.Response
        """
        return response


if __name__ == "__main__":
    base = BasePyTradier()
    print(base.token)
    print(base.accountId)
    print(base.url)
