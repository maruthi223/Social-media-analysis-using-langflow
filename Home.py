import streamlit as st
from datetime import datetime

import time 
from dotenv import load_dotenv
import requests
from typing import Optional
import json
import os

load_dotenv()

BASE_API_URL = "https://api.langflow.astra.datastax.com"
LANGFLOW_ID = "39cdaafa-cc9d-4659-9975-8bd02a62358f"
APPLICATION_TOKEN = os.getenv("LANGFLOW_TOKEN")

def get_macros(profile):
    TWEAKS = {
    }
    return run_flow(profile, tweaks=TWEAKS, application_token=APPLICATION_TOKEN)


def run_flow(message: str,
  output_type: str = "chat",
  input_type: str = "chat",
  tweaks: Optional[dict] = None,
  application_token: Optional[str] = None) -> dict:
    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/customer-1"

    payload = {
        "input_value": message,
        "output_type": output_type,
        "input_type": input_type,
    }
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    if application_token:
        headers = {"Authorization": "Bearer " + application_token, "Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    
    # return json.loads(response.json()["outputs"][0]["outputs"][0]["results"]["text"]["data"]["text"])
    return (response.json()['outputs'][0]['outputs'][0]['results']['message']['data']['text'])



st.set_page_config(page_title="PulseBot", page_icon=":robot_face:", layout="wide")

st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #6a11cb, #2575fc);  /* Gradient background */
            color: white;
            font-family: 'Arial', sans-serif;
            animation: fadeIn 2s ease-in-out;  /* Animation for fade-in effect */
        }
        @keyframes fadeIn {
            0% { opacity: 0; }
            100% { opacity: 1; }
        }
        .user { background-color: #ffffff; color: #1d1d1d; border-radius: 15px; padding: 10px; margin: 5px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .assistant { background-color: #d9f7be; color: #1d1d1d; border-radius: 15px; padding: 10px; margin: 5px 0; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); }
        .chat-container { max-width: 700px; margin: 0 auto; }
        .stChatInput input { border-radius: 10px; padding: 10px; font-size: 16px; }
        .stChatMessage { font-size: 16px; line-height: 1.6; }
        .stCaption { color: #888; font-style: italic; }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ["Home", "About", "Chat"])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Home Page (Default Page)
if page == "Home":
    st.title("Welcome to PulseBot :robot_face:")
    st.markdown("""
        **PulseBot** is your intelligent assistant designed to analyze engagement data from mock social media accounts.

        #### Key Features:
        - Analyze user engagement data in real-time.
        - Monitor social trends and activity.
        - Easy-to-use interface for streamlined data analysis.
        - Sidebar navigation for easy access to all sections.

        Use the **About** page to learn more or the **Chat** page to interact with PulseBot and explore insights!
    """)

# About Page
elif page == "About":
    st.title("About PulseBot")
    st.markdown("""
        **PulseBot** is an advanced chatbot built to analyze engagement data from mock social media accounts. It helps identify trends, interactions, and key metrics, making it an essential tool for social media analysts and marketers.

        #### Core Features:
        - Real-time engagement analysis from mock social media data.
        - Visualize trends, user interactions, and activity patterns.
        - Powered by AI for accurate and insightful responses.
        - Responsive and user-friendly design for easy navigation.

        Go to the **Chat** page to interact with PulseBot and start analyzing your social media data!
    """)

# Chat Page
elif page == "Chat":
    st.title("PulseBot Chat")

    with st.container():
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f'<div class="user">{message["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="assistant">{message["content"]}</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("How can I assist you with social media data analysis?"):
        st.markdown(f'<div class="user">{prompt}</div>', unsafe_allow_html=True)
        st.session_state.messages.append({"role": "user", "content": prompt})
        result_ai = get_macros(prompt)

        # Generate response and add a delay for effect
        response = f"Analyzing: {result_ai}..."
        with st.spinner("Generating response..."):
            time.sleep(1)  # Simulating delay for typing effect

        # Display assistant response
        st.markdown(f'<div class="assistant">{response}</div>', unsafe_allow_html=True)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

    st.write("---")
    st.caption(f"Chat initialized on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
