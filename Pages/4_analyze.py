import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from transformers import pipeline
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import inject_css, metric_cards

st.set_page_config(page_title="Analyze New Transcript", page_icon="🔬", layout="wide")
inject_css()

@st.cache_resource
def load_model():
    return pipeline(
        "text-classification",
        model="ProsusAI/finbert",
        tokenizer="ProsusAI/finbert",
        top_k=None
    )

def chunk_text(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

def analyze_transcript(text, model):
    chunks = chunk_text(text)
    results = []
    for i, chunk in enumerate(chunks):
        output = model(chunk[:512], truncation=True)
        scores = {item["label"]: item["score"] for item in output[0]}
        results.append({
            "chunk": i + 1,
            "positive": scores.get("positive", 0),
            "negative": scores.get("negative", 0),
            "neutral": scores.get("neutral", 0)
        })
    return pd.DataFrame(results)

st.title("🔬 Analyze New Transcript")
st.markdown("Paste any earnings call transcript and get instant FinBERT sentiment analysis")
st.markdown("---")

st.info("ℹ️ Sentiment delta (quarter-over-quarter change) is not available for new transcripts — that requires historical data. You will see absolute sentiment scores only.")

transcript_text = st.text_area(
    "Paste transcript text here",
    height=300,
    placeholder="Paste the executive Q&A or prepared remarks from any earnings call..."
)

if st.button("Analyze", key="analyze_btn"):
    if not transcript_text.strip():
        st.warning("Please paste a transcript before analyzing.")
    else:
        with st.spinner("Loading FinBERT and analyzing..."):
            model = load_model()
            chunk_df = analyze_transcript(transcript_text, model)

        st.markdown("---")

        avg_positive = chunk_df["positive"].mean()
        avg_negative = chunk_df["negative"].mean()
        avg_neutral = chunk_df["neutral"].mean()
        dominant = max(["positive", "negative", "neutral"], key=lambda x: chunk_df[x].mean())
        dominant_color = {"positive": "#00C853", "negative": "#D50000", "neutral": "#9E9E9E"}[dominant]

        metric_cards([
            {"label": "Avg Positive Score", "value": f"{avg_positive:.3f}", "color": "#00C853"},
            {"label": "Avg Negative Score", "value": f"{avg_negative:.3f}", "color": "#D50000"},
            {"label": "Avg Neutral Score", "value": f"{avg_neutral:.3f}", "color": "#9E9E9E"},
            {"label": "Dominant Sentiment", "value": dominant.capitalize(), "color": dominant_color},
        ])

        if avg_negative > 0.3:
            st.error("⚠️ High negative sentiment detected in this transcript")
        elif avg_negative > 0.15:
            st.warning("📉 Elevated negative sentiment detected")
        else:
            st.success("✅ Sentiment appears stable or positive")

        st.markdown("---")

        st.subheader("Overall Sentiment Breakdown")
        fig_bar = go.Figure(go.Bar(
            x=["Positive", "Negative", "Neutral"],
            y=[avg_positive, avg_negative, avg_neutral],
            marker_color=["#00C853", "#D50000", "#9E9E9E"],
            text=[f"{avg_positive:.3f}", f"{avg_negative:.3f}", f"{avg_neutral:.3f}"],
            textposition="outside"
        ))
        fig_bar.update_layout(
            yaxis=dict(range=[0, 1]),
            height=350,
            showlegend=False,
            yaxis_title="Score",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("---")

        st.subheader("Sentiment Timeline Through the Transcript")
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chunk_df["chunk"], y=chunk_df["positive"],
            mode="lines+markers", name="Positive",
            line=dict(color="#00C853"),
            fill="tozeroy", fillcolor="rgba(0,200,83,0.05)"
        ))
        fig.add_trace(go.Scatter(
            x=chunk_df["chunk"], y=chunk_df["negative"],
            mode="lines+markers", name="Negative",
            line=dict(color="#D50000")
        ))
        fig.add_trace(go.Scatter(
            x=chunk_df["chunk"], y=chunk_df["neutral"],
            mode="lines+markers", name="Neutral",
            line=dict(color="#9E9E9E")
        ))
        fig.update_layout(
            title="Sentiment Shift Through the Transcript",
            xaxis_title="Chunk Number",
            yaxis_title="Sentiment Score",
            height=450,
            hovermode="x unified",
            yaxis=dict(range=[0, 1]),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")
        st.subheader("Chunk-level Detail")
        st.dataframe(chunk_df.style.format({
            "positive": "{:.3f}",
            "negative": "{:.3f}",
            "neutral": "{:.3f}"
        }), use_container_width=True)