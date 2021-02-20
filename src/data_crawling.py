from datetime import datetime
from datetime import timedelta
from time import sleep
from tqdm import tqdm

import pandas as pd

from pyupbit.quotation_api import _get_url_ohlcv

from utils import get_timepoint_ohlcv


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"


def data_crawling(
    data_path,
    interval="minute5",
    ticker="KRW-XRP",
    start="2020-12-01T00:00:00",
    end="2021-02-18T23:59:59",
):
    time_standard = "+09:00"
    interval_time = timedelta(hours=12)

    start_date = datetime.strptime(start, DATETIME_FORMAT)
    end_date = datetime.strptime(end, DATETIME_FORMAT)
    n_trial = (end_date - start_date) // interval_time

    url = _get_url_ohlcv(interval=interval)

    total_data = []
    for _ in tqdm(range(n_trial)):
        start_date += interval_time
        timepoint = start_date.strftime(DATETIME_FORMAT) + time_standard
        data = get_timepoint_ohlcv(
            url,
            ticker=ticker,
            to=timepoint,
            count=200,
        )
        total_data += [data]
        sleep(1)
    total_data = pd.concat(total_data)
    total_data = total_data.loc[~total_data.index.duplicated()]
    total_data.to_parquet(data_path)


if __name__ == "__main__":
    data_path = "../data/minute5_data.parquet"
    data_crawling(data_path)
