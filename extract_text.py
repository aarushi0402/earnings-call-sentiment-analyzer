import os
import re
import pandas as pd

def clean_text(text):
    # Remove sync tags
    text = re.sub(r'<Sync id="[^"]+"/>', '', text)
    # Remove lines that are just dashes
    text = re.sub(r'-{3,}', '', text)
    # Remove bullet numbering like "1." "2." at start of lines
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def chunk_text(text, chunk_size=400):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

def extract_executive_text(text):
    text = re.sub(r'<Sync id="[^"]+"/>', '', text)
    blocks = re.split(r'-{80}\n', text)
    
    executive_text = []
    capture = False
    
    for block in blocks:
        block = block.strip()
        if re.search(r'\[\d+\]', block):
            is_executive = any(role in block for role in ['CEO', 'CFO', 'COO', 'President', 'Chairman'])
            is_analyst = 'Analyst' in block or 'Operator' in block
            capture = is_executive and not is_analyst
        elif capture and block:
            executive_text.append(block)
    
    return " ".join(executive_text).strip()

def extract_presentation(text):
    text = re.sub(r'<Sync id="[^"]+"/>', '', text)
    match = re.search(r'PRESENTATION SUMMARY.*?={3,}(.*?)={3,}', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return ""

# Load data
data_path = "data/Transcripts"
records = []

for company in os.listdir(data_path):
    company_path = f"{data_path}/{company}"
    for filename in os.listdir(company_path):
        filepath = f"{company_path}/{filename}"
        date_str = "-".join(filename.split("-")[:3])
        
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        
        presentation = extract_presentation(text)
        qa_executive = extract_executive_text(text)
        combined = clean_text(qa_executive)
        
        records.append({
            "company": company,
            "date": date_str,
            "filename": filename,
            "combined_text": combined.strip()
        })

df = pd.DataFrame(records)
df["date"] = pd.to_datetime(df["date"], format="%Y-%b-%d")
df = df.sort_values(["company", "date"]).reset_index(drop=True)

# Verify
sample = df[df["company"] == "AAPL"].iloc[0]
print("Company:", sample["company"])
print("Date:", sample["date"])
print("Text length:", len(sample["combined_text"]))

sample_chunks = chunk_text(sample["combined_text"])
print("Number of chunks for AAPL first transcript:", len(sample_chunks))
print("\nFirst chunk:\n", sample_chunks[0])

df.to_csv("transcripts_clean.csv", index=False)
print("\nSaved to transcripts_clean.csv")