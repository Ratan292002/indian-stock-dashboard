import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression

st.title("🤖 ML Forecasting Engine")

st.caption("Institutional Predictive Intelligence")

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

selected_stock = st.selectbox(

    "Select Stock",

    list(stocks.keys())
)

symbol = stocks[selected_stock]

# ----------------------------------------
# DOWNLOAD DATA
# ----------------------------------------

df = yf.download(

    symbol,

    period="2y",

    progress=False
)

df = df.reset_index()

df = df[["Date", "Close"]]

# ----------------------------------------
# ML PREPARATION
# ----------------------------------------

df["Day"] = np.arange(len(df))

X = df[["Day"]]

y = df["Close"]

# ----------------------------------------
# MODEL
# ----------------------------------------

model = LinearRegression()

model.fit(X, y)

# ----------------------------------------
# FUTURE FORECAST
# ----------------------------------------

future_days = 30

future_X = np.arange(

    len(df),

    len(df) + future_days

).reshape(-1,1)

forecast = model.predict(future_X)

# ----------------------------------------
# FORECAST DATAFRAME
# ----------------------------------------

future_df = pd.DataFrame({

    "Day": future_X.flatten(),

    "Forecast Price": forecast
})

# ----------------------------------------
# CURRENT METRICS
# ----------------------------------------

current_price = float(df["Close"].iloc[-1])

forecast_price = float(forecast[-1])

forecast_change = (

    (forecast_price - current_price)

    / current_price

) * 100

# ----------------------------------------
# FORECAST CLASSIFICATION
# ----------------------------------------

if forecast_change > 10:

    outlook = "🟢 Strong Bullish Forecast"

elif forecast_change > 3:

    outlook = "🟡 Mild Bullish Forecast"

elif forecast_change > -3:

    outlook = "🟠 Neutral Forecast"

else:

    outlook = "🔴 Bearish Forecast"

# ----------------------------------------
# METRICS
# ----------------------------------------

st.subheader("📊 ML Forecast Metrics")

col1, col2, col3 = st.columns(3)

col1.metric(

    "Current Price",

    f"₹{round(current_price,2)}"
)

col2.metric(

    "30-Day Forecast",

    f"₹{round(forecast_price,2)}"
)

col3.metric(

    "Forecast Change",

    f"{round(forecast_change,2)}%"
)

# ----------------------------------------
# CHART
# ----------------------------------------

chart_df = pd.DataFrame({

    "Historical": df["Close"]

})

chart_df["Forecast"] = np.nan

forecast_index = range(

    len(df),

    len(df) + future_days
)

forecast_series = pd.Series(

    forecast,

    index=forecast_index
)

chart_df = pd.concat([

    chart_df,

    pd.DataFrame({
        "Historical": [np.nan]*future_days,
        "Forecast": forecast
    })

], ignore_index=True)

st.subheader("📈 Forecast Projection")

st.line_chart(chart_df)

# ----------------------------------------
# OUTLOOK
# ----------------------------------------

st.subheader("🧠 AI Forecast Outlook")

st.success(

    f'''
    {selected_stock} currently exhibits:

    {outlook}

    Projected 30-day move:
    {round(forecast_change,2)}%
    '''
)

# ----------------------------------------
# COMMENTARY
# ----------------------------------------

st.info(
    '''
    The ML forecasting engine uses:
    
    • historical price behavior
    
    • trend estimation
    
    • regression modeling
    
    • probabilistic projections

    Institutional forecasting systems often combine:
    
    • machine learning
    
    • macro models
    
    • volatility analysis
    
    • momentum analytics
    
    • alternative datasets

    Forecasting models remain probabilistic,
    not deterministic.
    '''
)

# ----------------------------------------
# RISK NOTE
# ----------------------------------------

st.warning(
    '''
    Machine learning forecasts can fail during:
    
    • black swan events
    
    • macro shocks
    
    • earnings surprises
    
    • liquidity disruptions
    
    • regime shifts

    Forecasts should complement,
    not replace, disciplined investing.
    '''
)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Institutional machine learning forecasting"
)
