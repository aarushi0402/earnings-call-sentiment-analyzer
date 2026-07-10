import pandas as pd

df = pd.read_csv("transcripts_clean.csv")

# Show a sample of what FinBERT is actually reading
sample = df[df["company"] == "AAPL"].iloc[0]
text = sample["combined_text"]

words = text.split()
chunks = [" ".join(words[i:i+400]) for i in range(0, len(words), 400)]

print(f"Total chunks: {len(chunks)}")
print("\n--- CHUNK 1 (Presentation Summary) ---")
print(chunks[0])
print("\n--- CHUNK 6 (Should be Q&A executive speech) ---")
if len(chunks) > 6:
    print(chunks[6])
print("\n--- LAST CHUNK ---")
print(chunks[-1])