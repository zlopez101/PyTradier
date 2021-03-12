import requests
from PyTradier.response import OrderResponse
from ._base import BasePyTradier


class Account(BasePyTradier):
    def profile(self):
        """ 
        {
            "profile": {
                "account": 
                    {
                        "account_number": "VA000001",
                        "classification": "individual",
                        "date_created": "2016-08-01T21:08:55.000Z",
                        "day_trader": false,
                        "option_level": 6,
                        "status": "active",
                        "type": "margin",
                        "last_update_date": "2016-08-01T21:08:55.000Z"
                    },
                "id": "id-gcostanza",
                "name": "George Costanza"
            }
        }
        """
        return self._get("user/profile")

    def balance(self):
        """
        {
        "balances": {
            "option_short_value": 0,
            "total_equity": 17798.360000000000000000000000,
            "account_number": "VA00000000",
            "account_type": "margin",
            "close_pl": -4813.000000000000000000,
            "current_requirement": 2557.00000000000000000000,
            "equity": 0,
            "long_market_value": 11434.50000000000000000000,
            "market_value": 11434.50000000000000000000,
            "open_pl": 546.900000000000000000000000,
            "option_long_value": 8877.5000000000000000000,
            "option_requirement": 0,
            "pending_orders_count": 0,
            "short_market_value": 0,
            "stock_long_value": 2557.00000000000000000000,
            "total_cash": 6363.860000000000000000000000,
            "uncleared_funds": 0,
            "pending_cash": 0,
        }   
        "margin": {
            "fed_call": 0,
            "maintenance_call": 0,
            "option_buying_power": 6363.860000000000000000000000,
            "stock_buying_power": 12727.7200000000000000,
            "stock_short_value": 0,
            "sweep": 0
        },
        "cash": {
            "cash_available": 4343.38000000,
            "sweep": 0,
            "unsettled_funds": 1310.00000000
        },
        "pdt": {
            "fed_call": 0,
            "maintenance_call": 0,
            "option_buying_power": 6363.860000000000000000000000,
            "stock_buying_power": 12727.7200000000000000,
            "stock_short_value": 0
        }
    }
}
        """
        return self._get(f"accounts/{self.accountId}/balances")

    def positions(self):
        """
        {
        "positions": {
            "position": [
                    {
                        "cost_basis": 207.01,
                        "date_acquired": "2018-08-08T14:41:11.405Z",
                        "id": 130089,
                        "quantity": 1.00000000,
                        "symbol": "AAPL"
                    },
                    {
                      "cost_basis": 1870.70,
                      "date_acquired": "2018-08-08T14:42:00.774Z",
                      "id": 130090,
                      "quantity": 1.00000000,
                      "symbol": "AMZN"
                    },
                ]
            }
        }
        """
        return (
            self.get(f"accounts/{self.accountId}/positions")
            .get("positions")
            .get("position")
        )

    def orders(self):
        """
        Retrieve orders placed within an account. This API will return orders placed for the market session of the present calendar day.
        """
        r = self.get(f"accounts/{self.accountId}/orders")
        return [OrderResponse(order) for order in r.get("orders", []).get("order")]

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
        return self.get(
            f"accounts/{self.accountId}/history",
            symbol=symbol,
            page=page,
            limit=limit,
            type=activity_type,
            start=start,
            end=end,
        )

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
        {
  "gainloss": {
    "closed_position": [
      {
        "close_date": "2018-10-31T00:00:00.000Z",
        "cost": 12.7,
        "gain_loss": -2.64,
        "gain_loss_percent": -20.7874,
        "open_date": "2018-06-19T00:00:00.000Z",
        "proceeds": 10.06,
        "quantity": 1.0,
        "symbol": "GE",
        "term": 134
      },
      {
        "close_date": "2018-09-21T00:00:00.000Z",
        "cost": 3.05,
        "gain_loss": -3.05,
        "gain_loss_percent": -100.0,
        "open_date": "2018-09-18T00:00:00.000Z",
        "proceeds": 0.0,
        "quantity": 1.0,
        "symbol": "SNAP180921P00008500",
        "term": 3
      },
      {
        "close_date": "2018-09-19T00:00:00.000Z",
        "cost": 913.95,
        "gain_loss": 6.05,
        "gain_loss_percent": 0.662,
        "open_date": "2018-09-18T00:00:00.000Z",
        "proceeds": 920.0,
        "quantity": 100.0,
        "symbol": "SNAP",
        "term": 1
      },
      {
        "close_date": "2018-06-25T00:00:00.000Z",
        "cost": 25.05,
        "gain_loss": -25.05,
        "gain_loss_percent": -100.0,
        "open_date": "2018-06-22T00:00:00.000Z",
        "proceeds": 0.0,
        "quantity": 1.0,
        "symbol": "SPY180625C00276000",
        "term": 3
      }
    ]
  }
}
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
        r = self.get(f"accounts/{self.accountId}/orders/{str(orderId)}")
        return OrderResponse.from_order_conf(r)

