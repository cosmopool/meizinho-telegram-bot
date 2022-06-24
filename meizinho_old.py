import os
import logging
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater, Defaults

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

TOKEN = os.getenv('TELEGRAM_API_TOKEN')
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


from handlers.start_handler import start
# from handlers.mei_document_handler import get_doc
from handlers.guia_handler_old import get_doc
from handlers.other_handlers import echo

def set_handler_list() -> list:
    """Set all handlers into a list to add to a dispatcher."""
    return [
    MessageHandler(Filters.text & (~Filters.command), echo),
    CommandHandler('start', start),
    CommandHandler('guia', get_doc, run_async=True),
    ]


def add_all_handlers(handlers: list):
    """Add all handlers given a list of handlers"""
    for handler in handlers:
        dispatcher.add_handler(handler)


# add all handlers
add_all_handlers(set_handler_list())

# start the bot
updater.start_polling()
