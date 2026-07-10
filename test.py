with open("data/Transcripts/AAPL/2016-Jan-26-AAPL.txt", "r", encoding="utf-8", errors="ignore") as f:
    text = f.read()

# Find Q&A section and print first 3000 characters of it
qa_start = text.find("QUESTION AND ANSWER")
if qa_start == -1:
    qa_start = text.find("Q&A")
if qa_start == -1:
    qa_start = text.find("QUESTIONS AND ANSWERS")
    
print(text[qa_start:qa_start+3000])