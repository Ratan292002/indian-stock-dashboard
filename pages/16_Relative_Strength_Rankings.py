import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🏆 Relative Strength Ranking Engine")

st.caption("Institutional Momentum Leadership Analytics")

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

# -----------------------------------------
# NIFTY BENCHMARK
# -----------------------------------------

nifty = yf.download(
    "^NSEI",
    period="6mo",
    progress=False
)

nifty_close = nifty['Close'].squeeze()

nifty_return = (
    (nifty_close.iloc[-1] - nifty_close.iloc[0])
    / nifty_close.iloc[0]
) * 100

# -----------------------------------------
# RELATIVE STRENGTH ENGINE
# -----------------------------------------

results = []

for stock_name, symbol in stocks.items():

    try:

        df = yf.download(
            symbol,
            period="6mo",
            progress=False
        )

        close = df['Close'].squeeze()

        stock_return = (
            (close.iloc[-1] - close.iloc[0])
            / close.iloc[0]
        ) * 100

        relative_strength = (
            stock_return - nifty_return
        )

        # ---------------------------------
        # RANKING
        # ---------------------------------

        if relative_strength > 15:
            leadership = "🟢 Elite Leader"

        elif relative_strength > 5:
            leadership = "🟡 Strong Outperformer"

        elif relative_strength > 0:
            leadership = "🟠 Mild Outperformer"

        else:
            leadership = "🔴 Underperformer"

        results.append({

            "Stock": stock_name,

            "6M Return %": round(
                float(stock_return),
                2
            ),

            "Relative Strength": round(
                float(relative_strength),
                2
            ),

            "Leadership": leadership
        })

    except:
        pass

# -----------------------------------------
# RESULTS
# -----------------------------------------

rs_df = pd.DataFrame(results)

if not rs_df.empty:

    rs_df = rs_df.sort_values(
        by="Relative Strength",
        ascending=False
    )

    st.subheader("🔥 Institutional Leadership Rankings")

    st.dataframe(
        rs_df,
        use_container_width=True
    )

# -----------------------------------------
# TOP LEADER
# -----------------------------------------

if not rs_df.empty:

    leader = rs_df.iloc[0]

    st.subheader("🏆 Market Leader")

    st.success(
        f'''
        {leader['Stock']} currently ranks as the
        strongest relative strength candidate.

        Relative Strength:
        {leader['Relative Strength']}%

        Leadership Classification:
        {leader['Leadership']}
        '''
    )

# -----------------------------------------
# MARKET INTERPRETATION
# -----------------------------------------

st.subheader("🧠 Relative Strength Commentary")

st.info(
    '''
    Relative strength measures how strongly
    a stock performs compared to the broader market.

    Institutional momentum strategies typically
    prioritize:
    
    • consistent outperformers
    
    • leadership stocks
    
    • strong sector participants
    
    • trend persistence

    Strong relative strength often indicates:
    
    • institutional accumulation
    
    • stronger momentum
    
    • higher participation
    
    • leadership behavior
    '''
)

# -----------------------------------------
# RISK NOTE
# -----------------------------------------

st.warning(
    '''
    Relative strength leadership can change rapidly
    during:
    
    • earnings season
    
    • macro shocks
    
    • sector rotation
    
    • market corrections

    Leadership analysis should be combined with:
    
    • risk management
    
    • breadth
    
    • sector analytics
    
    • smart money tracking
    '''
)

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "Institutional momentum leadership analytics"
)
