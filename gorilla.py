import ccxt, pandas as pd
import urllib.request as u

ex = ccxt.kraken()
b = ex.fetch_ohlcv('BTC/USD','1h',limit=50)
df = pd.DataFrame(b)
c = df[4]
m = c.rolling(20).mean()
s = c.rolling(20).std()

price = c.iloc[-1]
z = round((price - m.iloc[-1]) / s.iloc[-1], 2)
pz = round((c.iloc[-2] - m.iloc[-2]) / s.iloc[-2], 2)

hook = (pz < -2.0) and (z >= -2.0)
status = "[BUY HOOK ACTIVE!]" if hook else "[STANDBY]"
msg = f"GORILLA: BUY BTC ${price} | Z:{z}"

if hook:
    u.urlopen("https://ntfy.sh/cozie-btc-alerts", msg.encode())

print("RUN SUCCESSFUL | BTC:", price, "| Z:", z, "| STATUS:", status)
