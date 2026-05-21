import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
from ta.volatility import AverageTrueRange

st.title("🧠 AI Predictive Scoring Engine")

st.caption("Institutional Probability Intelligence")

# -----------------------------------------
# STOCK UNIVERSE
# -----------------------------------------

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

# -----------------------------------------
# AI ENGINE
# -----------------------------------------

for stock_name, symbol in stocks.items():

    try:

        df = yf.download(
            symbol,
            period="1y",
            progress=False
        )

        close = df['Close'].squeeze()

        current_price = float(close.iloc[-1])

        # ---------------------------------
        # INDICATORS
        # ---------------------------------

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

        atr = AverageTrueRange(
            high=df['High'].squeeze(),
            low=df['Low'].squeeze(),
            close=close
        ).average_true_range()

        avg_volume = (
            df['Volume']
            .tail(20)
            .mean()
        )

        latest_volume = df['Volume'].iloc[-1]

        volume_ratio = (
            latest_volume / avg_volume
        )

        # ---------------------------------
        # PREDICTIVE SCORE
        # ---------------------------------

        score = 0

        # TREND

        if ema20.iloc[-1] > ema50.iloc[-1]:
            score += 25

        # PRICE POSITION

        if current_price > ema50.iloc[-1]:
            score += 20

        # MOMENTUM

        if 55 < rsi.iloc[-1] < 70:
            score += 20

        # PARTICIPATION

        if volume_ratio > 1.2:
            score += 20

        # VOLATILITY QUALITY

        atr_pct = (
            atr.iloc[-1]
            / current_price
        ) * 100

        if atr_pct < 4:
            score += 15

        # ---------------------------------
        # CLASSIFICATION
        # ---------------------------------

        if score >= 80:

            prediction = "🟢 High Probability"

        elif score >= 60:

            prediction = "🟡 Moderate Probability"

        elif score >= 40:

            prediction = "🟠 Mixed Structure"

        else:

            prediction = "🔴 Weak Probability"

        results.append({

            "Stock": stock_name,

            "AI Predictive Score": score,

            "Prediction": prediction,

            "RSI": round(
                float(rsi.iloc[-1]),
                2
            ),

            "Volume Ratio": round(
                float(volume_ratio),
                2
            ),

            "ATR %": round(
                float(atr_pct),
                2
            )
        })

    except:
        pass

# -----------------------------------------
# RESULTS
# -----------------------------------------

score_df = pd.DataFrame(results)

if not score_df.empty:

    score_df = score_df.sort_values(
        by="AI Predictive Score",
        ascending=False
    )

    st.subheader("🔥 AI Predictive Rankings")

    st.dataframe(
        score_df,
        use_container_width=True
    )

# -----------------------------------------
# TOP PREDICTION
# -----------------------------------------

if not score_df.empty:

    top_pick = score_df.iloc[0]

    st.subheader("🏆 Highest Probability Setup")

    st.success(
        f'''
        {top_pick['Stock']} currently shows
        the strongest predictive structure.

        AI Predictive Score:
        {top_pick['AI Predictive Score']}/100

        Classification:
        {top_pick['Prediction']}
        '''
    )

# -----------------------------------------
# AI COMMENTARY
# -----------------------------------------

st.subheader("🧠 Predictive Intelligence Commentary")

st.info(
    '''
    The AI Predictive Engine evaluates:
    
    • trend persistence
    
    • momentum quality
    
    • participation strength
    
    • volatility structure
    
    • probabilistic alignment

    Institutional predictive systems generally
    prioritize:
    
    • asymmetric opportunities
    
    • strong participation
    
    • controlled volatility
    
    • higher timeframe alignment

    Higher scores indicate stronger alignment
    across multiple analytical dimensions.
    '''
)

# -----------------------------------------
# RISK NOTE
# -----------------------------------------

st.warning(
    '''
    Predictive analytics remain probabilistic.

    No system guarantees outcomes.

    Professional workflows combine:
    
    • risk management
    
    • diversification
    
    • market context
    
    • disciplined execution
    '''
)

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "Institutional AI probabilistic analytics"
)
