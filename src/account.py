import requests


class Account:
    def __init__(self, accountId, token, url):
        self.accountId = accountId
        self.token = token
        self.url = url

    def _headers(self):
        return {"Authorization": f"Bearer {self.token}", "Accept": "application/json"}

    @property
    def account(self):
        return requests.get(
            self.url + "user/profile", params={}, headers=self._headers()
        ).json()

    @property
    def balance(self):
        return requests.get(
            self.url + f"accounts/{self.accountId}/balances",
            params={},
            headers=self._headers(),
        ).json()

    @property
    def positions(self):
        return requests.get(
            self.url + f"accounts/{self.accountId}/positions",
            params={},
            headers=self._headers(),
        ).json()

    @property
    def orders(self):
        """
        Retrieve orders placed within an account. This API will return orders placed for the market session of the present calendar day.
        """
        return requests.get(
            self.url + f"accounts/{self.accountId}/orders",
            params={},
            headers=self._headers(),
        ).json()

    def history(
        self, symbol=None, page=1, limit=25, activity_type=None, start=None, end=None
    ):
        """
        Get historical activity for an account. This data originates with our clearing firm and inherently has a few limitations:

        Updated nightly (not intraday)
        Will not include specific time (hours/minutes) a position or order was created or closed
        Will not include order numbers

        Parameter:
        
        page:           Used for paginated results. Page to start results.

        limit:          Number of results to return per page.

        activity_type:  trade, option, ach, wire, dividend, fee, tax, journal, check, transfer, adjustment, interest

        startDate:	    yyyy-mm-dd

        endDate:	    yyyy-mm-dd

        symbol:	    	SPY
        """
        return requests.get(
            self.url + f"accounts/{self.accountId}/history",
            params={
                "symbol": symbol,
                "page": page,
                "limit": limit,
                "type": activity_type,
                "start": start,
                "end": end,
            },
            headers=self._headers(),
        ).json()

    def gainloss(
        self,
        symbol=None,
        page=1,
        limit=100,
        sortby="closedate",
        sort="desc",
        start=None,
        end=None,
    ):
        """
        Get cost basis information for a specific user account. This includes information for all closed positions. Cost basis information is updated through a nightly batch reconciliation process with our clearing firm.

        Parameter:
        
        page:       Used for paginated results. Page to start results. 

        limit:      Number of results to return per page.

        sortBy:     Field to sort the results. One of: openDate,closeDate

        sort:	    Sort direction. One of: asc,desc

        start:	    yyyy-mm-dd	    Account opening date

        end:      	yyyy-mm-dd	    End of current day

        """
        return requests.get(
            self.url + f"accounts/{self.accountId}/gainloss",
            params={
                "symbol": str(symbol),
                "page": str(page),
                "limit": str(limit),
                "sortBy": str(sortby),
                "sort": str(sort),
                "start": str(start),
                "end": str(end),
            },
            headers=self._headers(),
        ).json()

    def order(self, orderId, includeTags=False):
        """
        Get detailed information about a previously placed order.

        Parameters:

        includeTags: bool
        """
        return requests.get(
            self.url + f"accounts/{self.accountId}/orders/{str(orderId)}",
            params={"includeTags": str(includeTags)},
            headers=self._headers(),
        ).json()

