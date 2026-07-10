import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from utils import inject_css

st.set_page_config(
    page_title="Earnings Call Sentiment Analyzer",
    page_icon="📈",
    layout="wide"
)
inject_css()

st.title("📈 Earnings Call Sentiment Analyzer")
st.markdown("---")

st.markdown("""
### What is this?
This tool analyzes sentiment in company earnings call transcripts using **FinBERT** — 
an NLP model trained specifically on financial language — and examines whether 
sentiment changes correlate with stock price movement.

### What's inside?
- **Explorer** — Browse pre-analyzed transcripts for 10 major tech companies (2016–2020)
- **Sentiment Timeline** — See how sentiment shifts chunk by chunk through a call
- **Cross-Company Analysis** — Compare sentiment trends and correlation with stock movement
- **Analyze New Transcript** — Paste any earnings call transcript and get instant sentiment analysis

### Key Finding
Sentiment delta (quarter-over-quarter change) shows no statistically significant 
correlation with next-day stock price movement (Pearson r = -0.047, p = 0.54) — 
consistent with the Efficient Market Hypothesis.
""")

st.info("👈 Use the sidebar to navigate between pages.")