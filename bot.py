
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import random
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = os.getenv('BOT_TOKEN')

def start(update, context):
    keyboard = [['Получить ссылку 📎']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    update.message.reply_text("Привет! Выберите, что хотите сделать:", reply_markup=reply_markup)

def handle_message(update, context):
    correct_emoji = random.choice(["🐶", "🐱", "🐰", "🦊", "🐻", "🐸"])
    all_emojis = ["🐶", "🐱", "🐰", "🦊", "🐻", "🐸"]
    random.shuffle(all_emojis)

    buttons = [
        [InlineKeyboardButton(emoji, callback_data=('correct' if emoji == correct_emoji else 'wrong'))]
        for emoji in all_emojis
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    context.user_data['correct_emoji'] = correct_emoji
    update.message.reply_text(f"Чтобы получить ссылку, выберите смайлик как в примере: {correct_emoji}", reply_markup=reply_markup)

def handle_callback(update, context):
    query = update.callback_query
    query.answer()
    if query.data == 'correct':
        query.edit_message_text("✅ Верно! Вот ссылка на наш Telegram-канал: https://t.me/+lqMH7xMTpw00YTVi")
    else:
        query.answer("❌ Неверно, попробуйте ещё раз.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dp.add_handler(CallbackQueryHandler(handle_callback))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
