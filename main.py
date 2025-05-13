import os
import requests
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from telegram import Update

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
    "Content-Type": "application/json",
    "X-DashScope-Model": "qwen-max"
}

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    await update.message.reply_text("Погоди секунду, я думаю...")

    data = {
        "model": "qwen-max",
        "input": {
            "prompt": user_message
        }
    }

    try:
        response = requests.post(
            "https://api.dashscope.cn/api/v1/services/aigc/text-generation/generation ",
            headers=HEADERS,
            json=data
        )

        if response.status_code == 200:
            answer = response.json()['output']['text']
        else:
            answer = "Ошибка при получении ответа."
    except Exception as e:
        answer = f"Произошла ошибка: {e}"

    await update.message.reply_text(answer)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_to_user))

print("Бот запущен...")
app.run_polling()
