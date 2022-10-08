import os

import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
    bot = telegram.Bot(token=telegram_token)
    print(bot.get_me())

if __name__ == '__main__':
    main()
