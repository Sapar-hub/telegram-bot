# 🛠️ Telegram Bot on Railway (Python)

This is a simple Telegram bot that runs on [Railway](https://railway.app), using long polling.

## 💡 Features

- `/start` – confirms the bot is online
- `/addevent 25.05 15:00 Meeting` – schedules an event (mock)

## 🚀 Deployment on Railway

1. Fork or clone this repository.
2. Go to [Railway.app](https://railway.app) → "New Project" → "Deploy from GitHub".
3. Add a **project variable**:
   - `BOT_TOKEN` → your token from @BotFather
4. Railway will auto-install requirements and run the bot.

## 🧠 Notes

- Long polling is used, so the bot runs continuously.
- Free Railway plan gives 500 hours/month (~21 days of 24/7 uptime).
