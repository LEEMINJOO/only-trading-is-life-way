import pandas as pd

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
    test_data: pd.DataFrame,
    seed_money: float = 1000000,  # 초기 자본금
    ticker: str = "KRW-EHT",
):

    upbit = MockUpbit(seed_money, ticker)
    trader = BasicTrader(upbit=upbit, ticker=ticker)

    # 모든 시점에 대해 for-loop을 돕니다.
    for t in range(test_data.shape[0] - 1):
        # t 시점의 데이터를 불러옵니다.
        data = test_data.iloc[t: t+1]

        # 입력된 t 시점의 데이터를 바탕으로
        # 살지, 팔지, 그대로 있을지와 거래 금액을 결정합니다.
        status, price = trader.check_market_status_price(data)

        # t + 1 시점의 데이터 중 저가와 고가를 추출합니다.
        next_data = test_data.iloc[t+1]
        low, high = next_data["low"], next_data["high"]

        if status == "buy":
            # 거래 금액 제약을 확인합니다.
            available, price = check_available_bought_price(price, low, high)
            if available:
                trader.buy(price)

        elif status == "sell":
            # 거래 금액 제약을 확인합니다.
            available, price = check_available_sold_price(price, low, high)
            if available:
                trader.sell(price)

    # 최근 코인 가격으로 총 자산을 계산합니다.
    recent_ticker_price = test_data["close"].iloc[-1]
    total_balance = (
        trader.krw_balance
        + trader.ticker_balance * recent_ticker_price
    )

    # 초기 자본금 대비 수익률을 계산합니다.
    ROI = ((total_balance - seed_money) / seed_money) * 100
    print(ROI, "% !!!!!")

    return ROI
