# -*- coding: utf-8 -*-

import logging
import os.path

from PIL import Image


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

QUALITY_SETTINGS = {
    'thumbs': ((120, 80), Image.BICUBIC),
    'lq': ((640, 480), Image.BICUBIC),
    'mq': ((1024, 768), Image.LANCZOS),
}


def generate_thumbnail(gallery_path, path):
    """Generate thumbnail for photo `path` in `gallery_path`.

    `gallery_path` must be the root of the gallery, i.e. the one containing
    info.txt.
    """
    LOG.debug('Generating thumbnail for %s', path)
    src = Image.open(path)

    if src.size[0] > src.size[1]:
        width, height = QUALITY_SETTINGS['thumbs'][0]
    else:
        height, width = QUALITY_SETTINGS['thumbs'][0]

    new = src.resize((width, height),
                     QUALITY_SETTINGS['thumbs'][1])
    new.save(os.path.join(gallery_path, 'thumbs', os.path.basename(path)))
