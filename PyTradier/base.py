import os
import requests
from functools import wraps
from PyTradier.exceptions import RequestError, OrderError
from typing import Union
import json
from datetime import datetime


class BasePyTradier:
    def __init__(
        self, token: str = "TRADIER_SANDBOX_TOKEN", paper: bool = True,
    ):
        self.token = os.environ.get(token)
        self.paper = paper
        if self.paper:
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
        elif isinstance(symbols, str):
            return symbols
        else:
            # raise some error
            print("this don't work!")

    def _bool_prep(self, boolean: Union[str, bool]) -> str:
        """allow user to input etierh a str or list and automatically converts to str       

        :param boolean: [description]
        :type boolean: Union[str, bool]
        :return: [description]
        :rtype: str
        """
        if isinstance(boolean, str):
            return boolean
        elif isinstance(boolean, bool):
            return str(boolean).lower()
        else:
            # raise some error
            print("this don't work!")

    def _datetime_prep(self, date: Union[str, datetime]) -> str:
        """allow user to input either a str or datetime and convert to str

        :param date: date in format YYYY-MM-DD or datetime
        :type date: Union[str, datetime]
        :return: str in format YYYY-MM-DD
        :rtype: str
        """
        if isinstance(date, str):
            return date
        elif isinstance(date, datetime):
            return date.strftime("%Y-%m-%d")
        else:
            # raise some error
            print("this don't work")

    def create_params(self, params: dict) -> dict:
        """Create the parameter dictionary for API calls

        :param params: The locally defined variables
        :type params: dict
        :return: dictionary of values that is not None nor self
        :rtype: dict
        """
        return {k: v for k, v in params.items() if v and k != "self"}

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
        return self._get(
            "/v1/user/profile", dict_args=("profile", "account", "account_number")
        )

    def process_response(
        self, response: requests.Response, dict_args: tuple
    ) -> Union[dict, list]:
        """Process the response for GET, POST, PUT, DELETE methods

        :param response: raw response object
        :type response: requests.Response
        :param dict_args: keys to parse successful response object, defaults to ()
        :type dict_args: tuple, optional
        :return: Processed response, either dict or list of dicts depending on endpoint
        :rtype: Union[dict, list]
        """
        try:
            response.raise_for_status()
            requested_data = response.json()
            for arg in dict_args:
                # return an empty dictionary if key doesn't exist
                # this could occur if account is new - no history
                requested_data = requested_data[arg]
            return requested_data
        except requests.exceptions.HTTPError as requesterror:
            print(
                f"there was an {response.status_code} error handling this response: {response.text}."
            )
        except KeyError as keyerror:

            # handle error exception
            try:
                requested = requested_data["errors"]["error"]
                raise OrderError(requested)
            except KeyError as stillwrong:
                print("something unexpected happened...")
                print(f"{requested} was the json response for this call")

    def _get(
        self, endpoint: str, params: dict = {}, dict_args: tuple = ()
    ) -> Union[dict, list]:
        """base GET requests method for all subsequent API calls

        :param endpoint: the endpoint being requested
        :type endpoint: str
        :param params: dictionary with parameters to be sent
        :type params: dict
        :param dict_args: dictionary keys for parsing the response
        :type dict_args: tuple
        :return: API response
        :rtype: Union[dict, list]
        """
        response = requests.get(
            self.url + endpoint, params=params, headers=self._headers()
        )
        return self.process_response(response, dict_args)

    def _post(
        self, endpoint: str, params: dict = {}, dict_args: tuple = ()
    ) -> Union[dict, list]:
        """base POST requests method for all subsequent API calls

        :param endpoint: the endpoint being requested
        :type endpoint: str
        :param params: dictionary with parameters to be sent
        :type params: dict
        :return: API response
        :rtype: Union[dict, list]
        """
        response = requests.post(
            self.url + endpoint, params=params, headers=self._headers()
        )
        return self.process_response(response, dict_args)

    def _put(
        self, endpoint: str, params: dict = {}, dict_arg: tuple = ()
    ) -> Union[dict, list]:
        """base PUT requests method for all API calls

        :param endpoint: the endpoint being requested
        :type endpoint: str
        :param params: dictionary with parameters to be sent, defaults to {}
        :type params: dict, optional
        :return: [description]
        :rtype: Union[dict, list]
        """
        pass

    def _delete(
        self, endpoint: str, params: dict = {}, dict_arg: tuple = ()
    ) -> Union[dict, list]:
        """base DELETE request method for all API calls

        :param endpoint: [description]
        :type endpoint: str
        :param params: [description], defaults to {}
        :type params: dict, optional
        :param dict_arg: [description], defaults to ()
        :type dict_arg: tuple, optional
        :return: [description]
        :rtype: Union[dict, list]
        """
        pass
