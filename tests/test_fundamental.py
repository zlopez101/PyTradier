import pytest
from datetime import datetime
from src.fundamental import *
from src.response import *


def test_Response(randomTicker):
    resp = randomTicker


def test_dividend():
    """
    GIVEN "GE" stock ticker
    THEN 
    """
    data = FundamentalData()
    resp = data.dividends("GE")
    assert isinstance(resp, DividendResponse), "Should return a dividend response"
    divs = resp.find("2020-01-01", "2020-12-01")
    assert len(divs) == 4, "There are 4 "
    divs = resp.find(datetime(2020, 1, 1), datetime(2020, 12, 1))
    assert isinstance(divs, list), "should be a list -> datetimes should also work"


def test_fundamental(randomTicker):
    data = FundamentalData()
    resp = data.dividends(randomTicker)

