import streamlit as st
import pandas as pd

st.title("💼 Portfolio Analytics Engine")

st.caption("Institutional Portfolio Risk Intelligence")

# ----------------------------------------
# SAMPLE PORTFOLIO
# ----------------------------------------

portfolio = pd.DataFrame({

    "Stock": [
        "RELIANCE",
        "TCS",
        "HDFCBANK",
        "ICICIBANK",
        "POLYCAB"
    ],

    "Sector": [
        "Energy",
        "IT",
        "Banking",
        "Banking",
        "Capital Goods"
    ],

    "Investment": [
        250000,
        180000,
        220000,
        150000,
        100000
    ],

    "Return %": [
        12,
        8,
        15,
        9,
        20
    ]
})

# ----------------------------------------
# PORTFOLIO SUMMARY
# ----------------------------------------

total_value = portfolio["Investment"].sum()

weighted_return = (
    (portfolio["Investment"]
    * portfolio["Return %"]).sum()
) / total_value

# ----------------------------------------
# ALLOCATION
# ----------------------------------------

portfolio["Allocation %"] = (
    portfolio["Investment"]
    / total_value
) * 100

# ----------------------------------------
# RISK ENGINE
# ----------------------------------------

max_alloc = portfolio["Allocation %"].max()

if max_alloc > 40:
    concentration_risk = "🔴 High"

elif max_alloc > 25:
    concentration_risk = "🟡 Moderate"

else:
    concentration_risk = "🟢 Healthy"

# ----------------------------------------
# MAIN METRICS
# ----------------------------------------

st.subheader("📊 Portfolio Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Portfolio Value",
    f"₹{total_value:,.0f}"
)

col2.metric(
    "Weighted Return",
    f"{round(weighted_return,2)}%"
)

col3.metric(
    "Holdings",
    len(portfolio)
)

col4.metric(
    "Concentration Risk",
    concentration_risk
)

# ----------------------------------------
# HOLDINGS TABLE
# ----------------------------------------

st.subheader("🏛 Holdings Analysis")

st.dataframe(
    portfolio,
    use_container_width=True
)

# ----------------------------------------
# SECTOR EXPOSURE
# ----------------------------------------

sector_alloc = (
    portfolio.groupby("Sector")["Investment"]
    .sum()
    .reset_index()
)

sector_alloc["Sector Allocation %"] = (
    sector_alloc["Investment"]
    / total_value
) * 100

st.subheader("🔄 Sector Exposure")

st.dataframe(
    sector_alloc,
    use_container_width=True
)

# ----------------------------------------
# BEST / WORST HOLDINGS
# ----------------------------------------

best = portfolio.sort_values(
    by="Return %",
    ascending=False
).iloc[0]

worst = portfolio.sort_values(
    by="Return %",
    ascending=True
).iloc[0]

st.subheader("🏆 Portfolio Leaders")

col1, col2 = st.columns(2)

col1.success(
    f'''
    Best Performer:
    
    {best['Stock']}
    
    Return:
    {best['Return %']}%
    '''
)

col2.error(
    f'''
    Weakest Performer:
    
    {worst['Stock']}
    
    Return:
    {worst['Return %']}%
    '''
)

# ----------------------------------------
# AI COMMENTARY
# ----------------------------------------

st.divider()

st.subheader("🧠 AI Portfolio Commentary")

commentary = f'''
Portfolio currently contains {len(portfolio)} holdings
with total capital allocation of ₹{total_value:,.0f}.

Weighted portfolio return stands at
{round(weighted_return,2)}%.

Current concentration risk is classified as:
{concentration_risk}

Sector diversification remains important to reduce
portfolio fragility during market volatility.

Institutional portfolios typically avoid excessive
single-sector concentration.
'''

st.info(commentary)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Institutional-style portfolio analytics"
)
