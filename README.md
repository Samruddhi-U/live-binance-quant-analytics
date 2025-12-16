# Live Binance Quant Analytics Dashboard

## Overview
This project is a real-time quantitative analytics application developed as part of a Quant Developer assignment.  
It ingests live cryptocurrency trade data from the Binance WebSocket API and performs pair-trading analysis using statistical methods.

The application focuses on BTC–ETH pair trading and demonstrates real-time data ingestion, analytics, validation, and alert generation.

---

## Features
- Real-time WebSocket data ingestion (BTCUSDT, ETHUSDT)
- Tick-level data storage
- 1-second price resampling
- Spread calculation (BTC − ETH)
- Rolling Z-score computation
- Augmented Dickey-Fuller (ADF) stationarity test
- Live trading signal alerts
- Interactive Streamlit dashboard

---

## Tech Stack
- Python
- Binance Futures WebSocket API
- Pandas & NumPy
- Statsmodels 
- Plotly
- Streamlit

---

## Architecture
The system follows a modular real-time analytics pipeline:

1. Binance WebSocket API provides live trade data
2. Python collectors ingest BTC and ETH tick data
3. Data is stored locally in CSV format
4. Analytics engine computes spread, Z-score, and ADF test
5. Streamlit dashboard visualizes analytics and generates alerts

Architecture diagrams included in this repository:
- architecture.drawio
- architecture.png

---

## Setup & Installation

### Prerequisites
- Python 3.9+
- pip

### Install dependencies
```bash
pip install -r requirements.txt
How to Run the Application
Step 1: Start data collectors (in two separate terminals)

python collector.py btcusdt
python collector.py ethusdt
These collectors stream live trade data from Binance.

Step 2: Run the dashboard

streamlit run app.py
The dashboard will open automatically in your browser.

Methodology & Analytics
Pair Selection
BTC and ETH were chosen due to their high liquidity and strong correlation, making them suitable for pair-trading strategies.

Spread Calculation

Spread = BTC Price − ETH Price
Z-Score
The spread is normalized using a rolling Z-score:

Z = (Spread − Rolling Mean) / Rolling Standard Deviation
ADF Test (Stationarity Check)
The Augmented Dickey-Fuller (ADF) test is applied to the spread to validate stationarity, a core assumption of pair trading.

p-value < 0.05 indicates the spread is stationary (mean-reverting)

Alerts
Trading signals are generated based on Z-score thresholds:

Z > +threshold → SELL BTC / BUY ETH

Z < −threshold → BUY BTC / SELL ETH

Otherwise → No trade

## Transparency in ChatGPT Usage

ChatGPT served as a support tool for learning and development throughout this project.
It assisted in comprehending Binance WebSocket APIs, troubleshooting Streamlit and Git problems, and organizing the analytics framework (spread, Z-score, and ADF test).
The author carried out the final system design, implementation, testing, and validation.
ChatGPT was utilized solely for advice and problem-solving, rather than for automated creation of solutions.
Example prompts contained:

"How can one calculate the rolling Z-score for pair trading?"
"How to execute the ADF test on a time series using Python?"
- "What is the best way to organize a Streamlit dashboard for real-time data?"

## Architecture

The following diagram illustrates the high-level architecture of the system, including data ingestion, storage, analytics, and alert flow.

![Architecture Diagram](Architecture.drawio.png)


## Author
Samruddhi Ubhad  
B.Tech Computer Engineering Student  
GitHub: https://github.com/Samruddhi-U
