import pandas as pd
from app import preprocess_text, load_model, download_nltk_resources

print("Downloading NLTK...")
download_nltk_resources()

print("Loading model...")
classifier = load_model()

print("Loading evaluation.csv...")
df = pd.read_csv("Data/Data/evaluation.csv")
print(f"Loaded {len(df)} rows.")

for i, row in df.head(3).iterrows():
    raw_text = row['content']
    cleaned_text = preprocess_text(raw_text)
    
    truncated_text = cleaned_text[:2000]
    result = classifier(truncated_text)
    predicted_class = result[0]['label']
    
    print(f"--- Row {i} ---")
    print(f"Raw Text: {raw_text[:100]}...")
    print(f"Cleaned: {cleaned_text[:100]}...")
    print(f"Predicted Class: {predicted_class}")
    
print("Test completed successfully.")
