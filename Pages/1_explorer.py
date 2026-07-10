import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import inject_css, metric_cards

st.set_page_config(page_title="Explorer", page_icon="🔍", layout="wide")
inject_css()

st.title("🔍 Transcript Explorer")
st.markdown("Browse pre-analyzed earnings call transcripts for 10 major tech companies (2016–2020)")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv("final_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    return df

df = load_data()

col1, col2 = st.columns(2)
with col1:
    company = st.selectbox("Select Company", sorted(df["company"].unique()))
with col2:
    company_sorted = df[df["company"] == company].sort_values("date").reset_index(drop=True)
    quarter = st.selectbox("Select Quarter", company_sorted["quarter"].tolist())

selected_idx = company_sorted[company_sorted["quarter"] == quarter].index[0]
row = company_sorted.iloc[selected_idx]
is_first = selected_idx == 0

st.markdown("---")

delta_display = "N/A" if is_first else f"{row['sentiment_delta']:.3f}"
delta_color = "#9E9E9E" if is_first else ("#00C853" if row['sentiment_delta'] >= 0 else "#D50000")
stock_color = "#00C853" if row['stock_pct_change'] >= 0 else "#D50000"

metric_cards([
    {"label": "Positive Score", "value": f"{row['positive_score']:.3f}", "color": "#00C853"},
    {"label": "Negative Score", "value": f"{row['negative_score']:.3f}", "color": "#D50000"},
    {"label": "Sentiment Delta (QoQ)", "value": delta_display, "color": delta_color},
    {"label": "Stock Change (next day)", "value": f"{row['stock_pct_change']:.2f}%", "color": stock_color},
])

st.markdown("---")

if is_first:
    st.info("ℹ️ This is the first available quarter for this company. Sentiment delta requires a previous quarter.")
else:
    delta = row["sentiment_delta"]
    if delta < -0.15:
        st.error("⚠️ Risk Flag: Significant sentiment decline detected this quarter (delta < -0.15)")
    elif delta < -0.05:
        st.warning("📉 Mild sentiment decline compared to previous quarter")
    else:
        st.success("✅ Sentiment stable or improving")

st.markdown("---")

st.subheader(f"{company} {quarter} — Sentiment Breakdown")
fig = go.Figure(go.Bar(
    x=["Positive", "Negative", "Neutral"],
    y=[row["positive_score"], row["negative_score"], row["neutral_score"]],
    marker_color=["#00C853", "#D50000", "#9E9E9E"],
    text=[f"{row['positive_score']:.3f}", f"{row['negative_score']:.3f}", f"{row['neutral_score']:.3f}"],
    textposition="outside"
))
fig.update_layout(
    yaxis=dict(range=[0, 1]),
    height=350,
    showlegend=False,
    yaxis_title="Score",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader(f"{company} — Sentiment History")
fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=company_sorted["quarter"], y=company_sorted["positive_score"],
    mode="lines+markers", name="Positive Score",
    line=dict(color="#00C853"),
    fill="tozeroy", fillcolor="rgba(0,200,83,0.1)"
))
fig2.add_trace(go.Scatter(
    x=company_sorted["quarter"], y=company_sorted["negative_score"],
    mode="lines+markers", name="Negative Score",
    line=dict(color="#D50000")
))
fig2.update_layout(
    height=350,
    xaxis_title="Quarter",
    yaxis_title="Score",
    hovermode="x unified",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Full History Table")
display_df = company_sorted[["quarter", "positive_score", "negative_score", "sentiment_delta", "stock_pct_change"]].copy()
display_df.columns = ["Quarter", "Positive Score", "Negative Score", "Sentiment Delta", "Stock Change %"]
display_df = display_df.sort_values("Quarter", ascending=False).reset_index(drop=True)
st.dataframe(display_df.style.format({
    "Positive Score": "{:.3f}",
    "Negative Score": "{:.3f}",
    "Sentiment Delta": "{:.3f}",
    "Stock Change %": "{:.2f}"
}), use_container_width=True)