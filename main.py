import os
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Погоди секунду, я думаю...")

    data = {
        "model": "Qwen/Qwen-3",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions ",
            headers=HEADERS,
            json=data
        )

        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
        else:
            answer = "Ошибка при получении ответа."
    except Exception as e:
        answer = f"Произошла ошибка: {e}"

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))

print("Бот запущен...")
app.run_polling()
