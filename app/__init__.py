import os
import logging

from .helpers import ocr
from telegram import Update
from telegram.bot import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def send_photo(update: Update, _: CallbackContext):
    bot = Bot(token=os.environ['TELEGRAM_TOKEN'])
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    
    filename = 'tmp/{}.jpg'.format(file_id[0:8])
    newFile.download(filename)

    try:
        ocr_text, ocr_list = ocr.detect_text(filename)    
        update.message.reply_text(str(ocr_text))
    except:
        update.message.reply_text('Desculpe! Eu não consigo converter essa imagem em texto')

def main() -> None:
    updater = Updater(os.environ['TELEGRAM_TOKEN'])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(MessageHandler(Filters.photo, send_photo))

    updater.start_polling()

    updater.idle()
