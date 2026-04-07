import streamlit as st
import requests
import uuid
import os

# 1. Configuration
# We use standard environment variables to check if we are in Docker
BACKEND_URL = "http://api:8000" if os.environ.get("DOCKER") == "true" else "http://localhost:8000"

st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

# 2. Session ID Management
# We generate a unique ID for the session if it doesn't exist.
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 3. Sidebar Configuration
with st.sidebar:
    st.title("Settings ⚙️")
    st.text(f"Session ID: {st.session_state.session_id}")
    
    if st.button("Clear History 🗑️"):
        try:
            response = requests.delete(f"{BACKEND_URL}/history/{st.session_state.session_id}")
            if response.status_code == 200:
                st.session_state.messages = []
                st.success("History cleared!")
                st.rerun()
        except Exception as e:
            st.error(f"Error clearing history: {e}")

    # Health Check Indicator
    try:
        health = requests.get(f"{BACKEND_URL}/health").json()
        if health.get("status") == "ok":
            st.success("Backend: Online ✅")
    except:
        st.error("Backend: Offline ❌")

st.title("AI Chatbot 🤖")
st.caption("A ChatGPT-style conversational AI powered by Gemini and FastAPI.")

# 4. Fetch History on Initial Load
if "messages" not in st.session_state:
    try:
        response = requests.get(f"{BACKEND_URL}/history/{st.session_state.session_id}")
        if response.status_code == 200:
            history = response.json().get("history", [])
            # Map history format to Streamlit chat message format
            st.session_state.messages = [
                {"role": m["role"], "content": m["content"]} for m in history
            ]
        else:
            st.session_state.messages = []
    except:
        st.session_state.messages = []

# 5. Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Input Logic
if prompt := st.chat_input("What is on your mind?"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call FastAPI backend for AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 🤔")
        
        try:
            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={"session_id": st.session_state.session_id, "message": prompt}
            )
            
            if response.status_code == 200:
                full_response = response.json().get("reply", "No response received.")
                message_placeholder.markdown(full_response)
                # Save assistant response to session state
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
                
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
