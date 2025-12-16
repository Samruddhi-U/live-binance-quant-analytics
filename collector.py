import websocket
import json
import csv
from datetime import datetime
import os
import ssl
import sys

# ----------------------------
# CONFIG
# ----------------------------
SYMBOL = sys.argv[1] if len(sys.argv) > 1 else "btcusdt"
DATA_FILE = "data/ticks.csv"

if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "symbol", "price", "qty"])

def on_message(ws, message):
    msg = json.loads(message)
    if msg.get("e") == "trade":
        with open(DATA_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.fromtimestamp(msg["T"] / 1000),
                msg["s"],
                msg["p"],
                msg["q"]
            ])

def on_open(ws):
    print(f"Connected to {SYMBOL.upper()}")

def on_error(ws, error):
    print("WebSocket error:", error)

def on_close(ws, code, msg):
    print("WebSocket closed")

if __name__ == "__main__":
    socket_url = f"wss://fstream.binance.com/ws/{SYMBOL}@trade"
    ws = websocket.WebSocketApp(
        socket_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
