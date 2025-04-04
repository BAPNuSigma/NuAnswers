import streamlit as st
import requests
import json

st.title("NuAnswers: Beta Alpha Psi - Nu Sigma Chapter's AI Tutor Bot")
st.write("Welcome to your Accounting & Finance Tutor! I'm here to help you understand concepts and work through problems.")

# Initialize session state for conversation flow
if 'conversation_state' not in st.session_state:
    st.session_state.conversation_state = 'initial'
    st.session_state.current_topic = None

# Topic selection
if st.session_state.conversation_state == 'initial':
    st.write("I can help you with:")
    topics = ["Accounting Equation", "Financial Ratios", "Financial Statements", "Time Value of Money"]
    selected_topic = st.radio("Select a topic you'd like to work on:", topics)
    
    if st.button("Start Learning"):
        st.session_state.current_topic = selected_topic
        st.session_state.conversation_state = 'topic_selected'
        st.experimental_rerun()

# Problem-focused interaction
elif st.session_state.conversation_state == 'topic_selected':
    st.write(f"Great choice! Let's work on {st.session_state.current_topic}.")
    st.write("What specific problem or concept are you struggling with?")
    
    user_input = st.text_input("Describe your question or problem:")
    if st.button("Get Help"):
        if user_input:
            try:
                response = requests.post("https://nuanswers.onrender.com/chat", 
                                      json={"message": user_input},
                                      headers={"Content-Type": "application/json"})
                
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
            st.warning("Please describe your question or problem!")

    if st.button("Choose a Different Topic"):
        st.session_state.conversation_state = 'initial'
        st.session_state.current_topic = None
        st.experimental_rerun()
