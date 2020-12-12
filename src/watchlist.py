import requests


class WatchList:
    def __init__(self, accountId, token, url):
        self.accountId = accountId
        self.token = token
        self.url = url

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    @property
    def watchlists(self):
        """
        Retrieve all of a users watchlists.
        """
        r = requests.get(self.url + "/watchlists", params={}, headers=self._headers())
        return [(lst["name"], lst["id"]) for lst in r.json()["watchlists"]["watchlist"]]

    def getwatchlist(self, watchListId):
        """
        Retrieve a specific watchlist by id.
        """
        assert watchListId in [
            _id[1] for _id in self.watchlists
        ], f"WatchListId of {watchListId} not in {self.watchlists}"
        r = requests.get(
            self.url + f"/watchlists/{watchListId}", params={}, headers=self._headers()
        )
        return r.json()["watchlist"]

    def create(self, watchListName, symbols):
        """
        Create a new watchlist. The new watchlist created will use the specified name and optional symbols upon creation.
        """

        r = requests.post(
            self.url + "/watchlists",
            params={"name": watchListName, "symbols": ",".join(symbols)},
            headers=self._headers(),
        )
        return r.json()

    def update(self, watchListId, watchListName, symbols):
        """
        Update an existing watchlist. This request will override the existing watchlist information with the parameters sent in the body.
        """
        assert watchListId in self.watchlists
        r = requests.put(
            self.url + f"/watchlists/{watchListId}",
            params={"name": watchListName, "symbols": ",".join(symbols)},
            headers=self._headers(),
        )
        return r.json()

    def delete(self, watchListId):
        """
        Delete a specific watchlist.
        """
        r = requests.delete(
            self.url + f"/watchlists/{watchlist_id}", params={}, headers=self._headers()
        )
        return r.json()

    def addSymbol(self, watchListId, symbols):
        """
        Add symbols to an existing watchlist. If the symbol exists, it will be over-written.
        """
        r = requests.post(
            self.url + f"watchlists/{watchlist_id}/symbols",
            params={"symbols": ",".join(symbols)},
            headers=self._headers(),
        )
        return r.json()

    def remove(self, watchListId, symbol):
        """
        Remove a symbol from a specific watchlist.
        """
        r = requests.delete(
            self.url + f"/watchlists/{watchlist_id}/symbols/{symbol}",
            params={},
            headers=self._headers(),
        )
        return r.json()
