import yfinance as yf
import requests
from datetime import datetime
import time
import os

# ====== ENV VARIABLES ======
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# ====== FUNCTION TO GET TREND ======
def get_trend(ticker):
    try:
        data = yf.download(ticker, period="5d", interval="1d", progress=False)

        if data is None or len(data) < 2:
            return "SIDEWAYS"

        close_prices = data["Close"]

        last = float(close_prices.iloc[-1])
        prev = float(close_prices.iloc[-2])

        if last > prev:
            return "UP"
        elif last < prev:
            return "DOWN"
        else:
            return "SIDEWAYS"

    except:
        return "SIDEWAYS"

# ====== MAIN BOT FUNCTION ======
def run_bot():
    dxy = get_trend("DX-Y.NYB")
    gold = get_trend("GC=F")
    oil = get_trend("CL=F")
    nifty = get_trend("^NSEI")
    btc = get_trend("BTC-USD")
    yields = get_trend("^TNX")

    score = 0
    score += 1 if dxy == "DOWN" else -1
    score += 1 if gold == "DOWN" else -1
    score += 1 if yields == "UP" else -1
    score += 1 if oil == "UP" else -1
    score += 1 if nifty == "UP" else -1
    score += 1 if btc == "UP" else -1

    if score >= 5:
        signal = "🔥 STRONG RISK-ON"
        action = "BUY NIFTY, STOCKS, BTC\nAVOID GOLD"
    elif score >= 3:
        signal = "🟢 RISK-ON"
        action = "BUY ON DIPS\nPARTIAL POSITIONS"
    elif score >= 1:
        signal = "🟡 WEAK BULL"
        action = "LIGHT TRADING ONLY"
    elif score <= -5:
        signal = "💣 PANIC"
        action = "EXIT ALL\nBUY GOLD"
    elif score <= -3:
        signal = "🔴 RISK-OFF"
        action = "SELL EQUITIES\nBUY GOLD"
    else:
        signal = "⚪ NEUTRAL"
        action = "WAIT / NO TRADE"

    confidence = round((abs(score) / 6) * 100, 1)

    msg = f"""
📊 DSM-7 DAILY SIGNAL

Date: {datetime.now().strftime('%d %b %Y %H:%M')}

Score: {score}
Confidence: {confidence}%

Signal: {signal}

DXY: {dxy}
Gold: {gold}
Yields: {yields}
Oil: {oil}
NIFTY: {nifty}
BTC: {btc}

📈 ACTION:
{action}
"""

    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        print("✅ Signal sent!")
    except:
        print("❌ Error sending")

# ====== LOOP (AUTO RUN) ======
while True:
    run_bot()
    print("⏳ Waiting 24 hours...")
    time.sleep(86400)  # 24 hours
