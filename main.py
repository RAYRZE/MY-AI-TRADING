import time
from config import SYMBOL, LEVERAGE, LOOP_INTERVAL
from exchanges.marginpad_api import MarginPadAdapter
from utils.risk_manager import RiskManager
from utils.logger import init_logger, log_trade
from brain.analyst import get_signal
from brain.personality import get_emotional_comment

def main():
    # Inisialisasi semua modul
    trader = MarginPadAdapter()
    risk = RiskManager()
    init_logger()

    print("🤖 [START] Bot AI MarginPad aktif. Mode: Futures (Long/Short).")
    print(f"💼 Modal Awal: ${risk.max_daily_loss / 0.02:.2f} | Trade Size: ${risk.get_trade_size()}")

    active_position_id = None
    entry_price = 0.0

    while True:
        try:
            price = trader.get_price(SYMBOL)
            print(f"\n📊 Harga {SYMBOL}: ${price}")

            # Kalau bot lagi hibernasi (rugi harian tercapai), skip
            if not risk.can_trade():
                print("😴 Bot sedang hibernasi (batas rugi tercapai).")
                time.sleep(LOOP_INTERVAL)
                continue

            # Cek apakah ada posisi terbuka
            account = trader.get_account_info()
            # (Logika MarginPad: kalau posisi terbuka, kita cek PnL-nya)
            
            if not active_position_id:
                # Belum ada posisi, minta sinyal ke AI
                signal = get_signal(price, SYMBOL)
                print(f"🧠 Sinyal AI: {signal}")

                if signal in ["LONG", "SHORT"]:
                    margin = risk.get_trade_size()
                    print(f"🚀 [EKSEKUSI] Buka {signal} sebesar ${margin} (Lev {LEVERAGE}x)")
                    
                    # Eksekusi ke MarginPad
                    pos = trader.open_position(SYMBOL, signal.lower(), margin, LEVERAGE)
                    active_position_id = pos.get("id", "dummy_id") 
                    entry_price = price
                    log_trade(price, signal, "OPEN", margin, 0, "Posisi dibuka")
                else:
                    print("⏸️ HOLD. Menunggu momen yang tepat.")
            
            else:
                # Kalau ada posisi, kita cek kondisi harga buat nutup posisi (simulasi)
                # Di bot beneran, ini diganti dengan Take Profit / Stop Loss
                pnl = (price - entry_price) if "LONG" in signal else (entry_price - price)
                
                # Simulasi: Tutup posisi kalau profit/loss udah 0.5%
                if abs(pnl) > (entry_price * 0.005): 
                    print(f"🔒 [EKSEKUSI] Tutup posisi. PnL: ${pnl:.2f}")
                    trader.close_position(active_position_id)
                    
                    # Catat kerugian buat Risk Manager
                    if pnl < 0:
                        risk.record_loss(abs(pnl))
                    
                    # Panggil Emosi
                    emosi = get_emotional_comment(pnl > 0, pnl)
                    print(emosi)
                    
                    log_trade(price, "CLOSE", "CLOSE", risk.get_trade_size(), pnl, emosi)
                    active_position_id = None

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(LOOP_INTERVAL)

if __name__ == "__main__":
    main()