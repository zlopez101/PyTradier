import requests
import pprint
from functools import wraps
from PyTradier.exceptions import *


def process_response(*dict_args):
    """Helper method that alerts user of rate limiting, and parses the response for cleaner code inside method
    """

    def _process_response(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            try:
                response.raise_for_status()
                data_requested = response.json()
                for arg in dict_args:
                    data_requested = data_requested[arg]
                return data_requested
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

    return _process_response


def printer(response: requests.Response):
    """Helper function for testing endpoints

    :param response: the response from API call
    :type response: Response
    """

    pprint.pprint(response.status_code)
    pprint.pprint(response.headers)
    pprint.pprint(response.json())
