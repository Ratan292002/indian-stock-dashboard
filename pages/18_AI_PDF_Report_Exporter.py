import streamlit as st
import yfinance as yf
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.pagesizes import letter
from ta.trend import EMAIndicator
from ta.momentum import RSIIndicator
import tempfile

st.title("📄 AI PDF Research Report Exporter")

st.caption("Institutional Research Document Generator")

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

selected_stock = st.selectbox(
    "Select Stock",
    list(stocks.keys())
)

symbol = stocks[selected_stock]

# -----------------------------------------
# DATA
# -----------------------------------------

ticker = yf.Ticker(symbol)

info = ticker.info

df = yf.download(
    symbol,
    period="1y",
    progress=False
)

close = df['Close'].squeeze()

# -----------------------------------------
# METRICS
# -----------------------------------------

current_price = round(
    float(close.iloc[-1]),
    2
)

market_cap = info.get("marketCap", 0)

pe_ratio = info.get("trailingPE", 0)

pb_ratio = info.get("priceToBook", 0)

roe = info.get("returnOnEquity", 0)

debt_equity = info.get("debtToEquity", 0)

# -----------------------------------------
# TECHNICALS
# -----------------------------------------

ema20 = EMAIndicator(
    close=close,
    window=20
).ema_indicator()

ema50 = EMAIndicator(
    close=close,
    window=50
).ema_indicator()

rsi = RSIIndicator(
    close=close
).rsi()

# -----------------------------------------
# SCORING
# -----------------------------------------

score = 0

if ema20.iloc[-1] > ema50.iloc[-1]:
    score += 25

if current_price > ema50.iloc[-1]:
    score += 20

if 50 < rsi.iloc[-1] < 70:
    score += 20

if pe_ratio and pe_ratio < 35:
    score += 15

if roe and roe > 0.15:
    score += 20

# -----------------------------------------
# RATING
# -----------------------------------------

if score >= 80:
    rating = "High Conviction"

elif score >= 60:
    rating = "Positive"

elif score >= 40:
    rating = "Neutral"

else:
    rating = "Weak"

# -----------------------------------------
# PDF GENERATOR
# -----------------------------------------

if st.button("Generate PDF Report"):

    temp_pdf = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".pdf"
    )

    doc = SimpleDocTemplate(
        temp_pdf.name,
        pagesize=letter
    )

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        f"{selected_stock} AI Research Report",
        styles['Title']
    )

    content.append(title)

    content.append(Spacer(1,12))

    overview = Paragraph(
        f'''
        <b>Current Price:</b> ₹{current_price}<br/>
        <b>AI Rating:</b> {rating}<br/>
        <b>Conviction Score:</b> {score}/100
        ''',
        styles['BodyText']
    )

    content.append(overview)

    content.append(Spacer(1,12))

    fundamentals = Paragraph(
        f'''
        <b>Market Cap:</b> {market_cap}<br/>
        <b>P/E Ratio:</b> {pe_ratio}<br/>
        <b>P/B Ratio:</b> {pb_ratio}<br/>
        <b>ROE:</b> {roe}<br/>
        <b>Debt/Equity:</b> {debt_equity}
        ''',
        styles['BodyText']
    )

    content.append(fundamentals)

    content.append(Spacer(1,12))

    commentary = Paragraph(
        f'''
        The AI engine currently classifies
        {selected_stock} as a {rating} setup.

        Analysis includes:
        • technical structure
        • momentum quality
        • valuation profile
        • capital efficiency
        • balance sheet analysis

        Institutional-style analytics prioritize:
        • probability
        • risk-adjusted returns
        • trend persistence
        • participation quality
        ''',
        styles['BodyText']
    )

    content.append(commentary)

    content.append(PageBreak())

    risk = Paragraph(
        '''
        Risk Factors:
        • market volatility
        • macro uncertainty
        • sector rotation
        • earnings risk
        • liquidity shocks

        Educational use only.
        ''',
        styles['BodyText']
    )

    content.append(risk)

    doc.build(content)

    with open(temp_pdf.name, "rb") as pdf_file:

        st.download_button(
            label="📥 Download PDF Report",
            data=pdf_file,
            file_name=f"{selected_stock}_AI_Report.pdf",
            mime="application/pdf"
        )

    st.success(
        "Institutional PDF report generated successfully!"
    )

# -----------------------------------------
# PREVIEW
# -----------------------------------------

st.subheader("🧠 Report Preview")

st.info(
    '''
    Generated reports include:
    
    • AI conviction rating
    
    • valuation metrics
    
    • technical structure
    
    • institutional commentary
    
    • risk analysis
    
    • printable research format
    
    This replicates institutional-style
    research workflows.
    '''
)

# -----------------------------------------
# FOOTER
# -----------------------------------------

st.divider()

st.caption(
    "AI institutional PDF research generation"
)
