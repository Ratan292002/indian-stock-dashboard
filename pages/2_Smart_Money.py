import streamlit as st
import pandas as pd
import yfinance as yf

st.title("🏦 Smart Money Tracker")

st.caption("Institutional Activity & Momentum Monitor")

# ---------------------------------
# STOCK LIST
# ---------------------------------

stocks = {
    "RELIANCE": "RELIANCE.NS",
    "ICICIBANK": "ICICIBANK.NS",
    "HDFCBANK": "HDFCBANK.NS",
    "SBIN": "SBIN.NS",
    "TATAMOTORS": "TATAMOTORS.NS",
    "LT": "LT.NS",
    "POLYCAB": "POLYCAB.NS",
    "ITC": "ITC.NS",
    "INFY": "INFY.NS",
    "TCS": "TCS.NS"
}

# ---------------------------------
# SMART MONEY SCANNER
# ---------------------------------

results = []

for stock_name, symbol in stocks.items():

    try:
        df = yf.download(symbol, period="3mo", progress=False)

        latest_close = float(df['Close'].iloc[-1])

        avg_volume = df['Volume'].tail(20).mean()
        latest_volume = df['Volume'].iloc[-1]

        volume_ratio = latest_volume / avg_volume

        price_change = (
            (df['Close'].iloc[-1] - df['Close'].iloc[-5])
            / df['Close'].iloc[-5]
        ) * 100

        smart_money_score = 0

        if volume_ratio > 1.5:
            smart_money_score += 40

        if price_change > 3:
            smart_money_score += 30

        if latest_close > df['Close'].mean():
            smart_money_score += 30

        results.append({
            "Stock": stock_name,
            "Price": round(latest_close,2),
            "5D Momentum %": round(float(price_change),2),
            "Volume Spike": round(float(volume_ratio),2),
            "Smart Money Score": smart_money_score
        })

    except:
        pass

# ---------------------------------
# RESULTS TABLE
# ---------------------------------

smart_df = pd.DataFrame(results)

if not smart_df.empty:

    smart_df = smart_df.sort_values(
        by="Smart Money Score",
        ascending=False
    )

    st.subheader("🔥 Institutional Momentum Candidates")

    st.dataframe(
        smart_df,
        use_container_width=True
    )

# ---------------------------------
# INTERPRETATION
# ---------------------------------

st.divider()

st.subheader("🧠 Interpretation Engine")

st.info(
    '''
    High Smart Money Scores generally indicate:
    
    • Strong participation by institutions
    
    • Momentum supported by volume
    
    • Potential accumulation phases
    
    • Stronger trend persistence
    
    Stocks with rising price + rising volume often indicate
    healthier institutional participation compared to
    low-volume speculative moves.
    '''
)

# ---------------------------------
# MARKET NOTES
# ---------------------------------

st.subheader("📌 Institutional Watch")

st.warning(
    '''
    Monitor:
    
    • Delivery spikes
    
    • Bulk/block deals
    
    • Sudden sector rotation
    
    • Relative strength vs Nifty
    
    • High-volume breakouts
    
    These often precede stronger directional moves.
    '''
)
