import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

st.title("📈 Elite Technical Intelligence Engine")

st.caption("Institutional Multi-Timeframe Analytics")

# ------------------------------------------
# STOCK UNIVERSE
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
# DAILY DATA
# ------------------------------------------

daily_df = yf.download(
    symbol,
    period="1y",
    interval="1d",
    progress=False
)

daily_close = daily_df['Close'].squeeze()

# ------------------------------------------
# WEEKLY DATA
# ------------------------------------------

weekly_df = yf.download(
    symbol,
    period="3y",
    interval="1wk",
    progress=False
)

weekly_close = weekly_df['Close'].squeeze()

# ------------------------------------------
# DAILY INDICATORS
# ------------------------------------------

daily_ema20 = EMAIndicator(
    close=daily_close,
    window=20
).ema_indicator()

daily_ema50 = EMAIndicator(
    close=daily_close,
    window=50
).ema_indicator()

daily_rsi = RSIIndicator(
    close=daily_close
).rsi()

# ------------------------------------------
# WEEKLY INDICATORS
# ------------------------------------------

weekly_ema20 = EMAIndicator(
    close=weekly_close,
    window=20
).ema_indicator()

weekly_ema50 = EMAIndicator(
    close=weekly_close,
    window=50
).ema_indicator()

weekly_rsi = RSIIndicator(
    close=weekly_close
).rsi()

# ------------------------------------------
# ATR VOLATILITY
# ------------------------------------------

atr = AverageTrueRange(
    high=daily_df['High'].squeeze(),
    low=daily_df['Low'].squeeze(),
    close=daily_close
).average_true_range()

current_price = round(
    float(daily_close.iloc[-1]),
    2
)

# ------------------------------------------
# SCORING ENGINE
# ------------------------------------------

score = 0
signals = []

# DAILY TREND

if daily_ema20.iloc[-1] > daily_ema50.iloc[-1]:
    score += 20
    signals.append("Daily bullish trend")

# WEEKLY TREND

if weekly_ema20.iloc[-1] > weekly_ema50.iloc[-1]:
    score += 25
    signals.append("Weekly bullish structure")

# DAILY MOMENTUM

if 50 < daily_rsi.iloc[-1] < 70:
    score += 15
    signals.append("Healthy daily RSI")

# WEEKLY MOMENTUM

if weekly_rsi.iloc[-1] > 50:
    score += 15
    signals.append("Positive weekly momentum")

# PRICE POSITION

if current_price > daily_ema50.iloc[-1]:
    score += 15
    signals.append("Above medium-term trend")

# VOLATILITY QUALITY

atr_pct = (
    atr.iloc[-1] / current_price
) * 100

if atr_pct < 3:
    score += 10
    signals.append("Controlled volatility")

# ------------------------------------------
# CLASSIFICATION
# ------------------------------------------

if score >= 80:
    classification = "🟢 Elite Bullish Structure"
    risk = "Moderate"

elif score >= 60:
    classification = "🟡 Strong Technical Structure"
    risk = "Moderate"

elif score >= 40:
    classification = "🟠 Mixed Structure"
    risk = "Moderate-High"

else:
    classification = "🔴 Weak Technical Structure"
    risk = "High"

# ------------------------------------------
# MAIN METRICS
# ------------------------------------------

st.subheader(f"📊 {selected_stock} Technical Intelligence")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"₹{current_price}"
)

col2.metric(
    "Technical Score",
    f"{score}/100"
)

col3.metric(
    "Risk Level",
    risk
)

col4.metric(
    "Classification",
    classification
)

# ------------------------------------------
# TIMEFRAME TABLE
# ------------------------------------------

timeframe_df = pd.DataFrame({

    "Metric": [
        "Daily RSI",
        "Weekly RSI",
        "ATR Volatility %",
        "Daily EMA Trend",
        "Weekly EMA Trend"
    ],

    "Value": [
        round(float(daily_rsi.iloc[-1]),2),
        round(float(weekly_rsi.iloc[-1]),2),
        round(float(atr_pct),2),
        "Bullish" if daily_ema20.iloc[-1] > daily_ema50.iloc[-1] else "Bearish",
        "Bullish" if weekly_ema20.iloc[-1] > weekly_ema50.iloc[-1] else "Bearish"
    ]
})

st.subheader("⏳ Multi-Timeframe Analysis")

st.dataframe(
    timeframe_df,
    use_container_width=True
)

# ------------------------------------------
# SIGNALS
# ------------------------------------------

st.subheader("⚡ Technical Signals")

for signal in signals:
    st.success(signal)

# ------------------------------------------
# TRADE LEVELS
# ------------------------------------------

entry = current_price

stop_loss = round(
    current_price - (atr.iloc[-1] * 1.5),
    2
)

target1 = round(
    current_price + (atr.iloc[-1] * 2),
    2
)

target2 = round(
    current_price + (atr.iloc[-1] * 4),
    2
)

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

st.subheader("🎯 ATR-Based Institutional Trade Setup")

st.dataframe(
    trade_df,
    use_container_width=True
)

# ------------------------------------------
# AI COMMENTARY
# ------------------------------------------

st.divider()

st.subheader("🧠 AI Technical Commentary")

commentary = f'''
{selected_stock} currently exhibits a
technical score of {score}/100.

The dashboard evaluates:
• daily structure
• weekly structure
• momentum persistence
• volatility behavior
• trend alignment

Current classification:
{classification}

Risk profile:
{risk}

Higher timeframe alignment generally improves
trend persistence and reduces noise.

ATR-based positioning helps adapt risk
management to prevailing volatility.
'''

st.info(commentary)

# ------------------------------------------
# FOOTER
# ------------------------------------------

st.divider()

st.caption(
    "Elite multi-timeframe analytics"
)
