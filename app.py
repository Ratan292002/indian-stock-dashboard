import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.set_page_config(
    page_title="Ratan Quant Terminal",
    layout="wide"
)

# -----------------------------
# HEADER
# -----------------------------

st.title("🌍 Ratan Quant Terminal")
st.caption("Global Market Intelligence Dashboard")

# -----------------------------
# GLOBAL MARKET WATCH
# -----------------------------

st.subheader("🌎 Global Markets")

indices = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
    "NIKKEI": "^N225",
    "HANG SENG": "^HSI",
    "CRUDE OIL": "CL=F",
    "GOLD": "GC=F",
    "USD/INR": "INR=X"
}

market_cols = st.columns(5)

i = 0

for name, ticker in indices.items():
    try:
        data = yf.download(ticker, period="5d", progress=False)

        latest = float(data['Close'].iloc[-1])
        prev = float(data['Close'].iloc[-2])

        change = latest - prev
        pct = (change / prev) * 100

        market_cols[i % 5].metric(
            name,
            round(latest, 2),
            f"{round(pct,2)}%"
        )

        i += 1

    except:
        pass

st.divider()

# -----------------------------
# STOCK SELECTOR
# -----------------------------

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
    "📌 Select Stock",
    list(stocks.keys())
)

symbol = stocks[selected_stock]

# -----------------------------
# LOAD DATA
# -----------------------------

@st.cache_data(ttl=300)
def load_data(symbol):
    df = yf.download(symbol, period="1y", progress=False)
    return df

df = load_data(symbol)

close = df['Close'].squeeze()

# -----------------------------
# TECHNICAL INDICATORS
# -----------------------------

ema20 = EMAIndicator(close=close, window=20).ema_indicator()
ema50 = EMAIndicator(close=close, window=50).ema_indicator()

rsi = RSIIndicator(close=close, window=14).rsi()

current_price = round(float(close.iloc[-1]), 2)

# -----------------------------
# AI SCORE ENGINE
# -----------------------------

score = 0
signals = []

if ema20.iloc[-1] > ema50.iloc[-1]:
    score += 35
    signals.append("Bullish EMA Trend")

if current_price > ema50.iloc[-1]:
    score += 35
    signals.append("Price Above EMA50")

if 50 < rsi.iloc[-1] < 70:
    score += 30
    signals.append("Healthy RSI Momentum")

# -----------------------------
# RECOMMENDATION ENGINE
# -----------------------------

if score >= 80:
    recommendation = "🟢 STRONG BUY"
elif score >= 60:
    recommendation = "🟡 BUY"
elif score >= 40:
    recommendation = "🟠 WATCHLIST"
else:
    recommendation = "🔴 AVOID"

# -----------------------------
# MAIN METRICS
# -----------------------------

st.subheader(f"📊 {selected_stock} Analysis")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Current Price", f"₹{current_price}")
col2.metric("AI Score", f"{score}/100")
col3.metric("RSI", round(float(rsi.iloc[-1]),2))
col4.metric("Recommendation", recommendation)

# -----------------------------
# TRADE SETUP
# -----------------------------

entry = current_price
stop_loss = round(current_price * 0.95, 2)
target1 = round(current_price * 1.08, 2)
target2 = round(current_price * 1.15, 2)

st.subheader("🎯 Trade Setup")

trade_df = pd.DataFrame({
    "Parameter": ["Entry", "Stop Loss", "Target 1", "Target 2"],
    "Value": [entry, stop_loss, target1, target2]
})

st.dataframe(trade_df, use_container_width=True)

# -----------------------------
# SIGNALS
# -----------------------------

st.subheader("🧠 AI Signals")

for s in signals:
    st.success(s)

# -----------------------------
# CHART
# -----------------------------

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
    height=600,
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# DAILY AI PICKS
# -----------------------------

st.subheader("🔥 Daily AI Picks")

recommendations = []

for stock_name, stock_symbol in stocks.items():

    try:
        temp_df = yf.download(stock_symbol, period="6mo", progress=False)

        temp_close = temp_df['Close'].squeeze()

        temp_ema20 = EMAIndicator(close=temp_close, window=20).ema_indicator()
        temp_ema50 = EMAIndicator(close=temp_close, window=50).ema_indicator()

        temp_score = 0

        if temp_ema20.iloc[-1] > temp_ema50.iloc[-1]:
            temp_score += 50

        if temp_close.iloc[-1] > temp_ema50.iloc[-1]:
            temp_score += 50

        recommendations.append({
            "Stock": stock_name,
            "Price": round(float(temp_close.iloc[-1]),2),
            "Score": temp_score
        })

    except:
        pass

rec_df = pd.DataFrame(recommendations)

if not rec_df.empty:
    rec_df = rec_df.sort_values(by="Score", ascending=False)
    st.dataframe(rec_df, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------

st.divider()

st.caption("Institutional-style educational dashboard • Not investment advice")
