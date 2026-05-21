import streamlit as st
import yfinance as yf
import pandas as pd

st.title("🔄 Sector Rotation Engine")

st.caption("Institutional Sector Leadership Tracker")

# -----------------------------------
# SECTOR ETFs / PROXIES
# -----------------------------------

sectors = {
    "Banking": "^NSEBANK",
    "IT": "^CNXIT",
    "Auto": "^CNXAUTO",
    "Pharma": "^CNXPHARMA",
    "FMCG": "^CNXFMCG",
    "Metal": "^CNXMETAL",
    "Energy": "^CNXENERGY",
    "Realty": "^CNXREALTY"
}

results = []

# -----------------------------------
# SECTOR ANALYSIS
# -----------------------------------

for sector_name, ticker in sectors.items():

    try:
        df = yf.download(ticker, period="3mo", progress=False)

        latest = float(df['Close'].iloc[-1])

        one_month_return = (
            (df['Close'].iloc[-1] - df['Close'].iloc[-22])
            / df['Close'].iloc[-22]
        ) * 100

        volatility = (
            df['Close'].pct_change().std()
        ) * 100

        score = 0

        # Momentum
        if one_month_return > 5:
            score += 50

        elif one_month_return > 0:
            score += 30

        # Lower volatility better
        if volatility < 2:
            score += 30

        elif volatility < 3:
            score += 15

        # Trend
        if latest > df['Close'].mean():
            score += 20

        results.append({
            "Sector": sector_name,
            "1M Return %": round(float(one_month_return),2),
            "Volatility": round(float(volatility),2),
            "Leadership Score": score
        })

    except:
        pass

# -----------------------------------
# RESULTS
# -----------------------------------

sector_df = pd.DataFrame(results)

if not sector_df.empty:

    sector_df = sector_df.sort_values(
        by="Leadership Score",
        ascending=False
    )

    st.subheader("🏆 Strongest Sectors")

    st.dataframe(
        sector_df,
        use_container_width=True
    )

# -----------------------------------
# LEADERS / LAGGARDS
# -----------------------------------

if not sector_df.empty:

    leader = sector_df.iloc[0]['Sector']
    laggard = sector_df.iloc[-1]['Sector']

    col1, col2 = st.columns(2)

    col1.success(f"🔥 Sector Leader: {leader}")

    col2.error(f"⚠ Weakest Sector: {laggard}")

# -----------------------------------
# AI INTERPRETATION
# -----------------------------------

st.divider()

st.subheader("🧠 AI Sector Interpretation")

st.info(
    '''
    Sector rotation analysis helps identify where
    institutional capital is flowing.

    Strong sectors generally attract:
    
    • Better momentum
    
    • Stronger earnings participation
    
    • Higher institutional activity
    
    • Better relative strength

    Weak sectors often underperform even during
    bullish market phases.
    '''
)

# -----------------------------------
# RISK REGIME
# -----------------------------------

st.subheader("🌍 Market Regime")

if not sector_df.empty:

    avg_score = sector_df['Leadership Score'].mean()

    if avg_score > 70:
        regime = "🟢 Strong Risk-On Environment"

    elif avg_score > 50:
        regime = "🟡 Moderate Bullish Environment"

    elif avg_score > 35:
        regime = "🟠 Mixed / Sideways Market"

    else:
        regime = "🔴 Risk-Off / Weak Environment"

    st.warning(regime)

# -----------------------------------
# FOOTER
# -----------------------------------

st.divider()

st.caption(
    "Sector leadership analytics • Institutional-style interpretation"
)
