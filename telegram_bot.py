from cgitb import text
import os

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=telegram_token)
    bot.send_message(chat_id='@SpacePhotos12', text='Hello, world!')

if __name__ == '__main__':
    main()
