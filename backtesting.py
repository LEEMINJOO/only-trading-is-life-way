import pandas as pd
import pyupbit

from src.trader import BasicTrader
from src.mock_upbit import MockUpbit


def check_available_bought_price(
    price,  # 매수 가격
    low,    # 다음 시점 저가
    high,   # 다음 시점 고가
):
    assert low <= high
    # 저가 보다 매수 가격이 큰 경우 거래 가능
    if low < price:
        # 고가 보다 매수 가격이 큰 경우 고가로 거래
        return True, min(high, price)
    return False, None


def check_available_sold_price(
    price,  # 매도 가격
    low,    # 다음 시점 저가
    high,   # 다음 시점 고가
):
    assert low <= high
    # 고가 보다 매도 가격이 작은 경우 거래 가능
    if price < high:
        # 저가 보다 매도 가격이 작은 경우 저가로 거래
        return True, max(price, low)
    return False, None


def backtesting(
    test_data,
    seed_money=1000000,
    ticker="KRW-EHT",
):

    upbit = MockUpbit(seed_money, ticker)
    trader = BasicTrader(upbit=upbit, ticker=ticker)

    results = []
    for i in range(test_data.shape[0] - 1):
        data = test_data.iloc[i: i+1]

        status, price = trader.check_market_status_price(data)

        next_data = test_data.iloc[i+1]
        low, high = next_data["low"], next_data["high"]

        result = {"timepoint": data.index[-1]}
        if status == "buy":
            available, price = check_available_bought_price(price, low, high)
            if available:
                trader.buy(price)
                result["status"] = "buy"

        elif status == "sell":
            available, price = check_available_sold_price(price, low, high)
            if available:
                trader.sell(price)
                result["status"] = "sell"

        else:
            result["status"] = "none"


if __name__ == "__main__":
    data = pyupbit.get_ohlcv(count=300)
    backtesting(test_data=data)
