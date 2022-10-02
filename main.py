import os
import datetime
import urllib.parse as urlparse
from os.path import split, splitext
from urllib.parse import unquote, urlsplit, urlencode
from pathlib import Path, PurePosixPath
from pprint import pprint

import requests
from dotenv import load_dotenv


SPACEX_LAUCHES_URL = 'https://api.spacexdata.com/v3/launches'
NASA_URL = 'https://api.nasa.gov/planetary/apod'
SPACEX_FLIGHT_ID = '5a9fc479ab70786ba5a1eaaa'
NASA_API_KEY ='zKE1M2alv5BkAQwK9adbQLZ6PX2zgHTAfJJohPZE'


def download_picture(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    make_directory(filepath)
    with open(filepath, 'wb') as file:
        file.write(response.content)

def make_directory(filepath):
    path = PurePosixPath(filepath)
    directory_path = list(path.parents)[0]
    Path(directory_path).mkdir(parents=True, exist_ok=True)

def add_url_params(url, params):
    url_parts = list(urlparse.urlparse(url))
    query = dict(urlparse.parse_qsl(url_parts[4]))
    query.update(params)
    url_parts[4] = urlencode(query)
    return urlparse.urlunparse(url_parts)


def get_epic_nasa_links():
    params = {'api_key': NASA_API_KEY}
    url = 'https://api.nasa.gov/EPIC/api/natural/images'
    response = requests.get(url, params=params)
    response.raise_for_status()
    urls = []
    images = response.json()[:5]
    for image in images:
        date = datetime.datetime.fromisoformat(image['date'])
        date = date.strftime('%Y/%m/%d')
        filename = image['image']
        url = f'https://api.nasa.gov/EPIC/archive/natural/{date}/png/{filename}.png'
        url = add_url_params(url, params)
        urls.append(url)
    return urls


def get_nasa_links():
    params = {'api_key': NASA_API_KEY,
              'count': 30
             }
    response = requests.get(NASA_URL, params=params)
    response.raise_for_status()
    urls = list()
    for apod in response.json():
        urls.append(apod['url'])
    return urls

    
def get_spacex_links():
    params = {'flight_id': SPACEX_FLIGHT_ID}
    response = requests.get(SPACEX_LAUCHES_URL, params=params)
    response.raise_for_status()
    return response.json()[0]['links']['flickr_images']


def determine_file_extension(url):
    filepath = unquote(urlsplit(url).path)
    file_extension = splitext(split(filepath)[1])[1]
    return file_extension


def fetch_epic_nasa_images():
    for photo_number, link in enumerate(get_epic_nasa_links()):
        filepath = f'images/epic_nasa{photo_number}.jpg'
        download_picture(link, filepath)


def fetch_spacex_last_launch():
    for photo_number, link in enumerate(get_spacex_links()):
        filepath = f'images/spacex{photo_number}.jpg'
        download_picture(link, filepath)


def fetch_nasa_images():
    for photo_number, link in enumerate(get_nasa_links()):
        filepath = f'images/nasa{photo_number}{determine_file_extension(link)}'
        download_picture(link, filepath)

def main():
    load_dotenv()
    fetch_nasa_images()
    

if __name__ == '__main__':
    main()
    