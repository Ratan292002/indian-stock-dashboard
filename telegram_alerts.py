import streamlit as st
import requests

BOT_TOKEN = st.secrets["BOT_TOKEN"]
CHAT_ID = st.secrets["CHAT_ID"]

# ---------------------------------------
# TELEGRAM ALERT FUNCTION
# ---------------------------------------

def send_telegram_alert(message):

    url = (
        f"https://api.telegram.org/bot"
        f"{BOT_TOKEN}/sendMessage"
    )

    payload = {

        "chat_id": CHAT_ID,

        "text": message
    }

    try:

        requests.post(
            url,
            data=payload
        )

        return True

    except:

        return False
