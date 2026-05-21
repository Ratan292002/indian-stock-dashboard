import requests

BOT_TOKEN = "8791019465:AAET0VzLU_hf4uTFd-owa-Stcb7HF_5eqpE"

CHAT_ID = "1680644187"

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
