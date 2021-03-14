import os
import requests
from functools import wraps
from PyTradier.exceptions import RequestError
from typing import Union
import json


class BasePyTradier:
    def __init__(
        self, token: str = "TRADIER_SANDBOX_TOKEN", paper: bool = True,
    ):
        self.token = os.environ.get(token)
        if paper:
            self.url = "https://sandbox.tradier.com"
        else:
            self.url = "https://api.tradier.com"

        self.account_id = self._retrieve_account_id()

    def _symbol_prep(self, symbols: Union[str, list]) -> str:
        """allowing users to input either a str or list and automatically converting

        :param symbols: Either str of single symbol or list of symbols to retreive
        :type symbols: Union[str, list]
        :return: dict of {"symbols" : symbols}
        :rtype: dict
        """
        if isinstance(symbols, list):
            return ", ".join(symbols)
        else:
            return symbols

    def create_params(self, params: dict) -> dict:
        """Create the parameter dictionary for API calls

        :param params: The locally defined variables
        :type params: dict
        :return: dictionary of values that is not None nor self
        :rtype: dict
        """
        return {k: v for k, v in params.items() if v and k != "self"}

    def _bool_prep(self, boolean: Union[str, bool]) -> str:
        """allow user to input etierh a str or list and automatically converts to str       

        :param boolean: [description]
        :type boolean: Union[str, bool]
        :return: [description]
        :rtype: str
        """

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
        response = self._get("/v1/user/profile")
        if response.status_code == 200:
            json_response = response.json()
            return json_response["profile"]["account"]["account_number"]
        else:
            return response

    # @process_response()
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

    # @process_response([201])
    def _post(self, endpoint: str, params: dict = {}):
        """base POST requests method for all subsequent API calls

        :param endpoint: the endpoint being requested. No need to add a prefix "/"
        :type endpoint: str
        :param params: dictionary with parameters to be sent
        :type params: dict
        :return: API response
        :rtype: request.Response
        """
        return requests.post(
            self.url + endpoint, params=params, headers=self._headers()
        )

