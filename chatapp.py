import streamlit as st
import requests
import html  # to safely escape message content

st.set_page_config(page_title="Custom Chat App", page_icon="💬", layout="centered")

st.title("💬 Custom Chat with Local API")

# Sidebar for API config
st.sidebar.header("🔑 API Settings")
api_endpoint = st.sidebar.text_input("API Endpoint", placeholder="https://xxxx.trycloudflare.com/chat")
api_key = st.sidebar.text_input("API Key", type="password")

# Session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display
st.subheader("Chat Window")

# Display previous messages with custom bubble styling
for msg in st.session_state.messages:
    safe_content = html.escape(msg["content"])  # escape to prevent </div> etc.
    if msg["role"] == "user":
        st.markdown(
            f"""
            <div style='text-align: right; margin-bottom: 10px;'>
                <span style='background-color: #333333; color: white; padding: 10px 15px;
                             border-radius: 15px; display: inline-block; max-width: 70%; text-align: left;'>
                    {safe_content}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:  # assistant
        st.markdown(
            f"""
            <div style='text-align: left; margin-bottom: 10px;'>
                <span style='background-color: #333333; color: white; padding: 10px 15px;
                             border-radius: 15px; display: inline-block; max-width: 70%;'>
                    {safe_content}
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

# User input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    safe_prompt = html.escape(prompt)
    st.markdown(
        f"""
        <div style='text-align: right; margin-bottom: 10px;'>
            <span style='background-color: #333333; color: white; padding: 10px 15px;
                         border-radius: 15px; display: inline-block; max-width: 70%; text-align: left;'>
                {safe_prompt}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Prepare last 2-3 messages as chat_history
    chat_history = st.session_state.messages[-3:]

    payload = {
        "message": prompt,
        "chat_history": chat_history
    }

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key
    }

    try:
        response = requests.post(api_endpoint, json=payload, headers=headers, timeout=180)
        response.raise_for_status()
        reply = response.json().get("response", "⚠️ No response field in API reply")
    except Exception as e:
        reply = f"❌ Error: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply})
    safe_reply = html.escape(reply)
    st.markdown(
        f"""
        <div style='text-align: left; margin-bottom: 10px;'>
            <span style='background-color: #333333; color: white; padding: 10px 15px;
                         border-radius: 15px; display: inline-block; max-width: 70%;'>
                {safe_reply}
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
