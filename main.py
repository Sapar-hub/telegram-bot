import os
import telebot
import json
from datetime import datetime, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Get your bot token from Railway environment variables
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
calendar_id = os.environ['CALENDAR_ID']

def get_calendar_service():
    # Build the service
    credentials_info = json.loads(os.environ['GOOGLE_CREDENTIALS'])
    token_info = json.loads(os.environ['GOOGLE_TOKEN'])
    creds = Credentials.from_authorized_user_info(token_info)
    return build('calendar', 'v3', credentials=creds)




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "👋 Привет! Я живу в Railway.")




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


        event = {
            'summary': desc,
            'start': {'dateTime': dt.isoformat(), 'timeZone': 'Asia/Almaty'},
            'end': {
                'dateTime': (dt + timedelta(hours=1)).isoformat(),  # 1-hour default
                'timeZone': 'Europe/Moscow'
            },
        }

        event = service.events().insert(calendarId=calendar_id, body=event).execute()

        bot.send_message(message.chat.id, f"📅 Мероприятие добавлена в календарь: {event.get('htmlLink')}")
    except Exception as e:
        print("Error:", e)
        bot.send_message(message.chat.id, "⚠️ Не удалось добавить событие. Проверьте формат: /addevent 25.05 15:00 Встреча")


@bot.message_handler(commands=['listevents'])
def list_event(message):
    try:
        service = get_calendar_service()
        now = datetime.utcnow().isoformat() + 'Z'

        events_result = service.events().list(
            calendarId=calendar_id, timeMin=now,
            maxResults=5, singleEvents=True,
            orderBy='startTime'
        ).execute()

        
        events = events_result.get('items', [])
       
        for e in events:
            start_time = e['start'].get('dateTime') or e['start'].get('date')
            bot.send_message(message.chat.id, f"📅 {e['summary']} в {start_time}")

    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, "❌ Ошибка парсинга.")
        import traceback
        traceback.print_exc()
        bot.send_message(message.chat.id, f"❌ :\n{str(e)}")


    
print("Бот работает...")
bot.polling()
