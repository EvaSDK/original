# -*- coding: utf-8 -*-

import logging
import os.path

from PIL import Image, ImageFile, ImageOps


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
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    src = Image.open(path)

    if src.size[0] > src.size[1]:
        width, height = QUALITY_SETTINGS['thumbs'][0]
    else:
        height, width = QUALITY_SETTINGS['thumbs'][0]

    orientation = src._getexif().get(0x0112, 1)
    new = src.resize((width, height),
                     QUALITY_SETTINGS['thumbs'][1])

    if orientation == 4:
        new = ImageOps.mirror(new)
    elif orientation in (2, 5, 7):
        new = ImageOps.flip(new)

    angle = {1: 0, 3: 180, 5: 90, 6: 270, 7: 270, 8: 90}.get(orientation, 1)
    new = new.rotate(angle)

    new.save(os.path.join(gallery_path, 'thumbs', os.path.basename(path)))
