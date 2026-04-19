import os
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# 1. Load data
# Make sure intents.csv is in the same folder as this script
df = pd.read_csv("model/data/intents.csv")

# 2. Build Pipeline
# We keep ngram_range=(1, 2) to catch phrases like "reset password"
pipeline = Pipeline([
    ("vect", CountVectorizer(ngram_range=(1, 2))),
    ("clf", MultinomialNB())
])

# 3. Train
pipeline.fit(df["text"], df["label"])

# 4. Save
os.makedirs("model/artifacts", exist_ok=True)
joblib.dump(pipeline, "model/artifacts/intent_model.pkl")

print(f"✅ Model trained with {len(df)} samples across {len(df['label'].unique())} categories.")