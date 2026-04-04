import streamlit as st
from backend import predict  # reuse your backend 🔥

st.set_page_config(page_title="Movie Emotion Classifier")

st.title("🎬 Movie Emotion Classifier")
st.write("Enter a movie review and detect emotion")

user_input = st.text_area("Write your review:")

if st.button("Predict"):
    if user_input.strip():
        emoji, label, color, desc = predict(user_input)

        st.markdown(f"## {emoji} {label}")
        st.write(desc)
    else:
        st.warning("Please enter a review")