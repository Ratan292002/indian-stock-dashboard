import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator

st.title("📊 Market Breadth & Heatmap Engine")

st.caption("Internal Market Strength Monitor")

# -------------------------------------
# STOCK UNIVERSE
# -------------------------------------

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

results = []

advances = 0
declines = 0
above_ema50 = 0

# -------------------------------------
# BREADTH ANALYSIS
# -------------------------------------

for stock_name, symbol in stocks.items():

    try:

        df = yf.download(
            symbol,
            period="6mo",
            progress=False
        )

        close = df['Close'].squeeze()

        current_price = float(close.iloc[-1])

        prev_price = float(close.iloc[-2])

        daily_change = (
            (current_price - prev_price)
            / prev_price
        ) * 100

        ema50 = EMAIndicator(
            close=close,
            window=50
        ).ema_indicator()

        # ------------------------------
        # ADVANCE / DECLINE
        # ------------------------------

        if daily_change > 0:
            advances += 1
        else:
            declines += 1

        # ------------------------------
        # EMA POSITION
        # ------------------------------

        if current_price > ema50.iloc[-1]:
            above_ema50 += 1
            trend_status = "🟢 Strong"
        else:
            trend_status = "🔴 Weak"

        results.append({
            "Stock": stock_name,
            "Daily Change %": round(daily_change,2),
            "Trend Status": trend_status
        })

    except:
        pass

# -------------------------------------
# HEATMAP TABLE
# -------------------------------------

heatmap_df = pd.DataFrame(results)

st.subheader("🔥 Momentum Heatmap")

st.dataframe(
    heatmap_df,
    use_container_width=True
)

# -------------------------------------
# BREADTH METRICS
# -------------------------------------

total_stocks = len(stocks)

breadth_score = (
    above_ema50 / total_stocks
) * 100

st.subheader("📈 Breadth Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Advances", advances)

col2.metric("Declines", declines)

col3.metric(
    "% Above EMA50",
    f"{round(breadth_score,2)}%"
)

col4.metric(
    "Advance/Decline Ratio",
    round(advances / max(declines,1),2)
)

# -------------------------------------
# MARKET HEALTH ENGINE
# -------------------------------------

st.subheader("🧠 Market Health Engine")

if breadth_score > 70:
    regime = "🟢 Strong Bullish Breadth"

elif breadth_score > 50:
    regime = "🟡 Moderate Bullish Breadth"

elif breadth_score > 35:
    regime = "🟠 Mixed Market Structure"

else:
    regime = "🔴 Weak / Defensive Market"

st.success(regime)

# -------------------------------------
# LEADERS / LAGGARDS
# -------------------------------------

if not heatmap_df.empty:

    strongest = heatmap_df.sort_values(
        by="Daily Change %",
        ascending=False
    ).iloc[0]

    weakest = heatmap_df.sort_values(
        by="Daily Change %",
        ascending=True
    ).iloc[0]

    st.subheader("🏆 Market Leadership")

    col1, col2 = st.columns(2)

    col1.success(
        f'''
        Strongest:
        
        {strongest['Stock']}
        
        Change:
        {strongest['Daily Change %']}%
        '''
    )

    col2.error(
        f'''
        Weakest:
        
        {weakest['Stock']}
        
        Change:
        {weakest['Daily Change %']}%
        '''
    )

# -------------------------------------
# INTERPRETATION
# -------------------------------------

st.divider()

st.subheader("📌 Breadth Interpretation")

st.info(
    '''
    Breadth measures how broadly market participation
    is distributed.

    Strong breadth usually indicates:
    
    • healthier rallies
    
    • stronger participation
    
    • broader momentum
    
    • lower fragility

    Weak breadth often signals:
    
    • concentrated rallies
    
    • rising market fragility
    
    • defensive conditions
    '''
)

# -------------------------------------
# FOOTER
# -------------------------------------

st.divider()

st.caption(
    "Institutional-style breadth analytics"
)
