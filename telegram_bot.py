import os
import argparse
from random import shuffle
from time import sleep
from pathlib import Path

from fetch_images_api import get_images_paths

import telegram
from dotenv import load_dotenv
load_dotenv()


def get_publications_frequency():
    parser = argparse.ArgumentParser()
    default_hour = os.getenv("PUBLICATION_FREQUENCY")
    parser.add_argument(
        "-F",
        "--hour_frequency",
        help="Частота публикаций (Одна фотография в X часов)",
        default=default_hour,
    )
    args = parser.parse_args()
    return int(args.hour_frequency) * 3600


def publicate_images(bot, image_path):
    chat_id = os.getenv('TELEGRAMM_CHAT_ID')
    bot.send_photo(chat_id=chat_id, photo=open(image_path, "rb"))


def main():
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = telegram.Bot(token=telegram_token)
    while True:
        images_paths = get_images_paths()
        shuffle(images_paths)
        for image_path in images_paths:
            try:
                publicate_images(bot, image_path)
            except telegram.error.BadRequest:
                continue
            sleep(get_publications_frequency())


if __name__ == "__main__":
    main()
