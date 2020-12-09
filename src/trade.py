from datetime import datetime


class TradePacket:
    def __init__(self, lst):
        self.trades = [Trade(trade) for trade in lst]
        self.symbol = self.trades[0].symbol
        # self.open
        # self.high
        # self.low
        # self.close
        # self.volume
        # self.timedelta
        self.beginTime = self.trades[0].date
        self.endTime = self.trades[-1].date

    def __repr__(self):
        return f"{self.symbol} TradePacket from {self.beginTime.strftime('%Y-%m-%d %H:%M:%S')} - {self.endTime.strftime('%Y-%m-%d %H:%M:%S')}"


class Trade(dict):
    def __init__(self, kwargs):  # , symbol, exch, price, size, cvol, date, last):
        for key, value in kwargs.items():
            setattr(self, key, value)

        self.price = float(self.price)
        self.size = float(self.size)
        self.cvol = float(self.cvol)
        self.date = datetime.fromtimestamp(int(self.date) / 100)
        self.last = float(self.last)

    def __repr__(self):
        return f"Trade(symbol: {self.symbol}, price: {self.price}, size:{self.size})"
