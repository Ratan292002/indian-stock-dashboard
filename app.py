import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.set_page_config(page_title="Indian Stock Intelligence Dashboard", layout="wide")

st.title("📈 Indian Stock Intelligence Dashboard")

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

selected_stock = st.sidebar.selectbox(
    "Select Stock",
    list(stocks.keys())
)

symbol = stocks[selected_stock]

@st.cache_data(ttl=300)
def load_data(symbol):
    data = yf.download(symbol, period="6mo")
    return data

df = load_data(symbol)
close = df['Close'].squeeze()

ema20 = EMAIndicator(close=close, window=20).ema_indicator()
ema50 = EMAIndicator(close=close, window=50).ema_indicator()

rsi = RSIIndicator(close=close).rsi()

current_price = round(float(close.iloc[-1]), 2)

score = 0
signals = []

if ema20.iloc[-1] > ema50.iloc[-1]:
    score += 30
    signals.append("Bullish EMA Crossover")

if 50 < rsi.iloc[-1] < 70:
    score += 30
    signals.append("Healthy RSI Momentum")

if current_price > ema50.iloc[-1]:
    score += 40
    signals.append("Price Above EMA50")

if score >= 80:
    recommendation = "STRONG BUY"
elif score >= 60:
    recommendation = "BUY"
elif score >= 40:
    recommendation = "WATCHLIST"
else:
    recommendation = "AVOID"

col1, col2, col3 = st.columns(3)

col1.metric("Current Price", f"₹{current_price}")
col2.metric("AI Score", f"{score}/100")
col3.metric("Recommendation", recommendation)

st.subheader("Detected Signals")

for s in signals:
    st.success(s)

entry = current_price
stop_loss = round(current_price * 0.95, 2)
target = round(current_price * 1.10, 2)

trade_df = pd.DataFrame({
    "Parameter": ["Entry", "Stop Loss", "Target"],
    "Value": [entry, stop_loss, target]
})

st.subheader("Trade Setup")
st.dataframe(trade_df, use_container_width=True)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=df.index,
    y=close,
    mode='lines',
    name='Close Price'
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=ema20,
    mode='lines',
    name='EMA20'
))

fig.add_trace(go.Scatter(
    x=df.index,
    y=ema50,
    mode='lines',
    name='EMA50'
))

fig.update_layout(
    title=f"{selected_stock} Price Chart",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Daily AI Stock Picks")

recommendations = []

for stock_name, stock_symbol in stocks.items():
    try:
        temp_df = yf.download(stock_symbol, period="3mo")

        temp_close = temp_df['Close']

        temp_ema20 = EMAIndicator(close=temp_close, window=20).ema_indicator()
        temp_ema50 = EMAIndicator(close=temp_close, window=50).ema_indicator()

        temp_score = 0

        if temp_ema20.iloc[-1] > temp_ema50.iloc[-1]:
            temp_score += 50

        if temp_close.iloc[-1] > temp_ema50.iloc[-1]:
            temp_score += 50

        recommendations.append({
            "Stock": stock_name,
            "Price": round(temp_close.iloc[-1], 2),
            "Score": temp_score
        })

    except:
        pass

rec_df = pd.DataFrame(recommendations)

if not rec_df.empty:
    rec_df = rec_df.sort_values(by="Score", ascending=False)
    st.dataframe(rec_df, use_container_width=True)

st.caption("Educational dashboard only. Not investment advice.")
