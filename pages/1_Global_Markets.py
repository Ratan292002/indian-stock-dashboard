import streamlit as st
import yfinance as yf

st.title("🌎 Global Market Command Center")

indices = {
    "NIFTY 50": "^NSEI",
    "BANK NIFTY": "^NSEBANK",
    "S&P 500": "^GSPC",
    "NASDAQ": "^IXIC",
    "DOW JONES": "^DJI",
    "NIKKEI": "^N225",
    "HANG SENG": "^HSI",
    "DAX": "^GDAXI",
    "FTSE": "^FTSE",
    "CRUDE OIL": "CL=F",
    "GOLD": "GC=F",
    "SILVER": "SI=F",
    "USD/INR": "INR=X",
    "US 10Y YIELD": "^TNX"
}

cols = st.columns(4)

i = 0

for name, ticker in indices.items():

    try:
        data = yf.download(ticker, period="5d", progress=False)

        latest = float(data['Close'].iloc[-1])
        prev = float(data['Close'].iloc[-2])

        change = latest - prev
        pct = (change / prev) * 100

        cols[i % 4].metric(
            name,
            round(latest,2),
            f"{round(pct,2)}%"
        )

        i += 1

    except:
        pass

st.divider()

st.subheader("🧠 Market Interpretation")

st.info(
    '''
    This dashboard tracks global risk sentiment across equities,
    commodities, currencies, and bond markets.

    Rising yields + rising dollar generally pressure equities.

    Strong crude supports energy stocks but hurts import-heavy sectors.

    Global indices strength helps bullish momentum in Indian equities.
    '''
)
