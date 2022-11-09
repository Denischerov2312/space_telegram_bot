import os
import argparse
from random import shuffle
from time import sleep

from bot_send_image import publicate_image

import telegram
from dotenv import load_dotenv


def get_delay(default_hour):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-F",
        "--hour_frequency",
        help="Частота публикаций (Одна фотография в X часов)",
        default=default_hour,
        type=int,
    )
    args = parser.parse_args()
    return args.hour_frequency * 3600


def publicate_photos(bot, chat_id, delay):
    while True:
        images = os.listdir("images")
        shuffle(images)
        for image in images:
            image_path = os.path.join("images", image)
            try:
                publicate_image(bot, image_path, chat_id)
            except telegram.error.BadRequest: # Пропускает изображение, если его размер слишком большой
                continue
            except telegram.error.NetworkError:
                print('Проблемы с подключением, следующая попытка через 10 сек.')
                sleep(10)
                continue
            sleep(delay)


def main():
    load_dotenv()
    default_hour = os.getenv("PUBLICATION_FREQUENCY", default=4)
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    telegram_token = os.environ["TELEGRAM_BOT_TOKEN"]
    bot = telegram.Bot(token=telegram_token)
    delay = get_delay(default_hour)
    publicate_photos(bot, chat_id, delay)


if __name__ == "__main__":
    main()
