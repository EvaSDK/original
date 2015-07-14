# -*- coding: utf-8 -*-

import argparse
import os.path
import glob

from redis import Redis
from rq import Queue

from original.tasks import generate_thumbnail


def do_thumbnails():
    """Entry-point for generating thumbnails."""
    parser = argparse.ArgumentParser(description='Generates thumbnails')
    parser.add_argument('path', help='path to root of gallery to generate '
                                     'thumbnails for.')

    args = parser.parse_args()

    queue = Queue(connection=Redis())
    gallery_root = os.path.abspath(args.path)
    for photo_path in glob.glob(os.path.join(gallery_root, 'hq', '*.jpg')):
        queue.enqueue(generate_thumbnail, gallery_root, photo_path)
