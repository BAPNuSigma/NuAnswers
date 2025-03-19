import streamlit as st
import requests

st.title("NuAnswers: Beta Alpha Psi - Nu Sigma Chapter's AI Tutor Bot")
st.write("Ask the AI Tutor any question!")

user_input = st.text_input("Your Question:")
if st.button("Get Answer"):
    if user_input:
        response = requests.post("https://nuanswers.onrender.com/chat", json={"message": user_input})
        st.write("Tutor Bot:", response.json().get("response"))
    else:
        st.warning("Please enter a question!")
