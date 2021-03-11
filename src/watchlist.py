import requests
from src.error import WatchListError


class WatchList:

    """
    Currently the watchlists property only contains names and values. Considerations for changing
    __init__ so that watchlist is populated 
    """

    def __init__(self, accountId, token, url):
        self.accountId = accountId
        self.token = token
        self.url = url
        self.watchlists = {}
        self._watchlists()

    def __repr__(self):
        return str(self.watchlists)

    def __getitem__(self, key):
        return self.watchlists[key]["symbols"]

    def get_id(self, name):
        """Return the ID of the watchlist"""
        return self.watchlists[name]["id"]

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    def _updateLocal(self, resp, key, value):
        """
        While we push data to tradier, we need to keep track of changes locally as well
        """
        if resp.status_code == 200:
            self.watchlists[key] = {}
            self.watchlists[key]["id"] = resp.json()["watchlist"]["id"]
            self.watchlists[key]["symbols"] = list(value)
            return self.watchlists[key]
        else:
            raise WatchListError(f"Error with key {key} and value {value}")

    def _watchlists(self):
        """
        Retrieve all of a users watchlists as dictionary with key name: id value
        """
        r = requests.get(self.url + "/watchlists", params={}, headers=self._headers())
        for lst in r.json()["watchlists"]["watchlist"]:

            self.watchlists[lst["name"]] = {"id": lst["id"]}
            self.watchlists[lst["name"]]["symbols"] = self.getwatchlist(lst["id"])

    def getwatchlist(self, watchListId) -> dict:
        """
        Retrieve a specific watchlist by id.
        """
        response = requests.get(
            self.url + f"/watchlists/{watchListId}", params={}, headers=self._headers(),
        ).json()["watchlist"]["items"]

        # default list has nothing in it, neither does a newly created list possibly
        # API returns the string "null"
        if response != "null":

            # response['item'] is either a list or a dictionary
            if isinstance(response["item"], list):
                return [resp["symbol"] for resp in response["item"]]
            else:
                # if dict
                return response["item"]["symbol"]
        else:
            return [None]

    def create(self, watchListName, *symbols):
        """
        Create a new watchlist. The new watchlist created will use the specified name and optional symbols upon creation.
        # """

        r = requests.post(
            self.url + "/watchlists",
            params={"name": watchListName, "symbols": ",".join(symbols)},
            headers=self._headers(),
        )
        return self._updateLocal(r, watchListName, list(symbols))

    def update(self, watchListName, *symbols):
        """
        Update an existing watchlist. This request will override the existing watchlist information with the parameters sent in the body.
        """
        try:
            _id = self.get_id(watchListName)
            r = requests.put(
                self.url + f"/watchlists/{_id}",
                params={"name": watchListName, "symbols": ",".join(symbols)},
                headers=self._headers(),
            )
            return self._updateLocal(r, watchListName, symbols)
        except KeyError as e:
            print(f"there is no watchlist: {e}")

        # _id = self.get_id(watchListName)
        # r = requests.put(
        #     self.url + f"/watchlists/{_id}",
        #     params={"name": watchListName, "symbols": ",".join(symbols)},
        #     headers=self._headers(),
        # )
        # return self._updateLocal(r, watchListName, symbols)

    def delete(self, watchListName):
        """
        Delete a specific watchlist.
        """
        try:
            _id = self.get_id(watchListName)
            r = requests.delete(
                self.url + f"/watchlists/{self.get_id(watchListName)}",
                params={},
                headers=self._headers(),
            )
            if r.status_code == 200:
                del self.watchlists[watchListName]
        except KeyError as e:
            print(f"there is no watchlist: {e}")

    def addSymbol(self, watchListName, *symbols):
        """
        Add symbols to an existing watchlist. If the symbol exists, it will be over-written.
        """
        r = requests.post(
            self.url + f"watchlists/{self.get_id(watchListName)}/symbols",
            params={"symbols": ",".join(symbols)},
            headers=self._headers(),
        )
        self._updateLocal(r,)
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


if __name__ == "__main__":
    import os

    watcher = WatchList(
        os.environ.get("TRADIER_PAPERACCOUNTID"),
        os.environ.get("TRADIER_SANDBOX_TOKEN"),
        "https://sandbox.tradier.com/v1/",
    )
    watcher.delete("New asdfsaf")
    print(watcher)
