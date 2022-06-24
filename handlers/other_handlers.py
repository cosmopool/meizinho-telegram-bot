from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater

def echo(update: Update, context: CallbackContext):
    """Echo all non command messages the bot receives"""
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
