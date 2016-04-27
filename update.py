#!/usr/bin/python
import mimetypes
import os
import random
import requests
import subprocess
from datetime import datetime

from db_ops import url_is_dupe, add_image

subreddits = ['EarthPorn', 'SpacePorn']
sub_url = "http://www.reddit.com/r/{}/top.json"
headers = {'User-Agent': 'earthpornbg v0.2'}
params = {'t': 'day'}
directory = '/home/abliskovsky/Pictures/backgrounds'
extensions = ('.jpg', '.jpeg', '.png')
basename = 'earthporndesktop_bg'
mimetypes.guess_extension('image/jpeg')  # hack to make result .jpeg
mimetypes.init()


def get_urls():
    urls = []
    for sub in subreddits:
        response = requests.get(sub_url.format(sub), params=params, headers=headers)
        response.raise_for_status()
        listings = response.json()['data']['children']
        urls.extend([listing['data']['url'] for listing in listings])

    return [url for url in urls if url.endswith(extensions)]


def fetch_image():
    urls = get_urls()
    random.shuffle(urls)
    for url in urls:
        if url_is_dupe(url):
            continue

        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        ext = mimetypes.guess_extension(response.headers['Content-Type'])
        if ext in extensions:
            timestamp = datetime.utcnow()
            file_id = add_image(timestamp, url, ext)
            filename = os.path.join(directory, "%s%s" % (file_id, ext))
            with open(filename, 'wb') as f:
                f.write(response.content)
                return


if __name__ == '__main__':
    fetch_image()
