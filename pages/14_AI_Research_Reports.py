import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.title("📑 AI Equity Research Reports")

st.caption("Institutional-Style Automated Research Engine")

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
    "Select Company",
    list(stocks.keys())
)

symbol = stocks[selected_stock]

# ------------------------------------------
# DATA
# ------------------------------------------

ticker = yf.Ticker(symbol)

info = ticker.info

df = yf.download(
    symbol,
    period="1y",
    progress=False
)

close = df['Close'].squeeze()

# ------------------------------------------
# METRICS
# ------------------------------------------

current_price = round(
    float(close.iloc[-1]),
    2
)

market_cap = info.get("marketCap", 0)

pe_ratio = info.get("trailingPE", 0)

pb_ratio = info.get("priceToBook", 0)

roe = info.get("returnOnEquity", 0)

debt_equity = info.get("debtToEquity", 0)

# ------------------------------------------
# TECHNICALS
# ------------------------------------------

ema20 = EMAIndicator(
    close=close,
    window=20
).ema_indicator()

ema50 = EMAIndicator(
    close=close,
    window=50
).ema_indicator()

rsi = RSIIndicator(
    close=close
).rsi()

# ------------------------------------------
# SCORING
# ------------------------------------------

score = 0

strengths = []
risks = []

if ema20.iloc[-1] > ema50.iloc[-1]:
    score += 20
    strengths.append(
        "Bullish trend structure"
    )
else:
    risks.append(
        "Weak medium-term trend"
    )

if 50 < rsi.iloc[-1] < 70:
    score += 15
    strengths.append(
        "Healthy momentum structure"
    )
else:
    risks.append(
        "Momentum not ideal"
    )

if pe_ratio and pe_ratio < 35:
    score += 15
    strengths.append(
        "Reasonable valuation"
    )
else:
    risks.append(
        "Valuation may be elevated"
    )

if roe and roe > 0.15:
    score += 20
    strengths.append(
        "Strong return on equity"
    )
else:
    risks.append(
        "ROE profile weaker"
    )

if debt_equity and debt_equity < 100:
    score += 15
    strengths.append(
        "Controlled debt structure"
    )
else:
    risks.append(
        "Debt profile elevated"
    )

if current_price > ema50.iloc[-1]:
    score += 15
    strengths.append(
        "Trading above medium-term support"
    )

# ------------------------------------------
# RATING
# ------------------------------------------

if score >= 80:
    rating = "🟢 High Conviction"

elif score >= 60:
    rating = "🟡 Positive"

elif score >= 40:
    rating = "🟠 Neutral"

else:
    rating = "🔴 Weak"

# ------------------------------------------
# HEADER
# ------------------------------------------

st.subheader(f"🏛 {selected_stock} Research Report")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Price",
    f"₹{current_price}"
)

col2.metric(
    "AI Rating",
    rating
)

col3.metric(
    "Conviction Score",
    f"{score}/100"
)

# ------------------------------------------
# FUNDAMENTALS
# ------------------------------------------

fund_df = pd.DataFrame({

    "Metric": [
        "Market Cap",
        "P/E",
        "P/B",
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

st.subheader("📊 Fundamental Snapshot")

st.dataframe(
    fund_df,
    use_container_width=True
)

# ------------------------------------------
# INVESTMENT THESIS
# ------------------------------------------

st.subheader("🧠 AI Investment Thesis")

thesis = f'''
{selected_stock} currently carries an
AI conviction rating of {rating}.

The stock demonstrates a blend of:
• technical structure
• momentum quality
• valuation analysis
• balance sheet strength
• trend persistence

Current price action suggests:
{"constructive momentum" if score >= 60 else "mixed market structure"}.

Institutional-quality setups generally emerge when:
• momentum aligns with fundamentals
• risk remains controlled
• broader sector participation improves
'''

st.info(thesis)

# ------------------------------------------
# STRENGTHS
# ------------------------------------------

st.subheader("✅ Key Strengths")

for s in strengths:
    st.success(s)

# ------------------------------------------
# RISKS
# ------------------------------------------

st.subheader("⚠ Key Risks")

for r in risks:
    st.error(r)

# ------------------------------------------
# TRADE SETUP
# ------------------------------------------

entry = current_price

stop_loss = round(
    current_price * 0.94,
    2
)

target1 = round(
    current_price * 1.10,
    2
)

target2 = round(
    current_price * 1.18,
    2
)

trade_df = pd.DataFrame({

    "Level": [
        "Entry",
        "Stop Loss",
        "Target 1",
        "Target 2"
    ],

    "Price": [
        entry,
        stop_loss,
        target1,
        target2
    ]
})

st.subheader("🎯 Institutional Trade Plan")

st.dataframe(
    trade_df,
    use_container_width=True
)

# ------------------------------------------
# FINAL COMMENTARY
# ------------------------------------------

st.divider()

st.subheader("📌 Final AI Commentary")

commentary = f'''
This report is generated using:
• momentum analytics
• valuation analysis
• technical structure
• risk evaluation
• balance sheet indicators

Current conviction profile:
{rating}

The platform prioritizes:
• probability-based setups
• risk-adjusted opportunities
• institutional-quality structures
rather than speculative momentum alone.
'''

st.warning(commentary)

# ------------------------------------------
# FOOTER
# ------------------------------------------

st.divider()

st.caption(
    "AI-generated institutional equity research"
)
