import os
import argparse
import random

import telegram

from fetch_images_api import get_images_paths
from dotenv import load_dotenv


def get_image_path():
    parser = argparse.ArgumentParser()
    default_path = random.choice(get_images_paths())
    parser.add_argument(
        '-I',
        '--image',
        default=default_path,
        help='Путь до изображения'
        )
    args = parser.parse_args()
    return args.image


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAMM_CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    image = get_image_path()
    with open(image, 'rb') as image:
        bot.send_photo(chat_id=chat_id, photo=image)


if __name__ == '__main__':
    main()
