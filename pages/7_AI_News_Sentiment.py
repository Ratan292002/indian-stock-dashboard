import streamlit as st
import yfinance as yf
import pandas as pd

st.title("📰 AI News & Sentiment Engine")

st.caption("Real-Time Market Narrative Intelligence")

# ----------------------------------------
# NEWS STOCKS
# ----------------------------------------

stocks = {
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS",
    "HDFCBANK.NS",
    "ICICIBANK.NS",
    "SBIN.NS",
    "LT.NS",
    "ITC.NS",
    "TATAMOTORS.NS",
    "POLYCAB.NS"
}

all_news = []

# ----------------------------------------
# FETCH NEWS
# ----------------------------------------

for symbol in stocks:

    try:

        ticker = yf.Ticker(symbol)

        news = ticker.news

        for item in news[:5]:

            title = item.get("title", "")

            publisher = item.get("publisher", "")

            link = item.get("link", "")

            # --------------------------------
            # BASIC SENTIMENT ENGINE
            # --------------------------------

            bullish_words = [
                "growth",
                "profit",
                "strong",
                "record",
                "surge",
                "beat",
                "expansion",
                "bullish"
            ]

            bearish_words = [
                "fall",
                "decline",
                "weak",
                "loss",
                "drop",
                "concern",
                "risk",
                "slowdown"
            ]

            bullish_score = 0
            bearish_score = 0

            title_lower = title.lower()

            for word in bullish_words:

                if word in title_lower:
                    bullish_score += 1

            for word in bearish_words:

                if word in title_lower:
                    bearish_score += 1

            # -------------------------------
            # SENTIMENT CLASSIFICATION
            # -------------------------------

            if bullish_score > bearish_score:
                sentiment = "🟢 Bullish"

            elif bearish_score > bullish_score:
                sentiment = "🔴 Bearish"

            else:
                sentiment = "🟡 Neutral"

            all_news.append({
                "Stock": symbol.replace(".NS",""),
                "Headline": title,
                "Publisher": publisher,
                "Sentiment": sentiment,
                "Link": link
            })

    except:
        pass

# ----------------------------------------
# NEWS TABLE
# ----------------------------------------

news_df = pd.DataFrame(all_news)

if not news_df.empty:

    st.subheader("🔥 Market News Feed")

    st.dataframe(
        news_df,
        use_container_width=True
    )

# ----------------------------------------
# MARKET SENTIMENT SUMMARY
# ----------------------------------------

if not news_df.empty:

    bullish_count = (
        news_df['Sentiment']
        == "🟢 Bullish"
    ).sum()

    bearish_count = (
        news_df['Sentiment']
        == "🔴 Bearish"
    ).sum()

    neutral_count = (
        news_df['Sentiment']
        == "🟡 Neutral"
    ).sum()

    st.subheader("🌍 Market Sentiment Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Bullish Headlines",
        bullish_count
    )

    col2.metric(
        "Bearish Headlines",
        bearish_count
    )

    col3.metric(
        "Neutral Headlines",
        neutral_count
    )

# ----------------------------------------
# AI INTERPRETATION
# ----------------------------------------

st.divider()

st.subheader("🧠 AI Narrative Engine")

if not news_df.empty:

    if bullish_count > bearish_count:
        narrative = '''
        Current news flow indicates a moderately bullish
        market narrative.

        Positive headlines dominate sentiment and may support
        risk appetite and momentum continuation.
        '''

    elif bearish_count > bullish_count:
        narrative = '''
        Current news flow reflects rising caution
        and defensive sentiment.

        Market participants may reduce risk exposure
        in weaker sectors.
        '''

    else:
        narrative = '''
        Market sentiment remains balanced with mixed
        narratives across sectors.

        Selective stock-specific opportunities may dominate.
        '''

    st.info(narrative)

# ----------------------------------------
# FOOTER
# ----------------------------------------

st.divider()

st.caption(
    "AI-powered market narrative intelligence"
)
