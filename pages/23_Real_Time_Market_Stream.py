import streamlit as st
import yfinance as yf
import pandas as pd

from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Real-Time Market Stream",
    layout="wide"
)

st.title("⚡ Real-Time Market Streaming Engine")

st.caption("Institutional Live Market Monitoring")

# ----------------------------------------
# AUTO REFRESH
# ----------------------------------------

count = st_autorefresh(

    interval=10000,

    limit=None,

    key="marketrefresh"
)

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

# ----------------------------------------
# LIVE MARKET TABLE
# ----------------------------------------

market_data = []

for stock_name, symbol in stocks.items():

    try:

        ticker = yf.Ticker(symbol)

        hist = ticker.history(period="2d")

        current_price = float(
            hist['Close'].iloc[-1]
        )

        previous_close = float(
            hist['Close'].iloc[-2]
        )

        change = (
            current_price - previous_close
        )

        change_pct = (
            change / previous_close
        ) * 100

        volume = int(
            hist['Volume'].iloc[-1]
        )

        market_data.append({

            "Stock": stock_name,

            "Price": round(current_price,2),

            "Change": round(change,2),

            "Change %": round(change_pct,2),

            "Volume": volume
        })

    except:
        pass

# ----------------------------------------
# DATAFRAME
# ----------------------------------------

df = pd.DataFrame(market_data)

if not df.empty:

    st.subheader("🔥 Live Market Dashboard")

    st.dataframe(
        df,
        use_container_width=True
    )

# ----------------------------------------
# MARKET LEADERS
# ----------------------------------------

if not df.empty:

    top_gainer = df.loc[
        df["Change %"].idxmax()
    ]

    top_loser = df.loc[
        df["Change %"].idxmin()
    ]

    col1, col2 = st.columns(2)

    col1.success(
        f'''
        🟢 Top Gainer
        
        {top_gainer["Stock"]}

        {top_gainer["Change %"]}%
        '''
    )

    col2.error(
        f'''
        🔴 Top Loser
        
        {top_loser["Stock"]}

        {top_loser["Change %"]}%
        '''
    )

# ----------------------------------------
# LIVE COMMENTARY
# ----------------------------------------

st.subheader("🧠 Real-Time Commentary")

st.info(
    '''
    The real-time market stream continuously monitors:
    
    • live prices
    
    • momentum shifts
    
    • participation
    
    • intraday leadership
    
    • relative performance
    
    • volatility behavior

    Institutional trading systems rely heavily on:
    
    • low-latency data
    
    • continuous monitoring
    
    • dynamic positioning
    
    • real-time analytics
    '''
)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Institutional real-time streaming analytics"
)
