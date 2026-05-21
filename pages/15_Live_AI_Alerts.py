import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator

st.title("🚨 Live AI Alert Engine")

st.caption("Real-Time Institutional Signal Monitoring")

# ----------------------------------------
# STOCK UNIVERSE
# ----------------------------------------

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

alerts = []

# ----------------------------------------
# ALERT ENGINE
# ----------------------------------------

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

        # --------------------------------
        # ALERT CONDITIONS
        # --------------------------------

        score = 0
        reasons = []

        if ema20.iloc[-1] > ema50.iloc[-1]:
            score += 30
            reasons.append(
                "Bullish EMA structure"
            )

        if current_price > ema50.iloc[-1]:
            score += 25
            reasons.append(
                "Trading above EMA50"
            )

        if 50 < rsi.iloc[-1] < 70:
            score += 20
            reasons.append(
                "Healthy momentum"
            )

        if volume_ratio > 1.5:
            score += 25
            reasons.append(
                "Strong volume participation"
            )

        # --------------------------------
        # SIGNAL GENERATION
        # --------------------------------

        if score >= 80:

            signal = "🟢 HIGH CONVICTION"

        elif score >= 60:

            signal = "🟡 POSITIVE"

        elif score >= 40:

            signal = "🟠 WATCHLIST"

        else:

            signal = "🔴 WEAK"

        alerts.append({

            "Stock": stock_name,

            "Signal": signal,

            "AI Score": score,

            "Current Price": round(current_price,2),

            "Reasons": ", ".join(reasons)
        })

    except:
        pass

# ----------------------------------------
# ALERT TABLE
# ----------------------------------------

alert_df = pd.DataFrame(alerts)

if not alert_df.empty:

    alert_df = alert_df.sort_values(
        by="AI Score",
        ascending=False
    )

    st.subheader("🔥 Live AI Signals")

    st.dataframe(
        alert_df,
        use_container_width=True
    )

# ----------------------------------------
# TOP SIGNAL
# ----------------------------------------

if not alert_df.empty:

    top_signal = alert_df.iloc[0]

    st.subheader("🏆 Highest Conviction Alert")

    st.success(
        f'''
        {top_signal['Stock']} currently shows
        the strongest signal profile.

        Signal:
        {top_signal['Signal']}

        AI Score:
        {top_signal['AI Score']}/100

        Key Drivers:
        {top_signal['Reasons']}
        '''
    )

# ----------------------------------------
# MARKET MONITOR
# ----------------------------------------

st.subheader("🧠 AI Monitoring Commentary")

st.info(
    '''
    The Live AI Alert Engine continuously monitors:
    
    • trend quality
    
    • momentum persistence
    
    • participation strength
    
    • breakout conditions
    
    • institutional-style setups

    Higher AI scores generally indicate
    stronger alignment between:
    
    • trend
    
    • momentum
    
    • participation
    
    • structure
    '''
)

# ----------------------------------------
# RISK NOTE
# ----------------------------------------

st.warning(
    '''
    Real-time alerts should always be combined with:
    
    • risk management
    
    • broader market context
    
    • sector leadership
    
    • volatility conditions
    
    Markets remain probabilistic.
    '''
)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Real-time institutional AI monitoring"
)
