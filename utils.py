from datetime import datetime

import pandas as pd

from pyupbit.request_api import _call_public_api
from pyupbit.quotation_api import _get_url_ohlcv


def get_timepoint_ohlcv(
    url,
    ticker="KRW-BTC",
    count=1,
    to="2020-12-01T00:00:00+09:00",
):
    try:
        contents = _call_public_api(url, market=ticker, to=to, count=count)[0]
        dt_list = [
            datetime.strptime(x["candle_date_time_kst"], "%Y-%m-%dT%H:%M:%S")
            for x in contents
        ]
        df = pd.DataFrame(
            contents,
            columns=[
                "opening_price",
                "high_price",
                "low_price",
                "trade_price",
                "candle_acc_trade_volume",
            ],
            index=dt_list,
        )
        df = df.rename(
            columns={
                "opening_price": "open",
                "high_price": "high",
                "low_price": "low",
                "trade_price": "close",
                "candle_acc_trade_volume": "volume",
            }
        )
        return df.iloc[::-1]
    except Exception as x:
        print(x.__class__.__name__)
        return None
