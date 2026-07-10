import pandas as pd
from transformers import pipeline
import ast

print("Loading FinBERT model...")
sentiment_pipeline = pipeline(
    "text-classification",
    model="ProsusAI/finbert",
    tokenizer="ProsusAI/finbert",
    top_k=None
)

def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def get_sentiment_score(text):
    chunks = chunk_text(text)
    all_scores = {"positive": [], "negative": [], "neutral": []}
    
    for chunk in chunks:
        results = sentiment_pipeline(chunk[:512], truncation=True)
        for item in results[0]:
            all_scores[item["label"]].append(item["score"])
    
    avg = {k: sum(v)/len(v) for k, v in all_scores.items() if v}
    dominant = max(avg, key=avg.get)
    return dominant, avg.get("positive", 0), avg.get("negative", 0), avg.get("neutral", 0)

# Load data
df = pd.read_csv("transcripts_clean.csv")

# Run on full dataset with progress tracking
print("Running on full dataset...")
from tqdm import tqdm
tqdm.pandas()

def get_sentiment_row(text):
    return get_sentiment_score(text)

results = []
for idx, row in tqdm(df.iterrows(), total=len(df)):
    sentiment, pos, neg, neu = get_sentiment_score(row["combined_text"])
    results.append({
        "company": row["company"],
        "date": row["date"],
        "filename": row["filename"],
        "sentiment": sentiment,
        "positive_score": pos,
        "negative_score": neg,
        "neutral_score": neu
    })

results_df = pd.DataFrame(results)
results_df.to_csv("sentiment_results.csv", index=False)
print("\nDone. Saved to sentiment_results.csv")
print(results_df["sentiment"].value_counts())