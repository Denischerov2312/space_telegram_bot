from cgitb import text
import os

import telegram
from dotenv import load_dotenv

CHAT_ID = '@SpacePhotos12'


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=telegram_token)
    bot.send_photo(chat_id=CHAT_ID, photo=open('images/epic_nasa0.png', 'rb'))

if __name__ == '__main__':
    main()
