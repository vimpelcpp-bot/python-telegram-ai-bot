import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Загружаем переменные из .env (если есть)
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # ключ OpenAI

# Логирование
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Инициализация OpenAI SDK (новая библиотека openai>=1.x)
client = None
if OPENAI_API_KEY:
    try:
        from openai import OpenAI  # pip install openai>=1.0.0
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        logger.error("Не удалось инициализировать OpenAI SDK: %s", e)
else:
    logger.warning("OPENAI_API_KEY не задан. Будет использоваться фолбэк-ответ.")

# ====== handlers ======

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я Telegram-бот на OpenAI. Напиши сообщение — попробую ответить 😉"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Команды: /start, /help\n"
        "Просто отправьте текстовое сообщение, я отвечу при помощи OpenAI."
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text or ""
    reply_text = None

    if client is not None:
        try:
            # Модель можно заменить при желании на gpt-4.1, gpt-4o, gpt-4o-mini и т.д.
            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.7,
                messages=[
                    {"role": "system", "content": "Ты дружелюбный, краткий и полезный ассистент."},
                    {"role": "user", "content": user_text},
                ],
            )
            reply_text = completion.choices[0].message.content.strip()
        except Exception as e:
            logger.error("Ошибка обращения к OpenAI API: %s", e)

    if not reply_text:
        # Фолбэк — если нет ключа/ошибка OpenAI:
        reply_text = (
            f"Вы написали: {user_text}\n"
            "(⚠️ OpenAI-ответ недоступен — проверьте OPENAI_API_KEY)"
        )

    await update.message.reply_text(reply_text)

def main():
    if not TELEGRAM_BOT_TOKEN:
        raise RuntimeError("Не задан TELEGRAM_BOT_TOKEN в .env или переменных окружения.")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Бот запущен (OpenAI). Нажмите Ctrl+C для остановки.")
    app.run_polling()

if __name__ == "__main__":
    main()
