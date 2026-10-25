import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
MARGINPAD_API_KEY = os.getenv("MARGINPAD_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

# Pengaturan Trading
SYMBOL = "BTC"
INITIAL_BALANCE = 1000.0    # Saldo virtual awal
LEVERAGE = 10               # Leverage untuk futures

# Manajemen Risiko (Sesuai blueprint)
RISK_PER_TRADE_PCT = 0.05   # 5% dari modal per trade (50 USD)
DAILY_LOSS_LIMIT_PCT = 0.02 # 2% dari modal (20 USD)

LOOP_INTERVAL = 60          # Cek pasar tiap 60 detik