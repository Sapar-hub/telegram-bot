import os
import telebot
import json
from datetime import datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Get your bot token from Railway environment variables
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


def get_calendar_service():
    # Build the service
    credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    token_info = json.loads(os.environ['GOOGLE_TOKEN'])
    creds = Credentials.from_authorized_user_info(token_info)
    return build('calendar', 'v3', credentials=creds)




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Hello! I'm alive on Railway.")




@bot.message_handler(commands=['addevent'])
def add_event(message):
    try:
        parts = message.text.split(' ', 3)
        date_str, time_str, desc = parts[1], parts[2], parts[3]
        dt = datetime.strptime(f"{date_str} {time_str}", "%d.%m %H:%M")

        # Build service
        credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
        token_info = json.loads(os.environ['GOOGLE_TOKEN'])
        creds = Credentials.from_authorized_user_info(token_info)
        service = build('calendar', 'v3', credentials=creds)

        calendar_id = os.environ['CALENDAR_ID']

        event = {
            'summary': desc,
            'start': {'dateTime': dt.isoformat(), 'timeZone': 'Asia/Almaty'},
            'end': {
                'dateTime': (dt + datetime.timedelta(hours=1)).isoformat(),  # 1-hour default
                'timeZone': 'Asia/Almaty'
            },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()

        bot.send_message(message.chat.id, f"📅 Event created: {event.get('htmlLink')}")
    except Exception as e:
        print("Error:", e)
        bot.send_message(message.chat.id, "⚠️ Could not create event. Check format: /addevent 25.05 15:00 Meeting")


@bot.message_handler(commands=['listevent'])
def list_event(message):
    try:
        service = get_calendar_service()
        now = datetime.datetime.utcnow().isoformat() + 'Z'

        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=5, singleEvents=True,
            orderBy='startTime'
        ).execute()

        
        events = events_result.get('items', [])
        bot.send_message(message.chat.id,"✅ Google Calendar connected.")
        for e in events:
            bot.send_message(message.chat.id,e['summary'], e['start'])
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "❌ Failed to list event.")



    
print("Bot is running...")
bot.polling()
