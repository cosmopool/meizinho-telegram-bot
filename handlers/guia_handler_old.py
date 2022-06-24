import datetime
import logging as log
from handlers.web_site_automation import get_webdriver, get_document
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater

def get_doc(update: Update, context: CallbackContext):
    """Get MEI document given a CNPJ"""
    cnpj = update.message.text.replace("/guia ", "")
    driver = get_webdriver()
    date = datetime.datetime.now()
    document_path = get_document(driver, cnpj, str(date.year))
    if document_path == "":
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ainda nao consigo baixar uma guia. Aguente firme ai!")
    else:
        with open(document_path, 'rb') as doc:
            # context.bot.send_message(chat_id=update.effective_chat.id, text=document_path)
            context.bot.send_document(chat_id=update.effective_chat.id, document=doc)
