import os

import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram(text):
    """Send a message to Telegram. Never crashes the worker if it fails."""
    if not TOKEN or not CHAT_ID:
        print("(alerts disabled: set TELEGRAM_TOKEN and TELEGRAM_CHAT_ID in .env)")
        return False
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": text},
            timeout=10,
        )
        return resp.ok
    except requests.RequestException as e:
        print(f"(alert failed: {e})")
        return False


if __name__ == "__main__":
    print("sent:", send_telegram("Test alert from the anomaly pipeline"))