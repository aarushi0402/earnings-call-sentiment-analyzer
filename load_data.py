import os
import pandas as pd

data_path = "data/Transcripts"
records = []

for company in os.listdir(data_path):
    company_path = f"{data_path}/{company}"
    for filename in os.listdir(company_path):
        filepath = f"{company_path}/{filename}"
        
        # Extract date from filename e.g. 2016-Jan-26-AAPL.txt
        date_str = "-".join(filename.split("-")[:3])
        
        # Read transcript text
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        records.append({
            "company": company,
            "date": date_str,
            "filename": filename,
            "text": text
        })

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"], format="%Y-%b-%d")
df = df.sort_values(["company", "date"]).reset_index(drop=True)

print(df[["company", "date", "filename"]].head(20))
print("\nShape:", df.shape)
df.to_csv("transcripts.csv", index=False)
print("Saved to transcripts.csv")
