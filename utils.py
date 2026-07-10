import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }
    .stButton > button {
        background-color: #00C4B4;
        color: #0F1117;
        border: none;
        border-radius: 6px;
        padding: 10px 28px;
        font-weight: 700;
        font-size: 15px;
        transition: 0.2s;
    }
    .stButton > button:hover {
        background-color: #00A89A;
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #0D0F18;
        border-right: 1px solid #2D3250;
    }
    h2, h3 {
        color: #00C4B4 !important;
    }
    </style>
    """, unsafe_allow_html=True)

def metric_cards(metrics):
    """
    metrics: list of dicts with keys: label, value, color (optional)
    """
    cards_html = '<div style="display:flex; gap:16px; margin:20px 0;">'
    for m in metrics:
        color = m.get("color", "#FAFAFA")
        cards_html += f"""
        <div style="flex:1; background:#1E2130; border:1px solid #2D3250; border-radius:10px; padding:20px;">
            <div style="color:#9E9E9E; font-size:13px; margin-bottom:8px;">{m['label']}</div>
            <div style="color:{color}; font-size:32px; font-weight:700;">{m['value']}</div>
        </div>"""
    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)