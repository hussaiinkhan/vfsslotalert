from flask import Flask
import threading
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

app = Flask(__name__)

# === Configuration ===
VFS_URL = "https://visa.vfsglobal.com/tur/en/pol/book-an-appointment"
NO_SLOT_TEXT = "No slots available in any centers"

TELEGRAM_BOT_TOKEN = "8289492569:AAFE-ZHyBxwiuJ6FNocTycyNqLUHfrrU0LI"
TELEGRAM_USER_ID = 7697893705
CHECK_INTERVAL = 60

bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def send_alert():
    await bot.send_message(chat_id=TELEGRAM_USER_ID,
                           text=f"🟢 Visa appointment slot may be available! Check:\n{VFS_URL}")

def check_slots():
    while True:
        try:
            response = requests.get(VFS_URL, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text().lower()

            if NO_SLOT_TEXT.lower() in page_text:
                print("❌ No slots available.")
            else:
                print("✅ SLOT AVAILABLE! Sending Telegram alert.")
                asyncio.run(send_alert())
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(CHECK_INTERVAL)

@app.before_first_request
def start_checker():
    thread = threading.Thread(target=check_slots)
    thread.daemon = True
    thread.start()

@app.route('/')
def home():
    return '✅ VFS Slot Checker is running!'
