#!/usr/bin/python
import mimetypes
import os
import random
import requests
import subprocess

sub_url = "http://www.reddit.com/r/EarthPorn/top.json"
headers = {'User-Agent': 'earthpornbg v0.2'}
params = {'t': 'day'}
directory = '/home/abliskovsky/Pictures/backgrounds'
extensions = ('.jpg', '.jpeg', '.png')
basename = 'earthporndesktop_bg'
mimetypes.guess_extension('image/jpeg')  # hack to make result .jpeg
mimetypes.init()


def get_urls():
    response = requests.get(sub_url, params=params, headers=headers)
    response.raise_for_status()
    listings = response.json()['data']['children']
    urls = [listing['data']['url'] for listing in listings]
    return [url for url in urls if url.endswith(extensions)]


def set_desktop(filename):
    subprocess.call(('feh', '--bg-scale', filename))


def fetch_image():
    urls = get_urls()
    random.shuffle(urls)
    for url in urls:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()
        ext = mimetypes.guess_extension(response.headers['Content-Type'])
        if ext in extensions:
            filename = os.path.join(directory, "%s%s" % (basename, ext))
            with open(filename, 'wb') as f:
                f.write(response.content)
                set_desktop(filename)
                return


if __name__ == '__main__':
    fetch_image()
