from datetime import datetime
from datetime import timedelta
import pandas as pd

import pyupbit
from pyupbit.quotation_api import _get_url_ohlcv

from trader import Trader
from utils import get_timepoint_ohlcv


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def backtesting(
    interval="minute60",
    ticker="KRW-XRP",
    start="2020-12-01T00:00:00",
    end="2021-02-18T23:59:59",
):
    seed_movey = 100000
    time_standard = "+09:00"
    count = 30
    bot = Trader(
        ticker=ticker,
        seed_movey=seed_movey,
    )

    start_date = datetime.strptime(start, DATETIME_FORMAT)
    end_date = datetime.strptime(end, DATETIME_FORMAT)

    if interval == "minute5":
        interval_time = timedelta(minutes=5)
    elif interval == "minute60":
        interval_time = timedelta(hours=1)
    else:
        ValueError

    url = _get_url_ohlcv(interval=interval)
    n_chance = (end_date - start_date) // interval_time

    test_data = get_timepoint_ohlcv(
        url,
        ticker=ticker,
        to=end + time_standard,
        count=count + n_chance,
    )
    results = []
    for i in range(n_chance):
        start_date += interval_time
        timepoint = start_date.strftime(DATETIME_FORMAT) + time_standard

        data = test_data.iloc[i: count + i]

        low = data['low'][-1]
        high = data['high'][-1]

        bot.current_price = data['close'][-2]
        status, price = bot.check_status_price(data)

        result = {"timepoint": timepoint}
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
        result.update()
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
    backtesting()
