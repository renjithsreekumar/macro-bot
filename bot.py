import requests
import os
import time
from datetime import datetime
import pytz

# =========================
# ENV VARIABLES
# =========================
BOT_TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# =========================
# TELEGRAM FUNCTION
# =========================
def send_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

        payload = {
            "chat_id": CHAT_ID,
            "text": message
        }

        response = requests.post(url, data=payload)

        print("📡 Telegram Status:", response.status_code)
        print("📩 Telegram Response:", response.text)

    except Exception as e:
        print("❌ Telegram Error:", e)


# =========================
# SIGNAL LOGIC (DUMMY NOW)
# Replace with your SMA logic later
# =========================
def generate_signal():
    # You can plug your SMA / Trading logic here

    return {
        "symbol": "NIFTY",
        "action": "BUY",
        "price": "Market Price",
        "strategy": "SMA 8/20 Crossover"
    }


# =========================
# MAIN BOT LOOP
# =========================
def run_bot():
    ist = pytz.timezone('Asia/Kolkata')

    while True:
        try:
            now = datetime.now(ist)

            print("⏰ Running at:", now)

            signal = generate_signal()

            message = f"""
📊 TRADE SIGNAL

📈 Stock: {signal['symbol']}
🟢 Action: {signal['action']}
💰 Price: {signal['price']}
📌 Strategy: {signal['strategy']}

🕒 Time: {now.strftime('%Y-%m-%d %H:%M:%S')}
"""

            send_telegram(message)

        except Exception as e:
            print("❌ Bot Error:", e)

        # Wait 24 hours
        print("⏳ Sleeping for 24 hours...\n")
        time.sleep(86400)


# =========================
# START BOT
# =========================
if __name__ == "__main__":
    print("🚀 Bot Started...")
    run_bot()
