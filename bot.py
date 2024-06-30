import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define your bot token and API keys
BOT_TOKEN = '7482688136:AAFAP2heGBUeLT_Ch7TCR6icFZxGMI-g5Wc'
MOVIE_API_KEY = '19311ff7'
LINK_SHORTENER_API_KEY = 'YOUR_LINK_SHORTENER_API_KEY'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /download <movie_name> to download a movie.')

def download_movie(update: Update, context: CallbackContext) -> None:
    movie_name = ' '.join(context.args)
    if not movie_name:
        update.message.reply_text('Please provide a movie name.')
        return

    # Fetch movie details from a movie database API
    movie_api_url = f'http://www.omdbapi.com/?t={movie_name}&apikey={19311ff7}'
    response = requests.get(movie_api_url)
    data = response.json()

    if data['Response'] == 'False':
        update.message.reply_text('Movie not found!')
        return

    # Generate download link (dummy example)
    download_link = f'http://example.com/download/{movie_name}'

    # Shorten the download link using a link shortener API
    shortener_api_url = f'https://api.yourshortener.com/shorten?url={download_link}&apikey={LINK_SHORTENER_API_KEY}'
    short_response = requests.get(shortener_api_url)
    short_data = short_response.json()
    short_link = short_data['shortenedUrl']

    update.message.reply_text(f'Download link for {movie_name}: {short_link}')

def main() -> None:
    updater = Updater(BOT_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("download", download_movie))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
