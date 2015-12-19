# -*- coding: utf-8 -*-

import glob
import logging
import os
import os.path

from PIL import Image, ImageFile, ImageOps
from redis import Redis
from rq import Queue


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

QUALITY_SETTINGS = {
    'thumbs': ((120, 80), Image.BICUBIC),
    'lq': ((640, 480), Image.BICUBIC),
    'mq': ((1024, 768), Image.LANCZOS),
}


def resize_picture(gallery_path, path, quality):
    """Generate thumbnail for photo `path` in `gallery_path`.

    `gallery_path` must be the root of the gallery, i.e. the one containing
    info.txt.
    """
    if quality not in QUALITY_SETTINGS:
        raise ValueError('Quality %s is not a valid setting' % quality)

    LOG.debug('Generating %s quality picture for %s', quality, path)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    src = Image.open(path)

    if src.size[0] > src.size[1]:
        width, height = QUALITY_SETTINGS[quality][0]
    else:
        height, width = QUALITY_SETTINGS[quality][0]

    orientation = src._getexif().get(0x0112, 1)
    new = src.resize((width, height),
                     QUALITY_SETTINGS[quality][1])

    if orientation == 4:
        new = ImageOps.mirror(new)
    elif orientation in (2, 5, 7):
        new = ImageOps.flip(new)

    angle = {1: 0, 3: 180, 5: 90, 6: 270, 7: 270, 8: 90}.get(orientation, 1)
    new = new.rotate(angle)

    new.save(os.path.join(gallery_path, quality, os.path.basename(path)))


def resize_pictures(gallery_path, quality):
    """Generate thumbnails for `gallery_path`."""
    if quality not in QUALITY_SETTINGS:
        raise ValueError('Quality %s is not a valid setting' % quality)

    os.makedirs(os.path.join(gallery_path, quality))

    queue = Queue(connection=Redis())
    for photo_path in glob.glob(os.path.join(gallery_path, 'hq', '*.jpg')):
        queue.enqueue(resize_picture, gallery_path, photo_path, quality)
