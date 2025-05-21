import os
import telebot
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Get your bot token from Railway environment variables
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Load credentials from environment variables
credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
token_info = json.loads(os.environ['GOOGLE_TOKEN'])

# Create Credentials object
creds = Credentials.from_authorized_user_info(token_info)

# Build the service
service = build('calendar', 'v3', credentials=creds)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Hello! I'm alive on Railway.")

@bot.message_handler(commands=['addevent'])
def add_event(message):
    try:
        parts = message.text.split(' ', 3)
        date_str, time_str, desc = parts[1], parts[2], parts[3]
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m %H:%M")
        response = f"✅ Event '{desc}' scheduled for {dt.strftime('%d.%m %H:%M')}."
        bot.send_message(message.chat.id, response)
    except:
        bot.send_message(message.chat.id, "⚠️ Usage: /addevent 25.05 15:00 Meeting")

print("Bot is running...")
bot.polling()
