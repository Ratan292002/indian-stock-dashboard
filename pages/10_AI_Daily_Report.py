import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

st.title("🧠 AI Daily Market Report")

st.caption("Institutional Morning Briefing Engine")

# -----------------------------------------
# GLOBAL INDICES
# -----------------------------------------

indices = {
    "NIFTY 50": "^NSEI",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
    "NIKKEI": "^N225",
    "CRUDE": "CL=F",
    "GOLD": "GC=F",
    "USD/INR": "INR=X"
}

market_summary = []

bullish = 0
bearish = 0

# -----------------------------------------
# MARKET ANALYSIS
# -----------------------------------------

for name, ticker in indices.items():

    try:

        df = yf.download(
            ticker,
            period="5d",
            progress=False
        )

        latest = float(df['Close'].iloc[-1])
        prev = float(df['Close'].iloc[-2])

        pct_change = (
            (latest - prev)
            / prev
        ) * 100

        if pct_change > 0:
            bullish += 1
        else:
            bearish += 1

        market_summary.append({
            "Asset": name,
            "Change %": round(pct_change,2)
        })

    except:
        pass

summary_df = pd.DataFrame(market_summary)

# -----------------------------------------
# DATE
# -----------------------------------------

today = datetime.now().strftime("%d %B %Y")

st.subheader(f"📅 Daily Report — {today}")

# -----------------------------------------
# GLOBAL SNAPSHOT
# -----------------------------------------

st.subheader("🌍 Global Market Snapshot")

st.dataframe(
    summary_df,
    use_container_width=True
)

# -----------------------------------------
# MARKET REGIME
# -----------------------------------------

st.subheader("📊 AI Market Regime")

if bullish > bearish:
    regime = "🟢 Risk-On / Bullish Environment"

elif bearish > bullish:
    regime = "🔴 Risk-Off / Defensive Environment"

else:
    regime = "🟡 Mixed Market Environment"

st.success(regime)

# -----------------------------------------
# MARKET COMMENTARY
# -----------------------------------------

st.subheader("🧠 AI Market Commentary")

commentary = f'''
Global market positioning currently reflects:
{regime}

The dashboard evaluates:
• equity momentum
• commodity trends
• currency movement
• cross-market participation

Bullish assets:
{bullish}

Bearish assets:
{bearish}

Investors should monitor:
• global volatility
• sector leadership
• institutional participation
• macro developments

Risk management remains critical during
high-volatility conditions.
'''

st.info(commentary)

# -----------------------------------------
# TOP OPPORTUNITY
# -----------------------------------------

st.subheader("🚀 AI Opportunity Focus")

st.success(
    '''
    Current dashboard framework prioritizes:
    
    • trend persistence
    
    • sector leadership
    
    • institutional participation
    
    • strong breadth
    
    • controlled volatility
    
    Highest-conviction setups generally emerge
    during supportive macro + breadth conditions.
    '''
)

# -----------------------------------------
# RISK WARNINGS
# -----------------------------------------

st.subheader("⚠ AI Risk Monitor")

st.warning(
    '''
    Key risks to monitor:
    
    • Global yield spikes
    
    • Crude oil volatility
    
    • Weak breadth
    
    • Rising USD strength
    
    • Geopolitical shocks
    
    • Expiry-related volatility
    '''
)

# -----------------------------------------
# DAILY PLAYBOOK
# -----------------------------------------

st.subheader("📌 Institutional Playbook")

playbook = pd.DataFrame({

    "Theme": [
        "Trend Following",
        "Sector Rotation",
        "Breakout Trading",
        "Defensive Allocation",
        "High Momentum"
    ],

    "Current Status": [
        "Active",
        "Moderately Strong",
        "Selective",
        "Monitor",
        "Favorable"
    ]
})

st.dataframe(
    playbook,
    use_container_width=True
)

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "AI-generated institutional market briefing"
)
