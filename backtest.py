import pyupbit
from src.backtesting import backtesting


ticker = "KRW-ETH"
data = pyupbit.get_ohlcv(ticker=ticker, count=300)
backtesting(test_data=data)