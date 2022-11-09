import argparse
import datetime
import os

from fetch_images_api import download_picture, add_url_params
from fetch_images_api import determine_file_extension

import requests
from dotenv import load_dotenv


def get_image_count():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-C",
        "--count",
        help="Количество желаемых фотографий (максимум 12)",
        default=5,
        type=int,
    )
    args = parser.parse_args()
    return args.count


def get_epic_nasa_links(api_key, image_count):
    params = {"api_key": api_key}
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    response = requests.get(url, params=params)
    response.raise_for_status()
    urls = []
    images = response.json()[: image_count]
    for image in images:
        date = datetime.datetime.fromisoformat(image["date"])
        date = date.strftime("%Y/%m/%d")
        filename = image["image"]
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date}/png/{filename}.png"
        url = add_url_params(url, params)
        urls.append(url)
    return urls


def fetch_epic_nasa_images(api_key, image_count):
    for photo_number, link in enumerate(get_epic_nasa_links(api_key, image_count)):
        filepath = os.path.join('images', f'epic_nasa{photo_number}{determine_file_extension(link)}')
        download_picture(link, filepath)


def main():
    load_dotenv()
    nasa_api_key = os.environ["NASA_API_KEY"]
    image_count = get_image_count()
    fetch_epic_nasa_images(nasa_api_key, image_count)


if __name__ == "__main__":
    main()
