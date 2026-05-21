import streamlit as st
import pandas as pd
from nsepython import *

st.title("📈 Live NSE Options Analytics")

st.caption("Institutional Derivatives Intelligence")

# ----------------------------------------
# INDEX SELECTION
# ----------------------------------------

index = st.selectbox(

    "Select Index",

    ["NIFTY", "BANKNIFTY"]
)

# ----------------------------------------
# OPTIONS DATA
# ----------------------------------------

try:

    options = option_chain(index)

    records = options['records']['data']

    df = pd.DataFrame(records)

    # ------------------------------------
    # EXTRACT DATA
    # ------------------------------------

    strikes = []
    ce_oi = []
    pe_oi = []

    for row in records:

        strike = row.get('strikePrice')

        strikes.append(strike)

        ce = row.get('CE')

        pe = row.get('PE')

        ce_oi.append(
            ce['openInterest']
            if ce else 0
        )

        pe_oi.append(
            pe['openInterest']
            if pe else 0
        )

    option_df = pd.DataFrame({

        "Strike": strikes,

        "Call OI": ce_oi,

        "Put OI": pe_oi
    })

    # ------------------------------------
    # PCR
    # ------------------------------------

    total_call_oi = option_df["Call OI"].sum()

    total_put_oi = option_df["Put OI"].sum()

    pcr = (
        total_put_oi / total_call_oi
    )

    # ------------------------------------
    # MAX PAIN
    # ------------------------------------

    option_df["Total OI"] = (

        option_df["Call OI"]
        +
        option_df["Put OI"]
    )

    max_pain = option_df.loc[
        option_df["Total OI"].idxmax()
    ]["Strike"]

    # ------------------------------------
    # CALL WRITING
    # ------------------------------------

    highest_call_oi = option_df.loc[
        option_df["Call OI"].idxmax()
    ]["Strike"]

    # ------------------------------------
    # PUT WRITING
    # ------------------------------------

    highest_put_oi = option_df.loc[
        option_df["Put OI"].idxmax()
    ]["Strike"]

    # ------------------------------------
    # DASHBOARD METRICS
    # ------------------------------------

    st.subheader("📊 Options Intelligence")

    col1, col2 = st.columns(2)

    col1.metric(
        "PCR",
        round(pcr,2)
    )

    col2.metric(
        "Max Pain",
        int(max_pain)
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "Strongest Call Writing",
        int(highest_call_oi)
    )

    col4.metric(
        "Strongest Put Writing",
        int(highest_put_oi)
    )

    # ------------------------------------
    # OI TABLE
    # ------------------------------------

    st.subheader("🔥 Open Interest Structure")

    st.dataframe(
        option_df.sort_values(
            by="Total OI",
            ascending=False
        ),
        use_container_width=True
    )

    # ------------------------------------
    # MARKET INTERPRETATION
    # ------------------------------------

    st.subheader("🧠 Derivatives Commentary")

    if pcr > 1.2:

        outlook = "🟢 Bullish Positioning"

    elif pcr < 0.8:

        outlook = "🔴 Bearish Positioning"

    else:

        outlook = "🟡 Neutral Positioning"

    st.success(
        f'''
        Current derivatives structure indicates:

        {outlook}

        PCR:
        {round(pcr,2)}

        Max Pain:
        {int(max_pain)}
        '''
    )

    st.info(
        '''
        Institutional derivatives analysis monitors:
        
        • PCR structure
        
        • call writing
        
        • put writing
        
        • max pain
        
        • hedging flows
        
        • volatility expectations

        Options markets often provide early clues
        regarding:
        
        • sentiment
        
        • positioning
        
        • institutional behavior
        '''
    )

except Exception as e:

    st.error(
        "Unable to fetch live NSE data currently."
    )

# ----------------------------------------
# RISK NOTE
# ----------------------------------------

st.warning(
    '''
    Options analytics should be interpreted
    alongside:
    
    • price action
    
    • volatility
    
    • macro conditions
    
    • event risk
    
    • institutional flows

    Derivatives positioning can shift rapidly.
    '''
)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Institutional NSE derivatives intelligence"
)
