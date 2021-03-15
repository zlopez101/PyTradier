from PyTradier.base import BasePyTradier
from collections.abc import Iterable


class WatchList(BasePyTradier):
    """Create and update custom watchlists.
    """

    def parse_args(self, *args) -> str:
        """Most of the methods here allow for multiple symbols be inserted/created/destroyed. this helper function allows user to specify iterable in form of *args or list/tuple
        args can either be str instances, or a single iterable instance
        :return: comma delimited string
        :rtype: str
        """
        if len(args) == 1:
            # user pass a list
            return ", ".join(args[0])

        else:
            return ", ".join(args)

    def __call__(self, *args) -> list:
        """return user's watchlist. If watchlist Id specified, return that watchlist

        :return: list of watchlists
        :rtype: list
        """
        if args:
            # user wants a specific watchlist
            return self._get("/v1/watchlists")
        else:
            # user wants all the watchlists
            return self._get(f"/v1/watchlists/{args[0]}")

    def create(self, name: str, *args) -> dict:
        """Create a new watchlist. The new watchlist created will use the specified name and optional symbols upon creation.

        :param name: name of the watchlist to create
        :type name: str
        :return: [description]
        :rtype: dict
        """
        symbols = parse_args(args)
        return self._get("/v1/watchlists", params={"name": name, "symbols": symbols})

    def update(self, watchlist_id: str, watchlist_name: str, *args) -> dict:
        """Update an existing watchlist. This request will override the existing watchlist information with the parameters sent in the body.

        :param watchlist_id: A watchlist id
        :type watchlist_id: str
        :param watchlist_name: A watchlist name
        :type watchlist_name: str
        :return: [description]
        :rtype: dict
        """
        symbols = parse_args(args)
        return self._put(
            "/v1/watchlists/{watchlist_id}", params={"name": name, "symbols": symbols}
        )

    def delete(self, watchlist_id: str) -> dict:
        """Delete a specific watchlist.

        :param watchlist_id: A watchlist id
        :type watchlist_id: str
        :return: [description]
        :rtype: dict
        """
        return self._delete(f"/v1/watchlists/{watchlist_id}")

    def add(self, watchlist_id: str, *args) -> dict:
        """Add symbols to an existing watchlist. If the symbol exists, it will be over-written.

        :param watchlist_id: A watchlist id
        :type watchlist_id: str
        :return: [description]
        :rtype: dict
        """
        symbols = parse_args(args)
        return self._get(
            "/v1/watchlists/{watchlist_id}/symbols", params={"symbols": symbols}
        )

    def remove(self, watchlist_id: str, symbol: str) -> dict:
        """Remove a symbol from a specific watchlist.

        :param watchlist_id: A watchlist id
        :type watchlist_id: str
        :param symbol: Symbol to remove from watchlist
        :type symbol: str
        :return: [description]
        :rtype: dict
        """
        return self._delete(f"/v1/watchlists/{watchlist_id}/symbols/{symbol}")
