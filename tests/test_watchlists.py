from src.PyTradier import PyTradier


def test_watchlist():
    trader = PyTradier()

    watching = trader.watchlist.watchlists
    sample = trader.watchlist.getwatchlist(watching[1][1])
    assert isinstance(sample, dict), "Should return a dictionary"
    assert (
        sample["items"]["item"]["symbol"] == "AAPL"
    ), "Apple is the only thing we are watching."

