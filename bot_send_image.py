import os
import argparse
import random
from pathlib import Path

import telegram
from dotenv import load_dotenv


def get_images_paths():
    images_paths = list(Path("images/").rglob("*.[jJpPGg][pPnNiI][gGgGfF]"))
    return images_paths


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


def publicate_image(bot, image_path, chat_id):
    with open(image_path, 'rb') as image:
        bot.send_photo(chat_id=chat_id, photo=image)


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAMM_CHAT_ID")
    bot = telegram.Bot(token=telegram_token)
    image = get_image_path()
    publicate_image(bot, image, chat_id) 


if __name__ == '__main__':
    main()
