import streamlit as st
import pandas as pd
import time
import os
import plotly.express as px
from statsmodels.tsa.stattools import adfuller

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="Live Binance Quant Analytics Dashboard",
    layout="wide"
)

st.title("📊 Live Binance Quant Analytics Dashboard")

DATA_FILE = "data/ticks.csv"

# ----------------------------
# Sidebar Controls
# ----------------------------
st.sidebar.header("Controls")

refresh_rate = st.sidebar.slider(
    "Refresh (seconds)",
    min_value=1,
    max_value=5,
    value=1
)

z_window = st.sidebar.slider(
    "Z-score window",
    min_value=20,
    max_value=200,
    value=60
)

# ----------------------------
# Load Data
# ----------------------------
if not os.path.exists(DATA_FILE):
    st.warning("Waiting for data...")
    st.stop()

df = pd.read_csv(DATA_FILE)

df["time"] = pd.to_datetime(
    df["time"],
    format="mixed",
    errors="coerce"
)

df = df.dropna(subset=["time"])
df = df.sort_values("time")

# ----------------------------
# Split Symbols
# ----------------------------
btc = df[df["symbol"] == "BTCUSDT"]
eth = df[df["symbol"] == "ETHUSDT"]

if btc.empty or eth.empty:
    st.warning("Waiting for both BTC and ETH data...")
    st.stop()

# ----------------------------
# Resample to 1 Second
# ----------------------------
btc_1s = btc.set_index("time").resample("1S").last()["price"]
eth_1s = eth.set_index("time").resample("1S").last()["price"]

combined = pd.concat([btc_1s, eth_1s], axis=1)
combined.columns = ["BTC", "ETH"]
combined = combined.dropna()

# ----------------------------
# Spread & Z-Score
# ----------------------------
combined["spread"] = combined["BTC"] - combined["ETH"]
combined["mean"] = combined["spread"].rolling(z_window).mean()
combined["std"] = combined["spread"].rolling(z_window).std()
combined["zscore"] = (combined["spread"] - combined["mean"]) / combined["std"]

combined = combined.dropna()

# ----------------------------
# Layout
# ----------------------------
col1, col2 = st.columns(2)

# ----------------------------
# Spread Chart
# ----------------------------
with col1:
    st.subheader("📉 Spread (BTC − ETH)")
    spread_fig = px.line(
        combined,
        y="spread",
        labels={"spread": "Spread"}
    )
    st.plotly_chart(spread_fig, use_container_width=True)

# ----------------------------
# Z-Score Chart
# ----------------------------
with col2:
    st.subheader("📊 Z-Score")
    z_fig = px.line(
        combined,
        y="zscore",
        labels={"zscore": "Z-Score"}
    )
    z_fig.add_hline(y=2, line_dash="dash", line_color="red")
    z_fig.add_hline(y=-2, line_dash="dash", line_color="green")
    st.plotly_chart(z_fig, use_container_width=True)

# ----------------------------
# Trading Signal
# ----------------------------
latest_z = combined["zscore"].iloc[-1]

st.subheader("🚨 Trading Signal")

if latest_z > 2:
    st.error(f"Z = {latest_z:.2f} → SELL BTC / BUY ETH")
elif latest_z < -2:
    st.success(f"Z = {latest_z:.2f} → BUY BTC / SELL ETH")
else:
    st.info(f"Z = {latest_z:.2f} → No trade")

# ----------------------------
# ADF TEST (Stationarity Check)
# ----------------------------
st.subheader("🧪 ADF Stationarity Test (Spread)")

spread_series = combined["spread"].dropna()

adf_result = adfuller(spread_series)

adf_stat = adf_result[0]
p_value = adf_result[1]
crit_values = adf_result[4]

col_a, col_b, col_c = st.columns(3)

col_a.metric("ADF Statistic", f"{adf_stat:.4f}")
col_b.metric("p-value", f"{p_value:.4f}")
col_c.metric("5% Critical Value", f"{crit_values['5%']:.4f}")

if p_value < 0.05:
    st.success("✅ Spread is stationary (mean-reverting)")
else:
    st.error("❌ Spread is NOT stationary")

# ----------------------------
# Controlled Refresh (Stable)
# ----------------------------
time.sleep(refresh_rate)
st.query_params["refresh"] = str(int(time.time()))
