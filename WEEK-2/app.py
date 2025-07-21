import os
import openai
import streamlit as st
from dotenv import load_dotenv
import datetime

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

LOG_FILE = "log_streamlit.txt"

def log_message(role: str, content: str):
    """Append messages to log file with timestamps."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{datetime.datetime.now()}] {role.upper()}: {content}\n")

# Streamlit Page Config
st.set_page_config(page_title="AI Chatbot (Week 2)", layout="centered")
st.title("AI Chatbot (Week 2)")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "current_prompt" not in st.session_state:
    st.session_state.current_prompt = "You are a helpful assistant."

# Sidebar to change system prompt
st.sidebar.header("Settings")
new_prompt = st.sidebar.text_area("System Prompt", value=st.session_state.current_prompt, height=120)
if st.sidebar.button("Apply Prompt"):
    st.session_state.current_prompt = new_prompt.strip()
    st.session_state.messages = [{"role": "system", "content": st.session_state.current_prompt}]
    log_message("system", st.session_state.current_prompt)
    st.sidebar.success("System prompt updated.")

# Conversation display
st.subheader("Conversation")
for msg in st.session_state.messages:
    if msg["role"] == "system":
        st.markdown(f"*System Prompt:* `{msg['content']}`")
    elif msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**Assistant:** {msg['content']}")

# User input with chat_input to clear after submission
user_input = st.chat_input("Your message:")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    log_message("user", user_input)

    with st.spinner("Generating response..."):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=st.session_state.messages,
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.messages.append({"role": "assistant", "content": reply})
            log_message("assistant", reply)
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")
            log_message("error", str(e))
