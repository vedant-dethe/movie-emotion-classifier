# model_analysis.py 🚀

import pandas as pd
import pickle
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

print("Loading dataset...")
df = pd.read_csv("reviews.csv")

print("Columns in dataset:", df.columns, "\n")

print("Loading model...")

with open("emotion_model.pkl", "rb") as f:
    model = pickle.load(f)

print("Model loaded!\n")

# ==============================
# ✅ USE RAW TEXT (IMPORTANT FIX)
# ==============================

X = df["review"]
y = df["emotion"]

print("Making predictions...")
predictions = model.predict(X)

# ==============================
# 📊 EVALUATION
# ==============================

print("\nMODEL PERFORMANCE\n")

accuracy = accuracy_score(y, predictions)
print(f"Accuracy: {accuracy * 100:.2f}%\n")

print("Confusion Matrix:")
print(confusion_matrix(y, predictions))

print("\nClassification Report:")
print(classification_report(y, predictions))

# ==============================
# 🧪 SAMPLE TESTING
# ==============================

print("\nSample Predictions:\n")

samples = [
    "This movie was amazing!",
    "I hated every second of it",
    "It was okay, nothing special",
    "Very emotional and touching film"
]

for text in samples:
    pred = model.predict([text])[0]
    print(f"Review: {text}")
    print(f"Predicted Emotion: {pred}\n")