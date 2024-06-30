import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
SHORTENER_API_KEY = os.getenv('SHORTENER_API_KEY')
BOT_TOKEN = os.getenv('7482688136:AAFAP2heGBUeLT_Ch7TCR6icFZxGMI-g5Wc')

def shorten_url(url):
    api_url = 'https://api.shorte.st/v1/data/url'
    headers = {
        'public-api-token': SHORTENER_API_KEY,
    }
    data = {'urlToShorten': url}
    response = requests.put(api_url, headers=headers, data=data)
    if response.status_code == 201:
        return response.json().get('shortenedUrl')
    else:
        logger.error(f"Error shortening URL: {response.text}")
        return url

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /search <movie name> to find movies.')

def search(update: Update, context: CallbackContext) -> None:
    query = ' '.join(context.args)
    if not query:
        update.message.reply_text('Please provide a movie name to search for.')
        return

    results = ["Movie1", "Movie2", "Movie3"]
    keyboard = [[InlineKeyboardButton(movie, callback_data=movie)] for movie in results]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Search results:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    movie_name = query.data
    download_link = f"https://example.com/download/{movie_name}"
    short_link = shorten_url(download_link)

    query.edit_message_text(text=f"Download link for {movie_name}: {short_link}")

def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main() -> None:
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable is missing")
        return
    if not SHORTENER_API_KEY:
        logger.error("SHORTENER_API_KEY environment variable is missing")
        return

    updater = Updater(BOT_TOKEN)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("search", search))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
