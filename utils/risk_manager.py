from config import INITIAL_BALANCE, RISK_PER_TRADE_PCT, DAILY_LOSS_LIMIT_PCT

class RiskManager:
    def __init__(self):
        self.trade_size_usd = INITIAL_BALANCE * RISK_PER_TRADE_PCT
        self.max_daily_loss = INITIAL_BALANCE * DAILY_LOSS_LIMIT_PCT
        self.current_loss = 0.0
        self.is_hibernating = False

    def record_loss(self, loss_amount: float):
        if loss_amount > 0:
            self.current_loss += loss_amount
            print(f"⚠️ [RISK] Rugi terdeteksi: ${loss_amount:.2f}. Total rugi hari ini: ${self.current_loss:.2f}")
            
            if self.current_loss >= self.max_daily_loss:
                self.is_hibernating = True
                print(f"🛑 [RISK] Batas rugi harian ${self.max_daily_loss} tercapai! Bot berhenti trading.")

    def can_trade(self) -> bool:
        return not self.is_hibernating

    def get_trade_size(self) -> float:
        return self.trade_size_usd