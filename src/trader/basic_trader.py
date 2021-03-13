class BasicTrader:
    def __init__(
        self,
        upbit,
        ticker,
    ):
        self.upbit = upbit
        self.ticker = ticker

    @property
    def krw_balance(self):
        return self.upbit.get_balance(ticker="KRW")

    @property
    def ticker_balance(self):
        return self.upbit.get_balance(ticker=self.ticker)

    def buy(self):
        krw_price = 10000
        if self.krw_balance > krw_price:
            self.upbit.buy_market_order(
                ticker=self.ticker,
                price=krw_price,
            )
            print(f"Buy {self.ticker}, KRW: {krw_price}")

    def sell(self, ticker_price, ticker_volume):
        self.upbit.sell_limit_order(
            ticker=self.ticker,
            price=ticker_price,
            volume=ticker_volume,
        )
        print(f"Sell {self.ticker}, Ticker: {self.ticker_balance}")

    @property
    def avg_ticker_price(self):
        balances = self.upbit.get_balances()
        for balance in balances:
            if self.ticker.split('-')[1] == balance['currency']:
                return float(balance['avg_buy_price'])
        return 0.0
