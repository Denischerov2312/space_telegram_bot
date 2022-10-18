import os
import argparse
from random import shuffle
from time import sleep
from pathlib import Path

import telegram
from dotenv import load_dotenv


CHAT_ID = "@SpacePhotos12"


def get_images_paths():
    images_paths = list(Path("images/").rglob("*.[jJpP][pPnN][gGgG]"))
    return images_paths


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
    return int(args.hour_frequency * 3600)


def publicate_images(bot, image_path):
    bot.send_photo(chat_id=CHAT_ID, photo=open(image_path, "rb"))


def main():
    load_dotenv()
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
