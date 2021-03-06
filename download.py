import sys
import argparse
import requests
import urllib
import os.path
import os
import json
import io


def parse_args():
    p = argparse.ArgumentParser()

    p.add_argument(
        'imgur_url', help='URL to the album section to download')
    p.add_argument(
        '-o', '--output', help='Destination directory to store the files')
    p.add_argument(
        '-c', '--continue', action="store_true",
        help='Destination directory to store the files',
        dest='_continue')

    args = p.parse_args()

    return args


def main(argv):

    args = parse_args()

    output = ""
    if args.output:
        output = args.output

    url = args.imgur_url.replace('http://', 'https://')
    if url[:5] != 'https':
        url = 'https://' + url
    print "Downloading from {}".format(url)
    url += '/page/{}.json'

    page = 0
    while True:
        res = requests.get(url.format(page))
        if not res.ok:
            raise ValueError('Bad URL: ' + url.format(page))
        res_json = res.json()

        data = res_json['data']
        if not data:
            break
        print "Downloading page {}".format(page)

        for meta in data:
            filename = meta['hash'] + meta['ext']
            json_file = os.path.join(output, meta['hash'] + '.json')
            out_file = os.path.join(output, filename)

            if args._continue and os.path.exists(out_file):
                print "Found {}, skipping".format(out_file)
                continue
            fetch_url = 'https://i.imgur.com/' + filename

            print "Writing {} to {}".format(fetch_url, out_file)
            try:
                urllib.urlretrieve(fetch_url, out_file)
            except:
                if os.path.exists(out_file):
                    print "Deleted partially written file"
                    os.remove(out_file)
                raise

            with io.open(json_file, 'w', encoding='utf8') as json_out_file:
                data = json.dumps(meta, sort_keys=True, ensure_ascii=False, indent=2)
                json_out_file.write(unicode(data))

        page += 1

    print "Completed downloading"


if __name__ == '__main__':
    main(sys.argv)
