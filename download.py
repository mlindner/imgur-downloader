import sys
import argparse
import requests
import urllib


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument(
        'imgur_url', action='store',
        help='URL to the album section to download')

    args = p.parse_args()

    return args


def main(argv):

    args = parse_args()

    url = args.imgur_url.replace('http://', 'https://')
    if url[:5] != 'https':
        url = 'https://' + url
    url += '/page/{}.json'

    for i in [1]:
        res = requests.get(url.format(i))
        if not res.ok:
            raise ValueError('Bad URL: ' + url.format(i))
        res_json = res.json()
        for meta in res_json['data']:
            filename = meta['hash'] + meta['ext']
            urllib.urlretrieve('https://i.imgur.com/' + filename, filename)



if __name__ == '__main__':
    main(sys.argv)
