import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load Environment Variables
load_dotenv()

# Configure Page
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS (ChatGPT Style)
st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

.chat-user {
    background-color: #1E293B;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

.chat-bot {
    background-color: #111827;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# Groq Client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

# Sidebar
with st.sidebar:

    st.title("🤖 AI Chatbot")

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")
    st.write("Made by vishnu")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Old Messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
prompt = st.chat_input("Type your message...")

# When User Sends Message
if prompt:

    # Save User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display User Message
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Response
    with st.chat_message("assistant"):

        message_placeholder = st.empty()

        full_response = ""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.messages,
            temperature=0.7,
            max_tokens=1024,
            stream=True
        )

        for chunk in completion:

            content = chunk.choices[0].delta.content or ""

            full_response += content

            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save AI Response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": full_response
        }
    )   