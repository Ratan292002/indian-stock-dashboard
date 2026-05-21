import streamlit as st
import yfinance as yf
import pandas as pd

st.title("💰 Earnings Analytics Engine")

st.caption("Institutional Earnings Intelligence")

# -----------------------------------------
# STOCKS
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
# EARNINGS ENGINE
# -----------------------------------------

for stock_name, symbol in stocks.items():

    try:

        ticker = yf.Ticker(symbol)

        income_stmt = ticker.quarterly_income_stmt

        revenues = income_stmt.loc["Total Revenue"]

        profits = income_stmt.loc["Net Income"]

        latest_revenue = float(revenues.iloc[0])
        prev_revenue = float(revenues.iloc[1])

        latest_profit = float(profits.iloc[0])
        prev_profit = float(profits.iloc[1])

        revenue_growth = (
            (latest_revenue - prev_revenue)
            / abs(prev_revenue)
        ) * 100

        profit_growth = (
            (latest_profit - prev_profit)
            / abs(prev_profit)
        ) * 100

        # ---------------------------------
        # QUALITY SCORING
        # ---------------------------------

        score = 0

        if revenue_growth > 10:
            score += 40

        elif revenue_growth > 0:
            score += 20

        if profit_growth > 15:
            score += 40

        elif profit_growth > 0:
            score += 20

        if latest_profit > 0:
            score += 20

        # ---------------------------------
        # CLASSIFICATION
        # ---------------------------------

        if score >= 80:
            classification = "🟢 Strong Earnings"

        elif score >= 60:
            classification = "🟡 Positive Earnings"

        elif score >= 40:
            classification = "🟠 Mixed Earnings"

        else:
            classification = "🔴 Weak Earnings"

        results.append({

            "Stock": stock_name,

            "Revenue Growth %": round(
                revenue_growth,
                2
            ),

            "Profit Growth %": round(
                profit_growth,
                2
            ),

            "Earnings Score": score,

            "Classification": classification
        })

    except:
        pass

# -----------------------------------------
# RESULTS
# -----------------------------------------

earnings_df = pd.DataFrame(results)

if not earnings_df.empty:

    earnings_df = earnings_df.sort_values(
        by="Earnings Score",
        ascending=False
    )

    st.subheader("🔥 Earnings Leadership Rankings")

    st.dataframe(
        earnings_df,
        use_container_width=True
    )

# -----------------------------------------
# TOP EARNINGS LEADER
# -----------------------------------------

if not earnings_df.empty:

    leader = earnings_df.iloc[0]

    st.subheader("🏆 Earnings Momentum Leader")

    st.success(
        f'''
        {leader['Stock']} currently exhibits
        the strongest earnings profile.

        Earnings Score:
        {leader['Earnings Score']}/100

        Classification:
        {leader['Classification']}
        '''
    )

# -----------------------------------------
# AI COMMENTARY
# -----------------------------------------

st.subheader("🧠 Earnings Intelligence Commentary")

st.info(
    '''
    Institutional investors closely monitor:
    
    • revenue acceleration
    
    • profit expansion
    
    • operating leverage
    
    • earnings consistency
    
    • post-results momentum

    Strong earnings often drive:
    
    • institutional accumulation
    
    • valuation re-rating
    
    • relative strength leadership
    
    • sector outperformance

    Earnings quality is one of the most
    important long-term market drivers.
    '''
)

# -----------------------------------------
# RISK NOTE
# -----------------------------------------

st.warning(
    '''
    Earnings reactions may also depend on:
    
    • forward guidance
    
    • management commentary
    
    • macro environment
    
    • sector positioning
    
    • valuation expectations

    Markets often react to expectations,
    not only reported numbers.
    '''
)

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "Institutional earnings intelligence system"
)
