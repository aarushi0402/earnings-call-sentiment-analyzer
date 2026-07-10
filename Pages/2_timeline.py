import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import inject_css

st.set_page_config(page_title="Sentiment Timeline", page_icon="📊", layout="wide")
inject_css()

st.title("📊 Sentiment Timeline")
st.markdown("See how sentiment shifts chunk by chunk through an earnings call")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv("final_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    return df

@st.cache_data
def load_chunks():
    return pd.read_csv("chunk_sentiments.csv")

df = load_data()
chunk_df_all = load_chunks()

col1, col2 = st.columns(2)
with col1:
    company = st.selectbox("Select Company", sorted(df["company"].unique()))
with col2:
    company_df = df[df["company"] == company].sort_values("date")
    quarter = st.selectbox("Select Quarter", company_df["quarter"].tolist())

chunk_df = chunk_df_all[
    (chunk_df_all["company"] == company) &
    (chunk_df_all["quarter"] == quarter)
].reset_index(drop=True)

if chunk_df.empty:
    st.error("No chunk data found for this selection.")
else:
    st.markdown(f"**{len(chunk_df)} chunks** of ~400 words each")
    st.markdown("---")

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=chunk_df["chunk_num"], y=chunk_df["positive"],
        mode="lines+markers", name="Positive",
        line=dict(color="#00C853"),
        fill="tozeroy", fillcolor="rgba(0,200,83,0.05)"
    ))
    fig.add_trace(go.Scatter(
        x=chunk_df["chunk_num"], y=chunk_df["negative"],
        mode="lines+markers", name="Negative",
        line=dict(color="#D50000")
    ))
    fig.add_trace(go.Scatter(
        x=chunk_df["chunk_num"], y=chunk_df["neutral"],
        mode="lines+markers", name="Neutral",
        line=dict(color="#9E9E9E")
    ))
    fig.update_layout(
        title=f"{company} {quarter} — Sentiment Through the Call",
        xaxis_title="Chunk Number (chronological order through the call)",
        yaxis_title="Sentiment Score",
        height=500,
        hovermode="x unified",
        yaxis=dict(range=[0, 1]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.subheader("Chunk-level Scores")
    st.dataframe(chunk_df[["chunk_num", "positive", "negative", "neutral"]].style.format({
        "positive": "{:.3f}",
        "negative": "{:.3f}",
        "neutral": "{:.3f}"
    }), use_container_width=True)