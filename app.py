from flask import Flask
import threading
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

app = Flask(__name__)

# ==== VFS Checker Config ====
VFS_URL = "https://visa.vfsglobal.com/tur/en/pol/book-an-appointment"
NO_SLOT_TEXT = "No slots available in any centers"

TELEGRAM_BOT_TOKEN = "8289492569:AAFE-ZHyBxwiuJ6FNocTycyNqLUHfrrU0LI"
TELEGRAM_USER_ID = 7697893705
CHECK_INTERVAL = 60  # In seconds

bot = Bot(token=TELEGRAM_BOT_TOKEN)

def check_slots():
    while True:
        try:
            response = requests.get(VFS_URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()

            if NO_SLOT_TEXT.lower() in page_text:
                print("❌ No slots available. Checked.")
            else:
                print("✅ SLOT AVAILABLE! Sending Telegram alert.")
                bot.send_message(
                    chat_id=TELEGRAM_USER_ID,
                    text="🟢 Visa appointment slot may be available! Visit:\n" + VFS_URL
                )
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(CHECK_INTERVAL)

# Start the background thread on app startup
@app.before_first_request
def activate_job():
    thread = threading.Thread(target=check_slots)
    thread.daemon = True
    thread.start()

@app.route('/')
def home():
    return '✅ VFS Slot Checker is Running!'

