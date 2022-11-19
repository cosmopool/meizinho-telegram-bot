import os
import asyncio
import logging as log
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from handlers.guia_handler import get_doc
from handlers.start_handler import start

log.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=log.INFO
)

TOKEN = os.getenv("TELEGRAM_API_TOKEN")
bot = AsyncTeleBot(TOKEN)


@bot.message_handler(commands=['guia'])
async def register_guia_handler(message):
    """Register handler that respond to /guia command"""
    await get_doc(bot, message)


@bot.message_handler(commands=['start'])
async def register_start_handler(message: Message):
    """Register handler that respond to /start command"""
    await start(bot, message)


asyncio.run(bot.polling())

# import os
# import logging
# from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, Defaults
#
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)
#
# TOKEN = os.getenv('TELEGRAM_API_TOKEN')
# updater = Updater(token=TOKEN, use_context=True)
# dispatcher = updater.dispatcher
#
#
# from handlers.start_handler import start
# from handlers.mei_document_handler import get_doc
# from handlers.other_handlers import echo
#
# def set_handler_list() -> list:
#     """Set all handlers into a list to add to a dispatcher."""
#     return [
#     MessageHandler(Filters.text & (~Filters.command), echo),
#     CommandHandler('start', start),
#     CommandHandler('guia', get_doc, run_async=True),
#     ]
#
#
# def add_all_handlers(handlers: list):
#     """Add all handlers given a list of handlers"""
#     for handler in handlers:
#         dispatcher.add_handler(handler)
#
#
# # add all handlers
# add_all_handlers(set_handler_list())
#
# # start the bot
# updater.start_polling()
