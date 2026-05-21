import streamlit as st
import yfinance as yf
import pandas as pd

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import sample_cov
from pypfopt.efficient_frontier import EfficientFrontier

st.title("🧠 AI Portfolio Optimizer")

st.caption("Institutional Portfolio Intelligence")

# ----------------------------------------
# STOCK UNIVERSE
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

selected_stocks = st.multiselect(

    "Select Stocks",

    list(stocks.keys()),

    default=[
        "RELIANCE",
        "TCS",
        "HDFCBANK",
        "ICICIBANK"
    ]
)

# ----------------------------------------
# DOWNLOAD DATA
# ----------------------------------------

price_data = pd.DataFrame()

for stock in selected_stocks:

    symbol = stocks[stock]

    df = yf.download(

        symbol,

        period="2y",

        progress=False
    )

    price_data[stock] = df['Close']

# ----------------------------------------
# OPTIMIZATION
# ----------------------------------------

try:

    mu = mean_historical_return(price_data)

    S = sample_cov(price_data)

    ef = EfficientFrontier(mu, S)

    weights = ef.max_sharpe()

    cleaned_weights = ef.clean_weights()

    expected_return, volatility, sharpe = ef.portfolio_performance()

    # ------------------------------------
    # WEIGHTS TABLE
    # ------------------------------------

    weights_df = pd.DataFrame({

        "Stock": list(cleaned_weights.keys()),

        "Allocation %": [
            round(v * 100,2)
            for v in cleaned_weights.values()
        ]
    })

    st.subheader("📊 Optimized Portfolio Allocation")

    st.dataframe(
        weights_df,
        use_container_width=True
    )

    # ------------------------------------
    # METRICS
    # ------------------------------------

    st.subheader("🔥 Portfolio Analytics")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Expected Annual Return",
        f"{round(expected_return*100,2)}%"
    )

    col2.metric(
        "Annual Volatility",
        f"{round(volatility*100,2)}%"
    )

    col3.metric(
        "Sharpe Ratio",
        round(sharpe,2)
    )

    # ------------------------------------
    # COMMENTARY
    # ------------------------------------

    st.subheader("🧠 AI Portfolio Commentary")

    st.success(
        '''
        The AI optimizer generated an allocation
        designed to maximize risk-adjusted returns.

        Institutional optimization models prioritize:
        
        • diversification
        
        • volatility management
        
        • return efficiency
        
        • correlation balancing
        
        • capital allocation efficiency
        '''
    )

    st.info(
        '''
        Portfolio optimization is one of the core
        foundations of institutional investing.

        Professional funds continuously optimize:
        
        • allocations
        
        • correlations
        
        • volatility
        
        • drawdowns
        
        • return efficiency
        '''
    )

except Exception as e:

    st.error(
        "Portfolio optimization failed. Try selecting different stocks."
    )

# ----------------------------------------
# RISK NOTE
# ----------------------------------------

st.warning(
    '''
    Portfolio optimization models rely on:
    
    • historical data
    
    • statistical assumptions
    
    • covariance behavior
    
    • return estimates

    Future market behavior may differ significantly.
    '''
)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "Institutional AI portfolio optimization"
)
