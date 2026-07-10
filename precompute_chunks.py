# save as precompute_chunks.py
import pandas as pd
from transformers import pipeline
from tqdm import tqdm

print("Loading FinBERT...")
sentiment_pipeline = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert",
    top_k=None
)

def chunk_text(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

df = pd.read_csv("transcripts_clean.csv")
df["date"] = pd.to_datetime(df["date"])
df["quarter"] = df["date"].dt.to_period("Q").astype(str)

records = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    chunks = chunk_text(row["combined_text"])
    for i, chunk in enumerate(chunks):
        result = sentiment_pipeline(chunk[:512], truncation=True)
        scores = {item["label"]: item["score"] for item in result[0]}
        records.append({
            "company": row["company"],
            "quarter": row["quarter"],
            "chunk_num": i + 1,
            "positive": scores.get("positive", 0),
            "negative": scores.get("negative", 0),
            "neutral": scores.get("neutral", 0)
        })

chunk_df = pd.DataFrame(records)
chunk_df.to_csv("chunk_sentiments.csv", index=False)
print(f"Saved {len(chunk_df)} chunk records.")# save as precompute_chunks.py
import pandas as pd
from transformers import pipeline
from tqdm import tqdm

print("Loading FinBERT...")
sentiment_pipeline = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert",
    top_k=None
)

def chunk_text(text, chunk_size=400):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

df = pd.read_csv("transcripts_clean.csv")
df["date"] = pd.to_datetime(df["date"])
df["quarter"] = df["date"].dt.to_period("Q").astype(str)

records = []
for _, row in tqdm(df.iterrows(), total=len(df)):
    chunks = chunk_text(row["combined_text"])
    for i, chunk in enumerate(chunks):
        result = sentiment_pipeline(chunk[:512], truncation=True)
        scores = {item["label"]: item["score"] for item in result[0]}
        records.append({
            "company": row["company"],
            "quarter": row["quarter"],
            "chunk_num": i + 1,
            "positive": scores.get("positive", 0),
            "negative": scores.get("negative", 0),
            "neutral": scores.get("neutral", 0)
        })

chunk_df = pd.DataFrame(records)
chunk_df.to_csv("chunk_sentiments.csv", index=False)
print(f"Saved {len(chunk_df)} chunk records.")