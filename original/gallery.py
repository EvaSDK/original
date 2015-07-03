# -*- coding: utf-8 -*-

import datetime
import io
import os

from PIL import Image


PHOTO_ROOT = '/mnt/data/www/galleries/'


class Gallery(object):

    def __init__(self, relative_path):
        info_txt = os.path.join(PHOTO_ROOT, relative_path, 'info.txt')
        if not os.path.exists(info_txt):
            raise ValueError("'{}' is not a valid gallery"
                             .format(relative_path))

        self.relative_path = relative_path

    @property
    def full_path(self):
        return os.path.join(PHOTO_ROOT, self.relative_path)

    @classmethod
    def all(self):
        """List galleries."""
        for dirname in os.listdir(PHOTO_ROOT):
            try:
                yield Gallery(os.path.join(PHOTO_ROOT, dirname))
            except ValueError:
                pass

        raise StopIteration

    def get_info(self):
        """Read info file."""
        with io.open(
            os.path.join(self.full_path, 'info.txt'),
            encoding='utf-8'
        ) as info_fd:
            info = dict([line.strip().split('|')
                         for line in info_fd.readlines()])
            info['date'] = datetime.datetime.strptime(info['date'].strip(),
                                                      '%Y-%m-%d').date()
            info['folder_name'] = info.pop('folder-name')

        return info

    @property
    def photos(self):
        """List of photos in this gallery."""
        for photo in Photo.all(self):
            yield photo


class Photo(object):

    def __init__(self, gallery, index):
        self.gallery = gallery
        self.index = index

        if not os.path.exists(self.compute_path('thumbs', True)):
            raise ValueError("Photo #{} of gallery '{}' does not exist"
                             .format(self.index, self.gallery.relative_path))

    @classmethod
    def all(cls, gallery):
        """ List all photos of `gallery`.

        Photos are numbered sequentially so stop iterating on first exception.
        """
        idx = 0
        while True:
            idx = idx + 1

            try:
                yield Photo(gallery, idx)
            except ValueError:
                raise StopIteration

    def compute_path(self, size, absolute=False):
        """Compute path to image variants."""
        return os.path.join(
            self.gallery.full_path if absolute else self.gallery.relative_path,
            size,
            'img-{}.jpg'.format(self.index),
        )

    def get_info(self):
        """Information to render photo."""
        im = Image.open(self.compute_path('lq', True))

        if im.size[0] > im.size[1]:
            orientation = 'landscape'
        else:
            orientation = 'portrait'

        view_path = os.path.join(
            self.gallery.full_path, 'comments', 'log_{}.txt'.format(self.index)
        )
        with io.open(view_path, encoding='utf-8') as view_file:
            views = view_file.read()

        info = {
            'lq': self.compute_path('lq'),
            'thumb': self.compute_path('thumbs'),
            'orientation': orientation,
            'height': im.size[1],
            'width': im.size[0],
            'views': int(views),
            'path': self.compute_path('thumbs'),
            'index': self.index,
        }

        if os.path.exists(self.compute_path('hq', True)):
            info['hq'] = self.compute_path('hq')

        if os.path.exists(self.compute_path('hq', True)):
            info['mq'] = self.compute_path('mq')

        return info

    def get_comments(self):
        """Comments associated to photo."""
        comment_path = os.path.join(
            self.gallery.full_path, 'comments', 'user_{}.txt'.format(self.index)
        )
        if not os.path.exists(comment_path):
             return None

        with io.open(comment_path, encoding='utf-8') as comment_file:
            return comment_file.read()
