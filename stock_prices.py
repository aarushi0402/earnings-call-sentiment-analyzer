import pandas as pd
import yfinance as yf
from datetime import timedelta

df = pd.read_csv("sentiment_results.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values(["company", "date"]).reset_index(drop=True)

df["prev_positive_score"] = df.groupby("company")["positive_score"].shift(1)
df["sentiment_delta"] = df["positive_score"] - df["prev_positive_score"]

ticker_map = {
    "AAPL": "AAPL", "AMD": "AMD", "AMZN": "AMZN",
    "ASML": "ASML", "CSCO": "CSCO", "GOOGL": "GOOGL",
    "INTC": "INTC", "MSFT": "MSFT", "MU": "MU", "NVDA": "NVDA"
}

records = []
for _, row in df.iterrows():
    ticker = ticker_map[row["company"]]
    date = row["date"]
    start = date - timedelta(days=3)
    end = date + timedelta(days=5)

    try:
        hist = yf.download(ticker, start=start, end=end, progress=False)
        hist.index = pd.to_datetime(hist.index)

        # Fix for newer yfinance MultiIndex columns
        if isinstance(hist.columns, pd.MultiIndex):
            hist.columns = hist.columns.get_level_values(0)

        after = hist[hist.index >= date]
        before = hist[hist.index < date]

        if len(after) >= 2 and len(before) >= 1:
            price_before = float(before["Close"].iloc[-1])
            price_after = float(after["Close"].iloc[0])
            pct_change = ((price_after - price_before) / price_before) * 100
        else:
            pct_change = None

        records.append({
            "company": row["company"],
            "date": row["date"],
            "sentiment": row["sentiment"],
            "positive_score": row["positive_score"],
            "negative_score": row["negative_score"],
            "neutral_score": row["neutral_score"],
            "prev_positive_score": row["prev_positive_score"],
            "sentiment_delta": row["sentiment_delta"],
            "stock_pct_change": pct_change
        })

    except Exception as e:
        print(f"Error for {ticker} on {date}: {e}")

result_df = pd.DataFrame(records)
result_df.dropna(subset=["stock_pct_change", "sentiment_delta"], inplace=True)

print(result_df[["company", "date", "positive_score", "sentiment_delta", "stock_pct_change"]].head(15))
print("\nShape:", result_df.shape)
print("\nSentiment delta stats:")
print(result_df["sentiment_delta"].describe())

result_df.to_csv("final_data.csv", index=False)
print("\nSaved to final_data.csv")