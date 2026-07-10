import os

data_path = "data/Transcripts"
companies = os.listdir(data_path)
print("Companies:", companies)
print("Total companies:", len(companies))

for company in companies:
    files = os.listdir(f"{data_path}/{company}")
    print(f"{company}: {len(files)} transcripts")