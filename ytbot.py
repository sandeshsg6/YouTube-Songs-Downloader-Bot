import logging
from telegram import Update, ForceReply,bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import constants
from pytube import YouTube
import validators
import time

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(constants.welcome_text)

def download_audio(update: Update, context: CallbackContext):
    if validators.url(update.message.text):
        try:
            msg1 = update.message.reply_text("🔎 Finding the Song...")
            time.sleep(0.05)
            audio_path = YouTube(update.message.text).streams.get_audio_only().download()
            song_name, extension = os.path.splitext(audio_path)
            new_audio_path = song_name + '.mp3'
            os.rename(audio_path, new_audio_path)
            msg2 = msg1.edit_text("📥 Downloading...")
            context.bot.send_audio(update.message.chat_id, audio=open(new_audio_path, 'rb'))
            msg2.delete()
            os.remove(new_audio_path)
        except Exception:
           update.message.reply_text(constants.unable_to_download) 
    else:
        update.message.reply_text(constants.reply_to_text_message)
    
def main() -> None:
    bot_token = os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True) 
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_audio))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

