# train_balanced_model.py 🚀

import pandas as pd
import pickle
from sklearn.utils import resample
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

# ==============================
# 📥 LOAD DATA
# ==============================

df = pd.read_csv("reviews.csv")

# ==============================
# ⚖️ BALANCE DATA (10k each)
# ==============================

target_size = 10000

balanced_df = []

for emotion in df["emotion"].unique():
    subset = df[df["emotion"] == emotion]
    
    # Upsample or downsample
    subset_balanced = resample(
        subset,
        replace=True,        # allows oversampling
        n_samples=target_size,
        random_state=42
    )
    
    balanced_df.append(subset_balanced)

df_balanced = pd.concat(balanced_df)

print("Balanced dataset:")
print(df_balanced["emotion"].value_counts(), "\n")

# ==============================
# 🧠 TRAIN MODEL (PIPELINE)
# ==============================

X = df_balanced["review"]
y = df_balanced["emotion"]

model = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LinearSVC())
])

print("Training model...")
model.fit(X, y)

# ==============================
# 💾 SAVE MODEL
# ==============================

with open("emotion_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("New balanced model saved!\n")