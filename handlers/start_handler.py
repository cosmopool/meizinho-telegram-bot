from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot

# @bot.message_handler(commands=['start'])
async def start(bot: AsyncTeleBot, message: Message):
    """Respond the /start command"""
    await bot.reply_to(message, "Olá, vamos começar?")

# from telegram import Update
# from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater
#
# def start(update: Update, context: CallbackContext):
#     """Respond the /start command"""
#     context.bot.send_message(chat_id=update.effective_chat.id, text="Olá, vamos começar? ")
