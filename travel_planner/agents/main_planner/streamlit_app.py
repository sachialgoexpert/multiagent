import streamlit as st
import requests
import uuid
import json

MAIN_PLANNER_URL = "http://localhost:8000/chat"

st.set_page_config(page_title="AI Travel Planner", layout="wide")

st.title("🧭 Multi-Agent Travel Planner")
st.caption("Powered by Agent-to-Agent (A2A) orchestration")

# -------------------------------
# Session state
# -------------------------------
if "context_id" not in st.session_state:
    st.session_state.context_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Planner call
# -------------------------------
def send_to_planner(message: str):
    payload = {
        "context_id": st.session_state.context_id,
        "message": message,
    }
    resp = requests.post(MAIN_PLANNER_URL, json=payload, timeout=90)
    resp.raise_for_status()
    return resp.json()

# -------------------------------
# Render chat history
# -------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------------
# Chat input
# -------------------------------
user_input = st.chat_input("Plan a trip…")

if user_input:
    # ---------------------------
    # User message
    # ---------------------------
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # ---------------------------
    # Planner call
    # ---------------------------
    with st.spinner("Planning…"):
        response = send_to_planner(user_input)

    # ---------------------------
    # Assistant response
    # ---------------------------
    with st.chat_message("assistant"):

        if response["type"] == "question":
            assistant_text = f"❓ **{response['message']}**"
            st.markdown(assistant_text)

            # UX hint (very important)
            st.caption("🧩 Collecting required details to plan your trip")

        elif response["type"] == "plan_options":
            st.markdown("## ✨ Your Travel Plan")
            st.markdown(response["summary"])

            # Optional debug / advanced view
            with st.expander("🔍 View detailed agent outputs (advanced)"):
                st.json(response.get("results", {}))

            assistant_text = response["summary"]

            st.info(
                "You can say:\n"
                "- *Find cheaper options*\n"
                "- *Change hotel area*\n"
                "- *Add local transport*\n"
                "- *Show restaurants*\n"
                "- *Finalize plan*"
            )

        else:
            assistant_text = "⚠ Unexpected response from planner"
            st.warning(assistant_text)

    # ---------------------------
    # Save assistant message
    # (prevent duplicates)
    # ---------------------------
    if (
        not st.session_state.messages
        or st.session_state.messages[-1]["content"] != assistant_text
    ):
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_text}
        )
