import urllib.parse as urlparse
from os.path import split, splitext
from urllib.parse import unquote, urlsplit, urlencode
from pathlib import Path, PurePosixPath

import requests


def determine_file_extension(url):
    filepath = unquote(urlsplit(url).path)
    file_extension = splitext(split(filepath)[1])[1]
    return file_extension


def download_picture(url, filepath):
    response = requests.get(url)
    response.raise_for_status()
    make_directory(filepath)
    with open(filepath, "wb") as file:
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
