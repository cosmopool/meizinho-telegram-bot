import datetime
from telebot.types import Message
from telebot.async_telebot import AsyncTeleBot
from handlers.web_site_automation_async import get_webdriver, get_document
import logging as log

USER = os.getenv("USER")


async def get_doc(bot: AsyncTeleBot, message):
    """Get MEI document given a CNPJ"""
    with open(f"/home/${USER}/tmp/test", "rb") as doc:
        # async with open("/home/arrow/tmp/DAS-PGMEI-39518994000178-AC2022.pdf", 'rb') as doc:
        await bot.send_document(message.chat, doc)
    # await bot.send_document(message, "/home/arrow/tmp/DAS-PGMEI-39518994000178-AC2022.pdf")
    # date = datetime.datetime.now()
    # cnpj = message.text.replace("/guia ", "")
    # await bot.reply_to(message, f"Vou pegar a guia do mês {date.month}, do CNPJ: {cnpj}")
    # driver = get_webdriver()
    # document_path = await get_document(driver, cnpj, str(date.year))
    #
    # if document_path == "":
    #     await bot.send_message(message, "Infelizmente não consegui baixar sua guia!")
    # else:
    # await bot.send_document(message.chat, document_path)
    # await bot.send_document(message, open(document_path, "rb"))
    # with open(document_path, 'rb') as doc:
    #     await bot.send_document(message, doc)


# import datetime
# import logging as log
# from handlers.web_site_automation import get_webdriver, get_document
# from telegram import Update
# from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters, Updater
#
# def get_doc(update: Update, context: CallbackContext):
#     """Get MEI document given a CNPJ"""
#     cnpj = update.message.text.replace("/guia ", "")
#     driver = get_webdriver()
#     date = datetime.datetime.now()
#     document_path = get_document(driver, cnpj, str(date.year))
#     if document_path == "":
#         context.bot.send_message(chat_id=update.effective_chat.id, text="Ainda nao consigo baixar uma guia. Aguente firme ai!")
#     else:
#         # context.bot.send_message(chat_id=update.effective_chat.id, text=document_path)
#         context.bot.send_document(chat_id=update.effective_chat.id, document=open(document_path, "rb"))
