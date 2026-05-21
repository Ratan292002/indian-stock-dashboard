import streamlit as st
import yfinance as yf
import pandas as pd

# ---------------------------------------
# PAGE CONFIG
# ---------------------------------------

st.set_page_config(
    page_title="Ratan Quant Terminal",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------
# CUSTOM CSS
# ---------------------------------------

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1, h2, h3 {
    color: #F9FAFB;
}

.stMetric {
    background-color: #1F2937;
    padding: 15px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------
# SIDEBAR
# ---------------------------------------

st.sidebar.title("📊 Ratan Quant Terminal")

st.sidebar.info(
    '''
    Institutional AI Market Intelligence
    
    Modules:
    
    • Global Markets
    
    • Smart Money
    
    • AI Scanner
    
    • Sector Rotation
    
    • Breadth Engine
    
    • Portfolio Analytics
    
    • Options Intelligence
    
    • AI Daily Reports
    '''
)

st.sidebar.divider()

# ---------------------------------------
# DASHBOARD HEADER
# ---------------------------------------

st.title("🌍 Ratan Quant Terminal")

st.caption(
    "AI-Powered Institutional Market Intelligence Platform"
)

# ---------------------------------------
# QUICK MARKET SNAPSHOT
# ---------------------------------------

indices = {
    "NIFTY": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC"
}

cols = st.columns(4)

i = 0

for name, ticker in indices.items():

    try:

        df = yf.download(
            ticker,
            period="5d",
            progress=False
        )

        latest = float(df['Close'].iloc[-1])
        prev = float(df['Close'].iloc[-2])

        pct = (
            (latest - prev)
            / prev
        ) * 100

        cols[i].metric(
            name,
            round(latest,2),
            f"{round(pct,2)}%"
        )

        i += 1

    except:
        pass

# ---------------------------------------
# PLATFORM OVERVIEW
# ---------------------------------------

st.divider()

st.subheader("🧠 Platform Overview")

overview = pd.DataFrame({

    "Engine": [
        "Global Macro",
        "AI Scanner",
        "Smart Money",
        "Sector Rotation",
        "Market Breadth",
        "Portfolio Analytics",
        "Options Intelligence",
        "News Sentiment"
    ],

    "Status": [
        "Active",
        "Active",
        "Active",
        "Active",
        "Active",
        "Active",
        "Active",
        "Active"
    ]
})

st.dataframe(
    overview,
    use_container_width=True
)

# ---------------------------------------
# AI TERMINAL COMMENTARY
# ---------------------------------------

st.subheader("🤖 AI Terminal Commentary")

st.info(
    '''
    Ratan Quant Terminal integrates:
    
    • macro intelligence
    
    • institutional analytics
    
    • opportunity scanning
    
    • breadth analytics
    
    • sector rotation
    
    • derivatives positioning
    
    • AI commentary
    
    The platform is designed to behave as a
    multi-layer market intelligence ecosystem
    rather than a simple stock dashboard.
    '''
)

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "Institutional-grade educational market terminal"
)
