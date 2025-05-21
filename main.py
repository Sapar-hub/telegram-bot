import os
import telebot
from datetime import datetime

# Get your bot token from Railway environment variables
TOKEN = os.getenv("7365413378:AAHCuNJ4JcHYoXrwRGYte6qowI6zlumryR4")
bot = telebot.TeleBot(TOKEN)

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
