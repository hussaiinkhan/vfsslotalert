from flask import Flask
import threading
import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot
import asyncio

# === Configuration ===
VFS_URL = "https://visa.vfsglobal.com/tur/en/pol/book-an-appointment"
NO_SLOT_TEXT = "No slots available in any centers"

TELEGRAM_BOT_TOKEN = "8289492569:AAFE-ZHyBxwiuJ6FNocTycyNqLUHfrrU0LI"
TELEGRAM_USER_ID = 7697893705
CHECK_INTERVAL = 60  # seconds

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Flask App
app = Flask(__name__)

# Start the thread only once
thread_started = False

async def send_alert():
    await bot.send_message(
        chat_id=7697893705,
        text=f"🟢 Visa appointment slot may be available! Check now:\n{VFS_URL}"
    )

def check_slots():
    while True:
        try:
            print("✅ TEST ALERT — sending Telegram message")
            asyncio.run(send_alert())   # Send alert unconditionally for testing
        except Exception as e:
            print("⚠️ Error:", e)
        time.sleep(CHECK_INTERVAL)
    

@app.route('/')
def index():
    global thread_started
    if not thread_started:
        print("🔁 Starting slot checker thread...")
        thread = threading.Thread(target=check_slots)
        thread.daemon = True
        thread.start()
        thread_started = True
    return '✅ VFS Slot Checker is running!'

