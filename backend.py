# backend.py — Model loading, text cleaning, prediction logic

import re, pickle

with open("emotion_model.pkl", "rb") as f:
    model = pickle.load(f)

EMOTIONS = {
    "happy":   ("😊", "HAPPY",   "#FF8533", "The review has a positive, joyful tone."),
    "sad":     ("😢", "SAD",     "#4A90D9", "The review has a sorrowful or moved tone."),
    "angry":   ("😠", "ANGRY",   "#E84040", "The review has a frustrated or furious tone."),
    "neutral": ("😐", "NEUTRAL", "#8A9BB5", "The review is factual with no strong feeling."),
}

def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"\[name\]|\[removed\]", "", text)
    text = re.sub(r"@\w+", "", text)
    text = re.sub(r"[^\w\s!?.,'\"-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()

def predict(review):
    label = model.predict([clean_text(review)])[0]
    return EMOTIONS[label]


