from telegram import ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

import os
import asyncio

BOT_TOKEN = os.environ.get("BOT_TOKEN")  # Токен из переменной окружения

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("Отправить номер", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("Привет! Отправь мне свой номер, пожалуйста.", reply_markup=reply_markup)

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact.phone_number
    await update.message.reply_text(f"Спасибо! Ты отправил номер: {contact}")
    # Здесь в будущем можно будет добавить отправку в amoCRM

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    await app.bot.delete_webhook(drop_pending_updates=True)  # Удалил  webhook перед polling

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.CONTACT, handle_contact))

    print("Бот запущен...")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
