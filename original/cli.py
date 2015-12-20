# -*- coding: utf-8 -*-

import argparse
import os.path

from redis import Redis
from rq import Queue

from original.tasks import resize_pictures


def do_thumbnails():
    """Entry-point for generating thumbnails."""
    parser = argparse.ArgumentParser(description='Generates thumbnails')
    parser.add_argument('path', help='path to root of gallery to generate '
                                     'thumbnails for.')

    args = parser.parse_args()

    queue = Queue(connection=Redis())
    gallery_root = os.path.abspath(args.path)
    queue.enqueue(resize_pictures, gallery_root, 'thumbs')
    queue.enqueue(resize_pictures, gallery_root, 'lq')
