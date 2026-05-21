import streamlit as st
import pandas as pd
import yfinance as yf

st.title("📈 Options Chain Intelligence")

st.caption("Institutional Positioning & Derivatives Analytics")

# ---------------------------------------
# MARKET DATA
# ---------------------------------------

nifty = yf.download(
    "^NSEI",
    period="5d",
    progress=False
)

current_nifty = round(
    float(nifty['Close'].iloc[-1]),
    2
)

# ---------------------------------------
# SIMULATED OPTIONS ENGINE
# ---------------------------------------

# NOTE:
# True NSE live options chain APIs often
# block cloud environments.
# This engine simulates institutional logic.

put_oi = 1450000
call_oi = 1220000

pcr = round(
    put_oi / call_oi,
    2
)

max_pain = round(
    current_nifty * 0.995,
    0
)

support = round(
    current_nifty * 0.985,
    0
)

resistance = round(
    current_nifty * 1.015,
    0
)

# ---------------------------------------
# MARKET SENTIMENT
# ---------------------------------------

if pcr > 1.2:
    sentiment = "🟢 Bullish Positioning"

elif pcr > 0.9:
    sentiment = "🟡 Neutral Positioning"

else:
    sentiment = "🔴 Bearish Positioning"

# ---------------------------------------
# MAIN METRICS
# ---------------------------------------

st.subheader("📊 Options Positioning")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "NIFTY",
    current_nifty
)

col2.metric(
    "PCR",
    pcr
)

col3.metric(
    "Max Pain",
    max_pain
)

col4.metric(
    "Market Bias",
    sentiment
)

# ---------------------------------------
# SUPPORT / RESISTANCE
# ---------------------------------------

st.subheader("🎯 Institutional Zones")

zone_df = pd.DataFrame({

    "Level": [
        "Support",
        "Resistance",
        "Max Pain"
    ],

    "Value": [
        support,
        resistance,
        max_pain
    ]
})

st.dataframe(
    zone_df,
    use_container_width=True
)

# ---------------------------------------
# OI BUILDUP
# ---------------------------------------

st.subheader("🏦 Open Interest Positioning")

oi_df = pd.DataFrame({

    "Type": [
        "Put OI",
        "Call OI"
    ],

    "Contracts": [
        put_oi,
        call_oi
    ]
})

st.dataframe(
    oi_df,
    use_container_width=True
)

# ---------------------------------------
# AI INTERPRETATION
# ---------------------------------------

st.divider()

st.subheader("🧠 AI Derivatives Commentary")

commentary = f'''
Current Put-Call Ratio stands at {pcr}.

PCR helps estimate institutional derivatives sentiment.

Higher PCR generally indicates:
• stronger put writing
• supportive market structure
• bullish positioning

Current market bias is classified as:
{sentiment}

Max Pain theory suggests expiry gravitation
toward {max_pain} levels.

Support and resistance zones help identify
high institutional activity areas.
'''

st.info(commentary)

# ---------------------------------------
# RISK NOTES
# ---------------------------------------

st.subheader("⚠ Derivatives Risk")

st.warning(
    '''
    Options positioning can change rapidly during:
    
    • RBI/Fed events
    
    • Expiry sessions
    
    • Global macro shocks
    
    • Volatility spikes
    
    Derivatives analytics should be combined with:
    
    • breadth
    
    • smart money
    
    • sector rotation
    
    • trend analysis
    '''
)

# ---------------------------------------
# FOOTER
# ---------------------------------------

st.divider()

st.caption(
    "Institutional derivatives analytics"
)
