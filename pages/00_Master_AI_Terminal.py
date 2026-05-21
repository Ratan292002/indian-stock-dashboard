import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from ta.trend import EMAIndicator, MACD
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Master AI Terminal",
    layout="wide"
)

# ----------------------------------------------------
# LOGIN
# ----------------------------------------------------

USERNAME = "ratan"
PASSWORD = "12345"

st.sidebar.title("🔐 Secure Access")

username = st.sidebar.text_input("Username")
password = st.sidebar.text_input(
    "Password",
    type="password"
)

if username != USERNAME or password != PASSWORD:

    st.warning("Please login")

    st.stop()

st.sidebar.success(f"Welcome {username}")

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.title("🌍 Global Watch")

indices = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
    "GOLD": "GC=F",
    "CRUDE OIL": "CL=F",
    "USD/INR": "INR=X"
}

for name, symbol in indices.items():

    try:

        data = yf.download(
            symbol,
            period="2d",
            progress=False
        )

        latest = round(
            data["Close"].iloc[-1],
            2
        )

        prev = round(
            data["Close"].iloc[-2],
            2
        )

        change = round(
            ((latest-prev)/prev)*100,
            2
        )

        st.sidebar.metric(
            name,
            latest,
            f"{change}%"
        )

    except:
        pass

# ----------------------------------------------------
# TITLE
# ----------------------------------------------------

st.title("🧠 MASTER AI MARKET TERMINAL")

st.caption(
    "Institutional-Grade Market Intelligence"
)

# ----------------------------------------------------
# STOCK SEARCH
# ----------------------------------------------------

st.subheader("🔎 Universal NSE Stock Search")

stock = st.text_input(
    "Enter NSE Symbol",
    value="RELIANCE"
)

symbol = stock.upper() + ".NS"

# ----------------------------------------------------
# DOWNLOAD DATA
# ----------------------------------------------------

try:

    df = yf.download(
        symbol,
        period="1y",
        interval="1d",
        progress=False
    )

    if df.empty:

        st.error("Invalid stock symbol")

        st.stop()

except:

    st.error("Unable to fetch data")

    st.stop()

# ----------------------------------------------------
# INDICATORS
# ----------------------------------------------------

df["EMA20"] = EMAIndicator(
    close=df["Close"],
    window=20
).ema_indicator()

df["EMA50"] = EMAIndicator(
    close=df["Close"],
    window=50
).ema_indicator()

df["RSI"] = RSIIndicator(
    close=df["Close"],
    window=14
).rsi()

macd = MACD(close=df["Close"])

df["MACD"] = macd.macd()
df["MACD_SIGNAL"] = macd.macd_signal()

atr = AverageTrueRange(
    high=df["High"],
    low=df["Low"],
    close=df["Close"]
)

df["ATR"] = atr.average_true_range()

# ----------------------------------------------------
# LATEST VALUES
# ----------------------------------------------------

latest_close = float(df["Close"].iloc[-1])
latest_ema20 = float(df["EMA20"].iloc[-1])
latest_ema50 = float(df["EMA50"].iloc[-1])
latest_rsi = float(df["RSI"].iloc[-1])
latest_macd = float(df["MACD"].iloc[-1])
latest_signal = float(df["MACD_SIGNAL"].iloc[-1])
latest_atr = float(df["ATR"].iloc[-1])

# ----------------------------------------------------
# AI SCORING ENGINE
# ----------------------------------------------------

score = 0
signals = []

# EMA Trend

if latest_close > latest_ema20:
    score += 15
    signals.append("Above EMA20")

if latest_close > latest_ema50:
    score += 15
    signals.append("Above EMA50")

# RSI

if latest_rsi > 60:
    score += 15
    signals.append("Strong RSI")

elif latest_rsi > 50:
    score += 10
    signals.append("Positive RSI")

# MACD

if latest_macd > latest_signal:
    score += 20
    signals.append("Bullish MACD")

# Volume

avg_volume = df["Volume"].tail(20).mean()
latest_volume = df["Volume"].iloc[-1]

if latest_volume > avg_volume:
    score += 15
    signals.append("Volume Expansion")

# Momentum

returns_30 = (
    latest_close /
    df["Close"].iloc[-30]
) - 1

if returns_30 > 0.08:
    score += 20
    signals.append("Strong Momentum")

# ----------------------------------------------------
# RECOMMENDATION ENGINE
# ----------------------------------------------------

if score >= 75:

    recommendation = "🟢 STRONG BUY"

elif score >= 55:

    recommendation = "🟡 BUY"

elif score >= 40:

    recommendation = "🟠 HOLD"

else:

    recommendation = "🔴 AVOID"

# ----------------------------------------------------
# TARGET + STOP LOSS
# ----------------------------------------------------

target = round(
    latest_close + (latest_atr * 2),
    2
)

stop_loss = round(
    latest_close - (latest_atr * 1.5),
    2
)

risk_reward = round(
    (target-latest_close) /
    (latest_close-stop_loss),
    2
)

# ----------------------------------------------------
# TOP METRICS
# ----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Current Price",
    f"₹{round(latest_close,2)}"
)

col2.metric(
    "AI Score",
    f"{score}/100"
)

col3.metric(
    "Recommendation",
    recommendation
)

col4.metric(
    "RSI",
    round(latest_rsi,2)
)

# ----------------------------------------------------
# TARGET SECTION
# ----------------------------------------------------

st.subheader("🎯 Institutional Trade Setup")

c1, c2, c3 = st.columns(3)

c1.success(f"Target: ₹{target}")
c2.error(f"Stop Loss: ₹{stop_loss}")
c3.info(f"Risk/Reward: {risk_reward}")

# ----------------------------------------------------
# SIGNALS
# ----------------------------------------------------

st.subheader("⚡ Detected Institutional Signals")

for s in signals:

    st.success(s)

# ----------------------------------------------------
# PRICE CHART
# ----------------------------------------------------

st.subheader("📈 Institutional Price Chart")

chart_df = pd.DataFrame({

    "Close": close_series,

    "EMA20": df["EMA20"],

    "EMA50": df["EMA50"]

})

st.line_chart(
    chart_df,
    use_container_width=True
)
# ----------------------------------------------------
# ANALYTICS PANELS
# ----------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("📊 Technical Analytics")

    st.dataframe(

        pd.DataFrame({

            "Metric": [

                "RSI",

                "MACD",

                "EMA20",

                "EMA50",

                "ATR",

                "30D Momentum"
            ],

            "Value": [

                round(latest_rsi,2),

                round(latest_macd,2),

                round(latest_ema20,2),

                round(latest_ema50,2),

                round(latest_atr,2),

                str(round(returns_30*100,2)) + "%"
            ]
        }),

        use_container_width=True
    )

with right:

    st.subheader("🧠 AI Interpretation")

    interpretation = f"""

    {stock.upper()} currently has an AI score of {score}/100.

    Current recommendation:
    {recommendation}

    The system is detecting:

    • momentum structure

    • trend strength

    • institutional participation

    • technical positioning

    • volatility-adjusted opportunity

    Risk management remains essential.
    """

    st.info(interpretation)

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.divider()

st.caption(
    "Master Institutional AI Market Terminal"
  )
