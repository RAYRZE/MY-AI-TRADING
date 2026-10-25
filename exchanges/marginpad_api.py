from marginpad import MarginPad
from config import MARGINPAD_API_KEY, INITIAL_BALANCE

class MarginPadAdapter:
    def __init__(self):
        self.mp = MarginPad(MARGINPAD_API_KEY)
        # Set simulasi awal: saldo 1000, ada slippage sedikit biar realistis
        self.mp.sim(start_balance_usd=INITIAL_BALANCE, slippage_bps=5)

    def get_price(self, symbol: str) -> float:
        return self.mp.price(symbol)

    def open_position(self, symbol: str, direction: str, margin_usd: float, leverage: int):
        # direction: "long" atau "short"
        return self.mp.open(
            symbol=symbol, 
            side=direction, 
            margin_usd=margin_usd, 
            leverage=leverage
        )

    def close_position(self, position_id: str):
        return self.mp.close(position_id)

    def get_account_info(self) -> dict:
        return self.mp.account()