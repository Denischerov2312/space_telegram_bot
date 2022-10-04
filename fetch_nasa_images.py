import argparse
import os

from fetch_images_api import download_picture, determine_file_extension

import requests
from dotenv import load_dotenv


def get_image_count():
    parser = argparse.ArgumentParser()
    parser.add_argument('-C', '--count', help='Количество желаемых фотографий', default=35)
    args = parser.parse_args()
    return args.count


def get_nasa_links(api_key):
    params = {'api_key': api_key,
              'count': get_image_count()
             }
    url = 'https://api.nasa.gov/planetary/apod'
    response = requests.get(url, params=params)
    response.raise_for_status()
    urls = list()
    for apod in response.json():
        urls.append(apod['url'])
    return urls


def fetch_nasa_images(api_key):
    for photo_number, link in enumerate(get_nasa_links(api_key)):
        file_extension = determine_file_extension(link)
        if file_extension == '':
            continue
        filepath = f'images/nasa{photo_number}{file_extension}'
        download_picture(link, filepath)


def main():
    load_dotenv()
    nasa_api_key = os.getenv('NASA_API_KEY')
    fetch_nasa_images(nasa_api_key)


if __name__ == '__main__':
    main()