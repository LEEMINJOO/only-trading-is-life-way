import random


FEE = 0.0005
MIN_BOUGHT_MONEY = 100
MIN_SOLD_TICKER = 0.01


class Trader:
    def __init__(
        self,
        ticker,
        seed_movey,
    ):
        self.ticker = ticker
        self.seed_movey = seed_movey
        self.cash = seed_movey
        self.volume = 0
        self.avg_price = 0
        self.current_price = 0

    def check_status_price(self, df):
        status = ["buy", "sell", "none"]
        status = random.sample(status, 1)[0]
        price = df["close"][-2]
        return status, price

    def buy(self, price):
        available = self.check_available_bought_wallet()
        if available:
            volume = int(self.cash / (price * (1 + FEE)))
            self.avg_price = self.volume * self.avg_price + volume * price
            self.volume += volume
            self.avg_price /= self.volume
            self.cash -= volume * (price * (1 + FEE))
            return True
        return False

    def sell(self, price):
        available = self.check_available_sold_wallet()
        if available:
            self.cash += self.volume * (price * (1 - FEE))
            self.volume = 0.0
            return True
        return False

    def check_available_bought_wallet(self):
        if self.cash > MIN_BOUGHT_MONEY:
            return True
        return False

    def check_available_sold_wallet(self):
        if self.volume > MIN_SOLD_TICKER:
            return True
        return False

    @property
    def total_money(self):
        return (
            self.cash + self.volume * self.current_price
        )  # will be current price in api

    @property
    def wallet(self):
        return {
            "cash": self.cash,
            "volume": self.volume,
            "avg_price": self.avg_price,
            "current_price": self.current_price,
            "total_money": self.total_money,
        }
