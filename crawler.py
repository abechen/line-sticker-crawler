# encoding=utf-8
import logging
import os
import sys
import requests
from bs4 import BeautifulSoup
from PIL import Image

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)


def initlog():
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))


def main():
    req = requests.get(sys.argv[1])
    soup = BeautifulSoup(req.text, 'lxml')

    title = soup.select('h3')[0].text
    logger.info("title: %s" % title)
    if not os.path.exists('download/' + title):
        os.mkdir('download/' + title)

    info = {}
    info['path'] = 'download/' + title
    info['type'] = '.png'
    for tag in soup.select('span'):
        if 'data-sticker-id' in tag.attrs:
            style = tag['style']
            info['sid'] = tag['data-sticker-id']
            info['url'] = style[style.rfind('(') + 1:style.rfind(')')]
            download_sticker(info)


def download_sticker(info):
    r = requests.get(info['url'], stream=True)
    with open(info['path'] + '/' + info['sid'] + info['type'], 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)

    convert_format(info['path'] + '/' + info['sid'])


def convert_format(fn):
    source = Image.open(fn+'.png').convert('RGBA')
    bg = Image.new('RGBA', source.size, (255,255,255))
    result = Image.alpha_composite(bg, source)
    result.save(fn+'.jpg', 'JPEG', quality=80)


if __name__ == '__main__':
    if len(sys.argv) < 1:
        print globals()['__doc__'] % locals()
        sys.exit(1)

    reload(sys)
    sys.setdefaultencoding('utf8')

    initlog()

    if not os.path.exists('download'):
        os.mkdir('download')

    main()
