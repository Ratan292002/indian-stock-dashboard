import streamlit as st
import yfinance as yf
import pandas as pd

from sklearn.ensemble import IsolationForest

st.title("🧠 AI Anomaly Detection Engine")

st.caption("Institutional Market Irregularity Scanner")

# ----------------------------------------
# STOCKS
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

results = []

# ----------------------------------------
# ANOMALY ENGINE
# ----------------------------------------

for stock_name, symbol in stocks.items():

    try:

        df = yf.download(

            symbol,

            period="1y",

            progress=False
        )

        df = df.dropna()

        # --------------------------------
        # FEATURES
        # --------------------------------

        df["Returns"] = (
            df["Close"].pct_change()
        )

        df["Volume Change"] = (
            df["Volume"].pct_change()
        )

        df["Volatility"] = (
            df["Returns"]
            .rolling(10)
            .std()
        )

        df = df.dropna()

        features = df[[
            "Returns",
            "Volume Change",
            "Volatility"
        ]]

        # --------------------------------
        # ISOLATION FOREST
        # --------------------------------

        model = IsolationForest(

            contamination=0.03,

            random_state=42
        )

        df["Anomaly"] = model.fit_predict(features)

        latest_signal = df["Anomaly"].iloc[-1]

        anomaly_count = len(

            df[df["Anomaly"] == -1]
        )

        # --------------------------------
        # CLASSIFICATION
        # --------------------------------

        if latest_signal == -1:

            status = "🚨 Active Anomaly"

            score = 90

        elif anomaly_count > 10:

            status = "🟡 Elevated Irregularity"

            score = 65

        else:

            status = "🟢 Normal Structure"

            score = 35

        results.append({

            "Stock": stock_name,

            "Status": status,

            "Anomaly Score": score,

            "Total Anomalies": anomaly_count
        })

    except:
        pass

# ----------------------------------------
# RESULTS
# ----------------------------------------

results_df = pd.DataFrame(results)

if not results_df.empty:

    results_df = results_df.sort_values(

        by="Anomaly Score",

        ascending=False
    )

    st.subheader("🚨 Market Irregularity Rankings")

    st.dataframe(

        results_df,

        use_container_width=True
    )

# ----------------------------------------
# TOP ANOMALY
# ----------------------------------------

if not results_df.empty:

    top = results_df.iloc[0]

    st.subheader("🔥 Highest Market Irregularity")

    st.error(
        f'''
        {top["Stock"]} currently exhibits
        the strongest anomaly behavior.

        Status:
        {top["Status"]}

        Anomaly Score:
        {top["Anomaly Score"]}/100
        '''
    )

# ----------------------------------------
# COMMENTARY
# ----------------------------------------

st.subheader("🧠 AI Commentary")

st.info(
    '''
    Institutional anomaly systems monitor:
    
    • unusual volatility
    
    • abnormal participation
    
    • price dislocations
    
    • volume spikes
    
    • irregular momentum

    Market anomalies can sometimes precede:
    
    • breakouts
    
    • breakdowns
    
    • institutional accumulation
    
    • event-driven volatility
    
    • regime shifts

    AI anomaly systems help identify
    statistically unusual behavior.
    '''
)

# ----------------------------------------
# RISK NOTE
# ----------------------------------------

st.warning(
    '''
    Not all anomalies lead to opportunities.

    Irregular behavior may also reflect:
    
    • temporary noise
    
    • earnings reactions
    
    • macro shocks
    
    • liquidity events
    
    • panic-driven moves

    Proper risk management remains essential.
    '''
)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Institutional AI anomaly intelligence"
)
