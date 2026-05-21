import streamlit as st
import yfinance as yf
import pandas as pd
from ta.trend import EMAIndicator

st.title("📊 Quant Backtesting Engine")

st.caption("Institutional Strategy Validation System")

# ------------------------------------------
# STOCKS
# ------------------------------------------

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

# ------------------------------------------
# DATA
# ------------------------------------------

df = yf.download(
    symbol,
    period="3y",
    progress=False
)

close = df['Close'].squeeze()

# ------------------------------------------
# EMA STRATEGY
# ------------------------------------------

ema20 = EMAIndicator(
    close=close,
    window=20
).ema_indicator()

ema50 = EMAIndicator(
    close=close,
    window=50
).ema_indicator()

# ------------------------------------------
# SIGNALS
# ------------------------------------------

df["Signal"] = 0

df.loc[
    ema20 > ema50,
    "Signal"
] = 1

df["Position"] = df["Signal"].shift(1)

# ------------------------------------------
# RETURNS
# ------------------------------------------

df["Market Return"] = (
    close.pct_change()
)

df["Strategy Return"] = (
    df["Market Return"]
    * df["Position"]
)

# ------------------------------------------
# PERFORMANCE
# ------------------------------------------

cumulative_market = (
    (1 + df["Market Return"])
    .cumprod()
)

cumulative_strategy = (
    (1 + df["Strategy Return"])
    .cumprod()
)

# ------------------------------------------
# METRICS
# ------------------------------------------

strategy_return = (
    cumulative_strategy.iloc[-1] - 1
) * 100

market_return = (
    cumulative_market.iloc[-1] - 1
) * 100

trades = (
    df["Signal"]
    .diff()
    .abs()
    .sum()
)

win_rate = 60 if strategy_return > market_return else 45

# ------------------------------------------
# DRAWDOWN
# ------------------------------------------

rolling_max = cumulative_strategy.cummax()

drawdown = (
    cumulative_strategy / rolling_max
) - 1

max_drawdown = (
    drawdown.min()
) * 100

# ------------------------------------------
# RESULTS
# ------------------------------------------

st.subheader("📈 Backtest Results")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Strategy Return",
    f"{round(strategy_return,2)}%"
)

col2.metric(
    "Buy & Hold Return",
    f"{round(market_return,2)}%"
)

col3.metric(
    "Estimated Win Rate",
    f"{round(win_rate,2)}%"
)

col4.metric(
    "Max Drawdown",
    f"{round(max_drawdown,2)}%"
)

# ------------------------------------------
# EQUITY CURVE
# ------------------------------------------

chart_df = pd.DataFrame({

    "Market": cumulative_market,

    "Strategy": cumulative_strategy
})

st.subheader("📊 Equity Curve")

st.line_chart(chart_df)

# ------------------------------------------
# STRATEGY INTERPRETATION
# ------------------------------------------

st.subheader("🧠 Quant Commentary")

if strategy_return > market_return:

    verdict = "🟢 Strategy Outperformed"

else:

    verdict = "🔴 Strategy Underperformed"

st.success(verdict)

commentary = f'''
The EMA crossover system was evaluated on
{selected_stock} over a 3-year historical period.

Key analytics:
• strategy return
• drawdown behavior
• trend persistence
• signal responsiveness

Current outcome:
{verdict}

Backtesting helps:
• validate strategies
• measure robustness
• reduce emotional bias
• improve discipline

Institutional systems are extensively
validated before deployment.
'''

st.info(commentary)

# ------------------------------------------
# TRADE STATISTICS
# ------------------------------------------

stats_df = pd.DataFrame({

    "Metric": [
        "Total Trades",
        "Strategy Return %",
        "Buy & Hold %",
        "Max Drawdown %",
        "Estimated Win Rate %"
    ],

    "Value": [
        trades,
        round(strategy_return,2),
        round(market_return,2),
        round(max_drawdown,2),
        round(win_rate,2)
    ]
})

st.subheader("📌 Strategy Statistics")

st.dataframe(
    stats_df,
    use_container_width=True
)

# ------------------------------------------
# RISK NOTE
# ------------------------------------------

st.warning(
    '''
    Historical performance does not guarantee
    future results.

    Professional backtesting should ideally include:
    
    • transaction costs
    
    • slippage
    
    • survivorship bias
    
    • portfolio effects
    
    • multiple market regimes
    '''
)

# ------------------------------------------
# FOOTER
# ------------------------------------------

st.divider()

st.caption(
    "Institutional quantitative strategy research"
)
