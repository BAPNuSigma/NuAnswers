import streamlit as st
import requests
import json

st.title("NuAnswers: Beta Alpha Psi - Nu Sigma Chapter's AI Tutor Bot")
st.write("Ask the AI Tutor any question!")

user_input = st.text_input("Your Question:")
if st.button("Get Answer"):
    if user_input:
        try:
            response = requests.post("https://nuanswers.onrender.com/chat", 
                                  json={"message": user_input},
                                  headers={"Content-Type": "application/json"})
            
            # Check if response is successful
            response.raise_for_status()
            
            try:
                response_data = response.json()
                tutor_response = response_data.get("response", "I apologize, but I couldn't process that response.")
                st.write("Tutor Bot:", tutor_response)
            except json.JSONDecodeError as e:
                st.error("I apologize, but I received an invalid response format. Please try again.")
                st.write("Debug info:", str(e))
        except requests.exceptions.RequestException as e:
            st.error("I apologize, but I couldn't connect to the tutor service. Please try again later.")
            st.write("Debug info:", str(e))
    else:
        st.warning("Please enter a question!")
