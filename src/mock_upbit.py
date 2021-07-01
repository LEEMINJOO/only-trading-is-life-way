class MockUpbit:
    def __init__(
        self,
        seed_money: float,  # 초기 잔고를 입력받습니다.
    ):
        # 코인은 이더리움으로 고정하겠습니다.
        ticker = "KRW-ETH"

        # 소유한 현금과 각 코인의 정보를 갖는 
        # `self.balances`를 정의합니다.
        self.balances = {
            "KRW": {
                "currency": "KRW",
                "balance": seed_money,
                "avg_buy_price": 0.,
            },
            ticker: {
                "currency": ticker,
                "balance": 0.,
                "avg_buy_price": 0.,
            },
        }

        self.fee = 0.0005

    def get_balance(
        self,
        ticker: str,
    ):
        # 잔고 정보를 간단하게 부를 수 있는 
        # 함수 `get_balance`를 정의합니다.
        return self.balances[ticker]["balance"]

    def buy_limit_order(
        self,
        ticker: str,
        price: float,
        volume: float,
    ) -> bool:
        if volume <= 0:
            return False

        # 수수료만큼 손해 보기 때문에 수수료만큼 더 부과되도록
        # `total_price`를 할당했습니다.
        total_price = price * volume * (1 + self.fee)

        # 원하는 금액보다 잔고가 많이 있을 때 체결됩니다.
        if self.balances["KRW"]["balance"] < total_price:
            return False

        # 거래 금액만큼 현금 잔고가 줄어듭니다.
        self.balances["KRW"]["balance"] -= total_price

        # 거래한 코인의 평균구매 단가를 계산하고,
        # 추가 매수한만큼 잔고가 증가합니다.
        self.balances[ticker]["avg_buy_price"] = (
            self.balances[ticker]["balance"] * self.balances[ticker]["avg_buy_price"]
            + volume * price
        )
        self.balances[ticker]["balance"] += volume
        self.balances[ticker]["avg_buy_price"] /= self.balances[ticker]["balance"]
        return True

    def sell_limit_order(
        self,
        ticker: str,
        price: float,
        volume: float,
    ) -> bool:
        # 수수료만큼 손해 보기 때문에 수수료만큼 더 부과되도록 
        # `total_price`를 할당했습니다.
        total_price = price * volume * (1 - self.fee)

        # 판매하고자 하는 코인의 수량보다 많이 가지고 있을 때만 거래합니다.
        if self.balances[ticker] < volume:
            return False

        # 거래한 만큼 잔고를 변화시킵니다.
        self.balances["KRW"] += total_price
        self.balances[ticker] -= volume
        return True
