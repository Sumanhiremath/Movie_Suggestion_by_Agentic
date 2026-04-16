import streamlit as st
import requests

st.set_page_config(page_title="Movie Chatbot", page_icon="🎬")

st.title("🎬 Movie Chatbot")

# -----------------------------
# 🔹 Initialize chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# 🔹 Display chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# 🔹 User input
# -----------------------------
user_input = st.chat_input("Ask me about movies...")

if user_input:

    # Show user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # -----------------------------
    # 🔹 Call backend
    # -----------------------------
    try:
        res = requests.post(
            "http://localhost:8000/chat",
            json={"query": user_input}
        )

        bot_reply = res.json()["response"]

    except Exception as e:
        bot_reply = f"⚠️ Error: {str(e)}"

    # -----------------------------
    # 🔹 Show bot response
    # -----------------------------
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_reply
    })

    with st.chat_message("assistant"):
        st.markdown(bot_reply)