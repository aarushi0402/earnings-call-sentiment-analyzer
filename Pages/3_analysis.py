import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import inject_css, metric_cards

st.set_page_config(page_title="Cross-Company Analysis", page_icon="📉", layout="wide")
inject_css()

st.title("📉 Cross-Company Analysis")
st.markdown("Comparing sentiment trends and correlation with stock price movement across companies")
st.markdown("---")

@st.cache_data
def load_data():
    df = pd.read_csv("final_data.csv")
    df["date"] = pd.to_datetime(df["date"])
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    return df

df = load_data()

companies = st.multiselect("Select Companies", sorted(df["company"].unique()), default=sorted(df["company"].unique()))
filtered = df[df["company"].isin(companies)]

st.markdown("---")

st.subheader("Overall Correlation: Sentiment Delta vs Stock Movement")
clean = filtered.dropna(subset=["sentiment_delta", "stock_pct_change"])
if len(clean) > 3:
    corr, pval = stats.pearsonr(clean["sentiment_delta"], clean["stock_pct_change"])
    sig = "No" if pval > 0.05 else "Yes"
    sig_color = "#D50000" if pval > 0.05 else "#00C853"

    metric_cards([
        {"label": "Pearson r", "value": f"{corr:.4f}", "color": "#00C4B4"},
        {"label": "P-Value", "value": f"{pval:.4f}", "color": "#00C4B4"},
        {"label": "Statistically Significant", "value": sig, "color": sig_color},
    ])
    st.caption("r close to 0 means sentiment delta does not reliably predict stock movement — consistent with semi-strong market efficiency.")

st.markdown("---")

st.subheader("Scatter Plot")
fig = px.scatter(
    clean,
    x="sentiment_delta",
    y="stock_pct_change",
    color="company",
    hover_data=["company", "quarter", "positive_score", "sentiment_delta", "stock_pct_change"],
    labels={
        "sentiment_delta": "Sentiment Delta (QoQ Change in Positive Score)",
        "stock_pct_change": "Stock Price Change % (next trading day)",
        "company": "Company"
    },
    title=f"Sentiment Delta vs Stock Movement — Pearson r = {corr:.4f}"
)
fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.add_vline(x=0, line_dash="dash", line_color="gray", opacity=0.5)
fig.update_layout(
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("Per Company Breakdown")
rows = []
for company, group in filtered.groupby("company"):
    c = group.dropna(subset=["sentiment_delta", "stock_pct_change"])
    if len(c) > 3:
        r, p = stats.pearsonr(c["sentiment_delta"], c["stock_pct_change"])
        rows.append({
            "Company": company,
            "Pearson r": round(r, 4),
            "P-Value": round(p, 4),
            "Avg Sentiment Delta": round(c["sentiment_delta"].mean(), 4),
            "Risk Quarters (delta < -0.15)": int((c["sentiment_delta"] < -0.15).sum())
        })

table_df = pd.DataFrame(rows).sort_values("Pearson r", ascending=False).reset_index(drop=True)
st.dataframe(table_df, use_container_width=True)

st.markdown("---")

st.subheader("Sentiment Score Over Time")
company_choice = st.selectbox("Select Company", sorted(filtered["company"].unique()))
company_df = filtered[filtered["company"] == company_choice].sort_values("date")

fig2 = go.Figure()
fig2.add_trace(go.Scatter(
    x=company_df["date"], y=company_df["positive_score"],
    mode="lines+markers", name="Positive Score",
    line=dict(color="#00C853"),
    fill="tozeroy", fillcolor="rgba(0,200,83,0.1)"
))
fig2.add_trace(go.Scatter(
    x=company_df["date"], y=company_df["negative_score"],
    mode="lines+markers", name="Negative Score",
    line=dict(color="#D50000")
))

risk_quarters = company_df[company_df["sentiment_delta"] < -0.15]
for _, row in risk_quarters.iterrows():
    fig2.add_vline(
        x=row["date"].timestamp() * 1000,
        line_dash="dash", line_color="red",
        opacity=0.4,
        annotation_text="⚠️ Risk",
        annotation_position="top"
    )

fig2.update_layout(
    title=f"{company_choice} — Sentiment Over Time",
    xaxis_title="Date",
    yaxis_title="Score",
    height=400,
    hovermode="x unified",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)
st.plotly_chart(fig2, use_container_width=True)