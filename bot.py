import yfinance as yf
import requests
from datetime import datetime

# ====== YOUR CONFIG ======
TOKEN = "8797176582:AAFbS1N-bv0xazsBOTgQqPrfVX1BEmtw8xU"
CHAT_ID = "1465180523"

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

# ====== FETCH DATA ======
dxy = get_trend("DX-Y.NYB")
gold = get_trend("GC=F")
oil = get_trend("CL=F")
nifty = get_trend("^NSEI")
btc = get_trend("BTC-USD")
yields = get_trend("^TNX")

# ====== SCORING ======
score = 0

score += 1 if dxy == "DOWN" else -1
score += 1 if gold == "DOWN" else -1
score += 1 if yields == "UP" else -1
score += 1 if oil == "UP" else -1
score += 1 if nifty == "UP" else -1
score += 1 if btc == "UP" else -1

# ====== SIGNAL ======
if score >= 5:
    signal = "🔥 STRONG RISK-ON"
elif score >= 3:
    signal = "🟢 RISK-ON"
elif score >= 1:
    signal = "🟡 WEAK BULL"
elif score <= -5:
    signal = "💣 PANIC"
elif score <= -3:
    signal = "🔴 RISK-OFF"
else:
    signal = "⚪ NEUTRAL"

# ====== ACTION ======
if score >= 5:
    action = "BUY NIFTY, STOCKS, BTC\nAVOID GOLD"
elif score >= 3:
    action = "BUY ON DIPS\nPARTIAL POSITIONS"
elif score >= 1:
    action = "LIGHT TRADING ONLY"
elif score <= -3:
    action = "SELL EQUITIES\nBUY GOLD"
else:
    action = "WAIT / NO TRADE"

# ====== CONFIDENCE ======
confidence = round((abs(score) / 6) * 100, 1)

# ====== MESSAGE ======
msg = f"""
📊 DSM-7 DAILY SIGNAL

Date: {datetime.now().strftime('%d %b %Y')}

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

# ====== SEND TELEGRAM ======
try:
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    print("✅ Signal sent successfully!")
except:
    print("❌ Error sending message")
    
