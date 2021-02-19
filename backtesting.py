from datetime import datetime
from datetime import timedelta
import pandas as pd

import pyupbit
from pyupbit.quotation_api import _get_url_ohlcv

from trader import Trader
from utils import get_timepoint_ohlcv


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def backtesting(
    data,
    ticker="KRW-XRP",
):
    seed_movey = 100000
    count = 30

    bot = Trader(
        ticker=ticker,
        seed_movey=seed_movey,
    )

    results = []
    for i in range(data.shape[0] - count):
        data = data.iloc[i: count + i]

        low, high = data['low'][-1], data['high'][-1]
        bot.current_price = data['close'][-2]
        status, price = bot.check_status_price(data)

        result = {"timepoint": data.index[-1]}
        if status == "buy":
            available, price = check_available_bought_price(price, low, high)
            if available:
                if bot.buy(price):
                    result["status"] = "buy"
        elif status == "sell":
            available, price = check_available_sold_price(price, low, high)
            if available:
                if bot.sell(price):
                    result["status"] = "sell"
        if not hasattr(result, "status"):
            result["status"] = "none"

        result.update(bot.wallet)
        results.append(result)
        print(result)

    ROI = (bot.total_money / seed_movey) * 100
    print(ROI, "!!!!!")
    return ROI, results


def check_available_bought_price(price, low, high):
    assert low <= high
    if low < price:
        return True, min(high, price)
    return False, None

def check_available_sold_price(price, low, high):
    assert low <= high
    if price < high:
        return True, max(price, low)
    return False, None


if __name__ == "__main__":
    data_path = "data/minute5_data.parquet"
    data = pd.read_parquet(data_path)
    backtesting(data=data)
