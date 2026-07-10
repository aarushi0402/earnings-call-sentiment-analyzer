# 📈 Earnings Call Sentiment Analyzer

> An AI-powered NLP tool that analyzes sentiment in company earnings call transcripts using **FinBERT** and studies its correlation with stock price movement.

Built during my summer internship at **Sopra Steria** (June–July 2026).

---

## 🎬 Demo

[![Dashboard Demo](https://img.youtube.com/vi/Gbd8vFtCuzc/maxresdefault.jpg)](https://youtu.be/Gbd8vFtCuzc)

*Click the thumbnail to watch the full dashboard walkthrough*

---

## 🔍 What It Does

Every quarter, companies like Apple, Microsoft, and NVIDIA hold earnings calls where executives discuss financial performance. The language they use influences investor sentiment and stock prices.

This project:
- **Extracts** executive speech from earnings call transcripts (CEO/CFO Q&A responses only)
- **Analyzes** sentiment using FinBERT — a BERT model fine-tuned on financial language
- **Correlates** quarter-over-quarter sentiment changes with next-day stock price movement
- **Visualizes** findings through an interactive Streamlit dashboard

---

## 📊 Key Finding

> Sentiment delta (quarter-over-quarter change) shows **no statistically significant correlation** with next-day stock price movement across 178 earnings calls from 10 major NASDAQ tech companies (Pearson r = -0.047, p = 0.535).

This null result is consistent with the **semi-strong form of the Efficient Market Hypothesis** — sentiment cues are already priced in through other channels before markets react. The one exception: Intel (INTC) showed a statistically significant *negative* correlation (r = -0.607, p = 0.008), suggesting a possible "sell the news" pattern.

---

## 🗂️ Dashboard Pages

| Page | Description |
|------|-------------|
| 🔍 **Explorer** | Browse pre-analyzed transcripts by company and quarter. View sentiment scores, risk flags, and historical sentiment trends |
| 📊 **Timeline** | Chunk-by-chunk sentiment visualization showing how executive tone shifts through a call |
| 📉 **Analysis** | Cross-company correlation analysis with interactive scatter plot and per-company breakdown |
| 🔬 **Analyze New** | Paste any earnings call transcript and get instant FinBERT sentiment analysis |

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.11 |
| NLP Model | FinBERT (ProsusAI/finbert) |
| ML Framework | HuggingFace Transformers 4.40.0 |
| Deep Learning | PyTorch |
| Stock Data | yfinance (Yahoo Finance API) |
| Data Processing | Pandas, NumPy |
| Statistics | SciPy (Pearson correlation) |
| Visualization | Plotly |
| Dashboard | Streamlit 1.59.0 |
| Dataset | Kaggle — NASDAQ Earnings Calls 2016–2020 |

---

## 📁 Project Structure

```
earnings-analyzer/
├── app.py                    # Main entry point (landing page)
├── utils.py                  # Shared CSS and card components
├── Pages/
│   ├── 1_Explorer.py         # Transcript Explorer
│   ├── 2_Timeline.py         # Sentiment Timeline
│   ├── 3_Analysis.py         # Cross-Company Analysis
│   └── 4_Analyze.py          # Analyze New Transcript
├── load_data.py              # Loads and structures raw transcripts
├── extract_text.py           # Extracts executive Q&A text
├── sentiment.py              # Runs FinBERT on all transcripts
├── precompute_chunks.py      # Precomputes chunk-level sentiments
├── stock_prices.py           # Fetches stock data and computes delta
├── analyze.py                # Correlation analysis
├── transcripts_clean.csv     # Cleaned executive-only text
├── sentiment_results.csv     # FinBERT scores per transcript
├── chunk_sentiments.csv      # Chunk-level scores for timeline
└── final_data.csv            # Combined sentiment + stock data
```

---

## 🚀 How to Run

### Prerequisites
- Python 3.11
- Download the dataset from [Kaggle](https://www.kaggle.com/datasets/ashwinm500/earnings-call-transcripts) and place it in `data/Transcripts/`

### Setup

```bash
# Clone the repo
git clone https://github.com/aarushi0402/earnings-call-sentiment-analyzer.git
cd earnings-call-sentiment-analyzer

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install pandas yfinance transformers==4.40.0 torch requests streamlit matplotlib scipy tqdm plotly
```

### Run the Pipeline (First Time)

```bash
python load_data.py           # Load transcripts
python extract_text.py        # Extract executive Q&A
python sentiment.py           # Run FinBERT (~15 mins)
python precompute_chunks.py   # Precompute chunk sentiments
python stock_prices.py        # Fetch stock data
python analyze.py             # Run correlation analysis
streamlit run app.py          # Launch dashboard
```

### Run Dashboard Only (if CSVs already generated)

```bash
streamlit run app.py
```

---

## 📈 Dataset

- **Source:** [Kaggle — Earnings Call Transcripts NASDAQ 2016-2020](https://www.kaggle.com/datasets/ashwinm500/earnings-call-transcripts)
- **Companies:** AAPL, AMD, AMZN, ASML, CSCO, GOOGL, INTC, MSFT, MU, NVDA
- **Transcripts:** 188 earnings calls (2016 Q1 – 2020 Q3)
- **Final observations:** 178 (after filtering for valid stock data and delta calculation)

---

## 🔬 Methodology

### Why executive Q&A only?
Three text sections were evaluated:
- **Overview** — rejected (written by Thomson Reuters analysts, not management)
- **Presentation Summary** — rejected after testing (bullet-point fragments, not natural prose)
- **Q&A executive responses** — chosen (natural spoken language, unscripted, captures real management tone)

### Why sentiment delta instead of raw scores?
110 out of 188 transcripts (58.5%) were labeled "positive" by FinBERT — not enough variation for meaningful correlation. Sentiment delta (QoQ change in positive score) captures whether tone is improving or declining, which is a far stronger signal.

### Risk Flag
Transcripts with `sentiment_delta < -0.15` are flagged as significant sentiment declines — a heuristic risk signal visible in the Explorer and Analysis pages.

---

## ⚠️ Limitations

- Dataset limited to 2016–2020 and 10 NASDAQ companies
- FinBERT's 512-token limit requires chunking; chunk averaging may dilute segment-specific signals
- Earnings surprises (beat vs miss vs expectations) not controlled for
- Speaker diarization is rule-based — edge cases may be missed
- Stock price window (next trading day) may not capture full market reaction

---

## 👩‍💻 Author

**Aarushi Khanna**
Manipal University Jaipur | BTech 2028
Summer Intern @ Sopra Steria (June–July 2026)

---

## 📄 License

This project is for educational and research purposes as part of an internship at Sopra Steria.
