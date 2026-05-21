import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.title("🚀 AI Opportunity Scanner")

st.caption("High Probability Opportunity Detection Engine")

# ------------------------------------
# STOCK UNIVERSE
# ------------------------------------

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

# ------------------------------------
# AI SCAN ENGINE
# ------------------------------------

for stock_name, symbol in stocks.items():

    try:

        df = yf.download(
            symbol,
            period="6mo",
            progress=False
        )

        close = df['Close'].squeeze()

        current_price = float(close.iloc[-1])

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

        avg_volume = df['Volume'].tail(20).mean()
        latest_volume = df['Volume'].iloc[-1]

        volume_ratio = latest_volume / avg_volume

        score = 0
        reasons = []

        # --------------------------------
        # TREND QUALITY
        # --------------------------------

        if ema20.iloc[-1] > ema50.iloc[-1]:
            score += 25
            reasons.append("Bullish trend structure")

        # --------------------------------
        # PRICE POSITION
        # --------------------------------

        if current_price > ema50.iloc[-1]:
            score += 20
            reasons.append("Trading above EMA50")

        # --------------------------------
        # MOMENTUM
        # --------------------------------

        if 50 < rsi.iloc[-1] < 70:
            score += 20
            reasons.append("Healthy RSI momentum")

        # --------------------------------
        # VOLUME PARTICIPATION
        # --------------------------------

        if volume_ratio > 1.5:
            score += 20
            reasons.append("Strong volume participation")

        # --------------------------------
        # BREAKOUT DETECTION
        # --------------------------------

        recent_high = df['High'].tail(20).max()

        if current_price >= recent_high * 0.98:
            score += 15
            reasons.append("Near breakout zone")

        # --------------------------------
        # RECOMMENDATION
        # --------------------------------

        if score >= 80:
            recommendation = "🟢 Strong Opportunity"
            risk = "Moderate"

        elif score >= 60:
            recommendation = "🟡 Good Setup"
            risk = "Moderate"

        elif score >= 40:
            recommendation = "🟠 Watchlist"

            risk = "Moderate-High"

        else:
            recommendation = "🔴 Weak Setup"
            risk = "High"

        # --------------------------------
        # TRADE LEVELS
        # --------------------------------

        entry = round(current_price,2)
        stop_loss = round(current_price * 0.95,2)
        target = round(current_price * 1.12,2)

        results.append({

            "Stock": stock_name,

            "Price": entry,

            "AI Score": score,

            "Risk": risk,

            "Recommendation": recommendation,

            "Target": target,

            "Stop Loss": stop_loss,

            "Reasons": ", ".join(reasons)
        })

    except:
        pass

# ------------------------------------
# RESULTS
# ------------------------------------

scan_df = pd.DataFrame(results)

if not scan_df.empty:

    scan_df = scan_df.sort_values(
        by="AI Score",
        ascending=False
    )

    st.subheader("🔥 Ranked Opportunities")

    st.dataframe(
        scan_df,
        use_container_width=True
    )

# ------------------------------------
# TOP PICK
# ------------------------------------

if not scan_df.empty:

    top_pick = scan_df.iloc[0]

    st.subheader("🏆 Top AI Opportunity")

    st.success(
        f'''
        {top_pick['Stock']} currently ranks as the
        highest-conviction setup based on trend quality,
        momentum, participation, and breakout structure.

        Recommendation:
        {top_pick['Recommendation']}

        AI Score:
        {top_pick['AI Score']}/100
        '''
    )

# ------------------------------------
# INTERPRETATION
# ------------------------------------

st.divider()

st.subheader("🧠 AI Interpretation")

st.info(
    '''
    This engine ranks opportunities using:
    
    • Trend structure
    
    • Momentum quality
    
    • Volume participation
    
    • Relative positioning
    
    • Breakout probability
    
    Higher scores generally indicate stronger
    institutional-style setups.
    '''
)

# ------------------------------------
# FOOTER
# ------------------------------------

st.divider()

st.caption(
    "AI opportunity analytics • Educational use only"
)
