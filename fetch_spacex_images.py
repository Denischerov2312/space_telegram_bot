import argparse
import os

from fetch_images_api import download_picture

import requests


def get_flight_id():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-F',
        "--flight_id",
        help="ID запуска SpaceX",
        default="latest",
    )
    args = parser.parse_args()
    return args.flight_id


def get_spacex_links(flight_id):
    url = f"https://api.spacexdata.com/v5/launches/{flight_id}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["links"]["flickr"]["original"]


def fetch_spacex_last_launch(flight_id):
    for photo_number, link in enumerate(get_spacex_links(flight_id)):
        filepath = os.path.join('images', f'spacex{photo_number}.jpg')
        download_picture(link, filepath)


def main():
    flight_id = get_flight_id()
    fetch_spacex_last_launch(flight_id)


if __name__ == "__main__":
    main()
