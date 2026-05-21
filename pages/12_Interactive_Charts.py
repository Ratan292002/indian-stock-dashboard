import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from ta.trend import EMAIndicator

st.title("📉 Interactive Trading Charts")

st.caption("Professional Candlestick Analytics")

# ------------------------------------------
# STOCKS
# ------------------------------------------

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

# ------------------------------------------
# TIMEFRAME
# ------------------------------------------

timeframe = st.selectbox(
    "Select Timeframe",
    ["1mo", "3mo", "6mo", "1y"]
)

# ------------------------------------------
# DATA
# ------------------------------------------

df = yf.download(
    symbol,
    period=timeframe,
    progress=False
)

close = df['Close'].squeeze()

# ------------------------------------------
# EMA
# ------------------------------------------

ema20 = EMAIndicator(
    close=close,
    window=20
).ema_indicator()

ema50 = EMAIndicator(
    close=close,
    window=50
).ema_indicator()

# ------------------------------------------
# CANDLESTICK CHART
# ------------------------------------------

fig = go.Figure()

fig.add_trace(go.Candlestick(

    x=df.index,

    open=df['Open'],

    high=df['High'],

    low=df['Low'],

    close=df['Close'],

    name='Candles'
))

# ------------------------------------------
# EMA OVERLAYS
# ------------------------------------------

fig.add_trace(go.Scatter(

    x=df.index,

    y=ema20,

    line=dict(width=1),

    name='EMA20'
))

fig.add_trace(go.Scatter(

    x=df.index,

    y=ema50,

    line=dict(width=1),

    name='EMA50'
))

# ------------------------------------------
# VOLUME
# ------------------------------------------

fig.add_trace(go.Bar(

    x=df.index,

    y=df['Volume'],

    name='Volume',

    opacity=0.3
))

# ------------------------------------------
# LAYOUT
# ------------------------------------------

fig.update_layout(

    template="plotly_dark",

    height=800,

    xaxis_rangeslider_visible=False,

    title=f"{selected_stock} Interactive Chart",

    hovermode="x unified"
)

# ------------------------------------------
# DISPLAY
# ------------------------------------------

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------------------------
# QUICK INSIGHTS
# ------------------------------------------

st.subheader("🧠 Quick Technical Insights")

latest_close = float(close.iloc[-1])

if latest_close > ema20.iloc[-1]:
    short_term = "🟢 Bullish"
else:
    short_term = "🔴 Bearish"

if ema20.iloc[-1] > ema50.iloc[-1]:
    medium_term = "🟢 Bullish"
else:
    medium_term = "🔴 Bearish"

col1, col2 = st.columns(2)

col1.metric(
    "Short-Term Structure",
    short_term
)

col2.metric(
    "Medium-Term Structure",
    medium_term
)

# ------------------------------------------
# AI INTERPRETATION
# ------------------------------------------

st.divider()

st.subheader("🤖 Chart Interpretation")

st.info(
    '''
    The candlestick engine allows:
    
    • visual trend analysis
    
    • breakout inspection
    
    • support/resistance observation
    
    • volume participation analysis
    
    • multi-timeframe evaluation

    EMA overlays help identify:
    
    • trend persistence
    
    • structure quality
    
    • directional bias
    '''
)

# ------------------------------------------
# FOOTER
# ------------------------------------------

st.divider()

st.caption(
    "Professional interactive charting system"
)
