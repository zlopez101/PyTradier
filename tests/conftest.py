import pytest
import requests
import random
import json


@pytest.fixture(scope="module")
def randomTicker():
    """
    Return a random ticker from the list of current S&P 500 members for testing.
    """
    with open(r"tests\Data\S_and_P_500.json", "r") as f:
        s_and_p = json.load(f)
        yield random.sample(s_and_p["S_and_P_500"], 2)


@pytest.fixture
def randomOption(randomTicker):
    """create a random option symbol based on random tickers selected from `randomTicker`

    Option Tickers contain ROOT + Expiration (yymmdd) + Side (C for call or P for put) + Strike (ddddd.ddd -> dddddddd)


    :yield: [description]
    :rtype: [type]
    """
    yield [
        ticker + "211005C00200000" for ticker in randomTicker
    ]  # 10-05-2021 $200 Strike Call


@pytest.fixture
def mockresponse():
    class MockResponse:
        def __init__(self, status, response_json_path):
            self.status_code = status
            with open(response_json_path, "r") as f:
                self.response = json.load(f)

        def raise_for_status(self):
            """need to implement a raise for status test
            """
            pass

        def json(self):
            return self.response

    yield MockResponse


@pytest.fixture
def patch_get(monkeypatch, mockresponse):
    """monkeypatch the requests.get function to return response dict for API calls. succesful API responses come from Tradier website.

    :param mockresponse: [description]
    :type mockresponse: [type]
    :return: [description]
    :rtype: [type]
    :yield: [description]
    :rtype: [type]
    """

    class PatchGet:
        def __init__(self, status, response_json_path):
            self.mocked = mockresponse(status, response_json_path)
            self.setter()

        def mock_get(self, url, params, headers):
            return self.mocked

        def setter(self):
            monkeypatch.setattr(requests, "get", self.mock_get)

    yield PatchGet


@pytest.fixture
def post_return_parameters(monkeypatch):
    """monkeypatch the requests.post function to return response dict for API calls.

    This a factory style method allows code re-use by defining the mockPost class once, and specifying a function to instantiate
    it when the mock_post method is called. The pytest monkeypatch module allows fixture to overwrite the requests.post function, 
    preventing a real API call, and resulting in any calls to requests.post returning a mockPost Object 
    :yield: [description]
    :rtype: [type]
    """

    class mockPost:
        def __init__(self, url, params, headers):
            self.url = url
            self.params = params
            self.headers = headers

    def mock_post(url, params, headers):
        return mockPost(url, params, headers)

    monkeypatch.setattr(requests, "post", mock_post)
