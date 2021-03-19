import requests
import pprint
from functools import wraps
from PyTradier.exceptions import *


def printer(response: requests.Response):
    """Helper function for testing endpoints

    :param response: the response from API call
    :type response: Response
    """

    pprint.pprint(response.status_code)
    pprint.pprint(response.headers)
    pprint.pprint(response.text)
    pprint.pprint(response.json())
