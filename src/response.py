from datetime import datetime, timedelta


class OrderResponse:

    """
    base class for interacting with order responses
    """

    def __init__(self, _orderResponse):
        for key, value in _orderResponse.items():
            setattr(self, key, value)

    @classmethod
    def from_order_conf(cls, _orderConf):
        return cls(_orderConf["order"])

    def __repr__(self):
        return f"Order(id:{self.id}, status: {self.status})\n"

    def modify(self, **kwargs):
        """
        modify the order
        """
        pass

    def delete(self):
        """
        delete the order
        """
        pass


class Response(object):
    """
    Response class for Fundamental Data Response
    """

    def __init__(self, _type, resp):

        self.symbol = resp["request"]
        self.type = _type
        self.results = resp["results"]

    def __repr__(self):
        return f"Response Data({self.type} for {self.request})"

    def __len__(self):
        return len(self.results)


class FundamentalResponse(Response):
    """
    Response class of Fundamental Data
    """

    def __init__(self, resp):
        super().__init__("Fundamental Data", resp)


class DividendResponse(Response):
    """
    Class for parsing the dividend.
    Usually the 'key' contains two values and one is empty for some reason. __init__ method tries to remove this value

    Example Object from dividends list:

    {   
        'share_class_id': '0P000002DO', 
        'dividend_type': 'CD', 
        'ex_date': '2020-09-25', 
        'cash_amount': 0.01, 
        'currency_i_d': 'USD', 
        'declaration_date': '2020-09-03',
        'frequency': 4,
        'pay_date': '2020-10-26',
        'record_date': '2020-09-28'
    }
    """

    def __init__(self, resp):
        super().__init__("Dividends", resp)
        lst = [
            res["tables"]["cash_dividends"]
            for res in self.results
            if res["tables"]["cash_dividends"] is not None
        ]
        if lst:
            self.dividends = lst[0]
        else:
            self.dividends = lst

    def __getitem__(self, val):
        return self.dividends[val]

    @property
    def count(self) -> int:
        """
        return the length of the dividend list
        """
        return len(self.dividends)

    @property
    def dividendAmounts(self) -> list:
        """
        return list of dividend amounts per share
        """
        return set([div["cash_amount"] for div in self.dividends])

    def find(self, _from, _to) -> list:
        """
        find all dividends in date range defined by _from and _to
 
        Parameters:
        _from: a datetime.datetime or a string of format 'YYYY-MM-DD'
        _to: a datetime.datetime or a string of format 'YYYY-MM-DD'
        """
        if not (isinstance(_from, datetime)):
            _from = datetime.strptime(_from, "%Y-%m-%d")
        if not (isinstance(_to, datetime)):
            _to = datetime.strptime(_to, "%Y-%m-%d")

        payDates = [
            datetime.strptime(dividend["pay_date"], "%Y-%m-%d")
            for dividend in self.dividends
        ]

        dividendsBetween = []

        for idx, paydate in enumerate(payDates):
            if paydate > _from and paydate < _to:
                dividendsBetween.append(self.dividends[idx])

        return dividendsBetween
