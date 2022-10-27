import argparse

from fetch_images_api import download_picture

import requests


def get_flight_id():
    parser = argparse.ArgumentParser()
    parser.add_argument('--flight_id',
                        help='ID запуска SpaceX',
                        default='latest'
                        )
    args = parser.parse_args()
    return args.flight_id


def get_spacex_links():
    url = f'https://api.spacexdata.com/v5/launches/{get_flight_id()}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()['links']['flickr']['original']


def fetch_spacex_last_launch():
    for photo_number, link in enumerate(get_spacex_links()):
        filepath = f'images/spacex{photo_number}.jpg'
        download_picture(link, filepath)


def main():
    fetch_spacex_last_launch()


if __name__ == '__main__':
    main()
