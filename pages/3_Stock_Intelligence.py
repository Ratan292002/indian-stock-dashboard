import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.title("🧠 Advanced Stock Intelligence")

stocks = {
    "RELIANCE": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "INFY": "INFY.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "SBIN": "SBIN.NS",
    "LT": "LT.NS",
    "ITC": "ITC.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "POLYCAB": "POLYCAB.NS"
}

selected_stock = st.selectbox(
    "Select Stock",
    list(stocks.keys())
)

symbol = stocks[selected_stock]

df = yf.download(symbol, period="1y", progress=False)

close = df['Close'].squeeze()

info = yf.Ticker(symbol).info

# ---------------------------------
# TECHNICALS
# ---------------------------------

ema20 = EMAIndicator(close=close, window=20).ema_indicator()
ema50 = EMAIndicator(close=close, window=50).ema_indicator()

rsi = RSIIndicator(close=close).rsi()

current_price = round(float(close.iloc[-1]),2)

# ---------------------------------
# FUNDAMENTALS
# ---------------------------------

market_cap = info.get("marketCap", 0)
pe_ratio = info.get("trailingPE", 0)
pb_ratio = info.get("priceToBook", 0)
roe = info.get("returnOnEquity", 0)
debt_equity = info.get("debtToEquity", 0)

# ---------------------------------
# AI SCORING ENGINE
# ---------------------------------

score = 0
signals = []

# Trend
if ema20.iloc[-1] > ema50.iloc[-1]:
    score += 20
    signals.append("Bullish Trend Structure")

# RSI
if 50 < rsi.iloc[-1] < 70:
    score += 15
    signals.append("Healthy Momentum")

# Price Strength
if current_price > ema50.iloc[-1]:
    score += 15
    signals.append("Price Above Medium-Term Trend")

# PE
if pe_ratio != 0 and pe_ratio < 35:
    score += 15
    signals.append("Reasonable Valuation")

# PB
if pb_ratio != 0 and pb_ratio < 8:
    score += 10
    signals.append("Acceptable Price-to-Book")

# ROE
if roe != 0 and roe > 0.15:
    score += 15
    signals.append("Strong Return on Equity")

# Debt
if debt_equity != 0 and debt_equity < 100:
    score += 10
    signals.append("Controlled Debt Structure")

# ---------------------------------
# RECOMMENDATION ENGINE
# ---------------------------------

if score >= 80:
    recommendation = "🟢 High Conviction Buy"
    risk = "Medium"
elif score >= 60:
    recommendation = "🟡 Accumulation Candidate"
    risk = "Moderate"
elif score >= 40:
    recommendation = "🟠 Watchlist"
    risk = "Moderate-High"
else:
    recommendation = "🔴 Avoid"
    risk = "High"

# ---------------------------------
# MAIN METRICS
# ---------------------------------

st.subheader(f"📊 {selected_stock} Intelligence Report")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Price", f"₹{current_price}")
col2.metric("AI Conviction Score", f"{score}/100")
col3.metric("Risk Level", risk)
col4.metric("Recommendation", recommendation)

# ---------------------------------
# FUNDAMENTAL TABLE
# ---------------------------------

fund_df = pd.DataFrame({
    "Metric": [
        "Market Cap",
        "P/E Ratio",
        "P/B Ratio",
        "ROE",
        "Debt/Equity"
    ],
    "Value": [
        market_cap,
        pe_ratio,
        pb_ratio,
        roe,
        debt_equity
    ]
})

st.subheader("🏛 Fundamental Analysis")

st.dataframe(
    fund_df,
    use_container_width=True
)

# ---------------------------------
# AI COMMENTARY
# ---------------------------------

st.subheader("🤖 AI Commentary")

commentary = f'''
{selected_stock} currently shows a conviction score of {score}/100.

The stock demonstrates:

• Trend quality based on EMA structure

• Momentum analysis through RSI positioning

• Fundamental balance via valuation metrics

• Capital efficiency through ROE

• Financial stability using debt analysis

Current risk profile is classified as {risk}.

Recommendation category:
{recommendation}
'''

st.info(commentary)

# ---------------------------------
# SIGNALS
# ---------------------------------

st.subheader("⚡ Detected Signals")

for s in signals:
    st.success(s)

# ---------------------------------
# TRADE SETUP
# ---------------------------------

entry = current_price
stop_loss = round(current_price * 0.94,2)
target1 = round(current_price * 1.10,2)
target2 = round(current_price * 1.18,2)

trade_df = pd.DataFrame({
    "Parameter": [
        "Entry",
        "Stop Loss",
        "Target 1",
        "Target 2"
    ],
    "Value": [
        entry,
        stop_loss,
        target1,
        target2
    ]
})

st.subheader("🎯 Institutional Trade Setup")

st.dataframe(
    trade_df,
    use_container_width=True
)

# ---------------------------------
# FOOTER
# ---------------------------------

st.divider()

st.caption(
    "Institutional-style educational analytics • Not investment advice"
)
