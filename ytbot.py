import logging
from telegram import Update, ForceReply,bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import os
import constants
from pytube import YouTube
import validators

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(constants.welcome_text)

def download_videos(update: Update, context: CallbackContext):
    if validators.url(update.message.text):
        try:
            update.message.reply_text("Downloading your video!")
            video_path = YouTube(update.message.text).streams.get_highest_resolution().download()
            update.message.reply_text("video downloaded. Uploading it!") 
            print(video_path)
            context.bot.send_video(update.message.chat_id, video=open(str(video_path), 'rb'))
            os.remove(video_path)
        except:
           update.message.reply_text(constants.unable_to_download) 
    else:
        update.message.reply_text(constants.reply_to_text_message)
    
def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    bot_token = os.environ.get("BOT_TOKEN","")
    updater = Updater(bot_token, use_context=True) 

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_videos))

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()

