import requests


class Something:
    def __init__(self, accountId, token, url):
        self.accountId = accountId
        self.token = token
        self.url = url

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    def watchlists(self) -> dict:
        """
        Retrieve all of a users watchlists as dictionary with key name: id value
        """
        r = requests.get(self.url + "/watchlists", params={}, headers=self._headers())
        for lst in r.json()["watchlists"]["watchlist"]:
            self[lst["name"]] = {"id": lst["id"]}
            self[lst["name"]]["items"] = self.getwatchlist(lst["id"])

    def getwatchlist(self, watchListId) -> dict:
        """
        Retrieve a specific watchlist by id.
        """

        if watchListId in self.keys():
            r = requests.get(
                self.url + f"/watchlists/{watchListId}",
                params={},
                headers=self._headers(),
            )
            return r.json()["watchlist"]["items"]["item"]
        else:
            raise AttributeError(f"{watchListId} not in watchlists")
