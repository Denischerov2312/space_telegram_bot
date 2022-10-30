import os
import argparse
from random import shuffle
from time import sleep

from bot_send_image import publicate_image

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


def publicate_photos(bot, chat_id, default_hour):
    while True:
        images = os.listdir("images")
        shuffle(images)
        for image in images:
            image_path = os.path.join("images", image)
            try:
                publicate_image(bot, image_path, chat_id)
            except telegram.error.BadRequest:
                continue
            sleep(get_publications_frequency(default_hour))


def main():
    load_dotenv()
    default_hour = os.getenv("PUBLICATION_FREQUENCY")
    chat_id = os.getenv("TELEGRAMM_CHAT_ID")
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    bot = telegram.Bot(token=telegram_token)
    publicate_photos(bot, chat_id, default_hour)


if __name__ == "__main__":
    main()
