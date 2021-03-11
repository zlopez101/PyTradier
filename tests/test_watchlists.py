import pytest


def test_watchlist(pytrader, randomTicker):
    """
    GIVEN watchlist module
    WHEN
    THEN 
    """

    # retrieve a watchlist and check
    sample = pytrader.watchlist["Sample Watchlist"]
    assert isinstance(sample, list), "Should be a list of symbols in 'Sample Watchlist'"
    assert "AAPL" in sample, "Apple is the only thing we are watching."

    # create a watchlist
    resp = pytrader.watchlist.create("New Watchlist", randomTicker[0])
    assert (
        randomTicker[0] in resp["symbols"]
    ), f"{randomTicker[0]} is the random addition"

    # update the watchlist
    # first update the symbols
    pytrader.watchlist.update("New Watchlist", randomTicker[1])
    assert (
        randomTicker[1] in pytrader.watchlist["New Watchlist"]
    ), f"{randomTicker[1]} replaces {randomTicker[0]}"

    # delete a watchlist
    pytrader.watchlist.delete("New Watchlist")
    assert not (
        pytrader.watchlist.watchlists.get("New Watchlist")
    ), "Watchlist should have been deleted"

