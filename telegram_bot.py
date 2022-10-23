import os
import argparse
from random import shuffle
from time import sleep

from fetch_images_api import get_images_paths

import telegram
from dotenv import load_dotenv


def get_publications_frequency(default_hour):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-F",
        "--hour_frequency",
        help="Частота публикаций (Одна фотография в X часов)",
        default=default_hour,
    )
    args = parser.parse_args()
    return int(args.hour_frequency) * 3600


def publicate_images(bot, image_path, chat_id):
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=chat_id, photo=image)


def main():
    load_dotenv()
    default_hour = os.getenv("PUBLICATION_FREQUENCY")
    chat_id = os.getenv('TELEGRAMM_CHAT_ID')
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = telegram.Bot(token=telegram_token)
    while True:
        images_paths = get_images_paths()
        shuffle(images_paths)
        for image_path in images_paths:
            try:
                publicate_images(bot, image_path, chat_id)
            except telegram.error.BadRequest:
                continue
            sleep(get_publications_frequency(default_hour))


if __name__ == "__main__":
    main()
