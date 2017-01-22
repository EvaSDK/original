# -*- coding: utf-8 -*-

import base64
import datetime
import glob
import io
import os

try:
    from urllib import quote as urlquote
except ImportError:
    from urllib.parse import quote as urlquote

from flask import current_app as app
from flask_babel import gettext as _
from PIL import Image
from redis import Redis
from rq import Queue

from original.tasks import resize_pictures


class Gallery(object):

    def __init__(self, relative_path):
        info_txt = os.path.join(app.config['GALLERY_ROOT'], relative_path,
                                'info.txt')
        if not os.path.exists(info_txt):
            raise ValueError("'{}' is not a valid gallery"
                             .format(relative_path))

        self.relative_path = relative_path

        if not os.path.exists(
            os.path.join(app.config['GALLERY_ROOT'], relative_path, 'thumbs')
        ):
            queue = Queue(connection=Redis.from_url(app.config['REDIS_URL']))
            queue.enqueue(resize_pictures, self.full_path)

    @property
    def has_credentials(self):
        info = self.get_info()
        return 'restricted_user' in info

    def get_credentials(self, encoding):
        if not self.has_credentials:
            return None

        info = self.get_info()
        creds = u'{restricted_user}:{restricted_password}'.format(**info)
        creds = base64.encodestring(creds.encode(encoding))
        creds = b'Basic ' + creds.strip()
        return creds

    @property
    def full_path(self):
        return os.path.join(app.config['GALLERY_ROOT'], self.relative_path)

    @classmethod
    def all(cls):
        """List galleries."""
        for dirname in os.listdir(app.config['GALLERY_ROOT']):
            try:
                yield cls(os.path.join(app.config['GALLERY_ROOT'], dirname))
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
            info['folder_name'] = urlquote(info.pop('folder-name'))

        return info

    @property
    def photos(self):
        """List of photos in this gallery."""
        for photo in Photo.all(self):
            yield photo


class Photo(object):

    def __init__(self, gallery, filename):
        self.gallery = gallery
        self.filename = filename

        if not os.path.exists(self.compute_path('thumbs', True)):
            raise ValueError("Photo {} of gallery '{}' does not exist"
                             .format(self.filename,
                                     self.gallery.relative_path))

    @classmethod
    def all(cls, gallery):
        """List all photos of `gallery`."""
        for path in glob.iglob(os.path.join(gallery.full_path, 'hq', '*.jpg')):
            yield cls(gallery, os.path.basename(path))

        raise StopIteration

    def compute_path(self, size, absolute=False):
        """Compute path to image variants."""
        return os.path.join(
            self.gallery.full_path if absolute else self.gallery.relative_path,
            size,
            self.filename,
        )

    def get_info(self):
        """Information to render photo."""
        info = {
            'thumb': self.compute_path('thumbs'),
            'views': self.views,
            'filename': self.filename,
        }

        path = self.compute_path('lq', True)
        if os.path.exists(path):
            im = Image.open(path)
            info.update({
                'height': im.size[1],
                'width': im.size[0],
            })
        else:
            path = self.compute_path('hq', True)
            im = Image.open(path)
            info.update({
                'height': im.size[1],
                'width': im.size[0],
            })

        if im.size[0] > im.size[1]:
            info['orientation'] = 'landscape'
        else:
            info['orientation'] = 'portrait'

        for res in ('lq', 'mq', 'hq'):
            if os.path.exists(self.compute_path(res, True)):
                info[res] = self.compute_path(res)

        exif = im._getexif()
        if exif:
            info['exif'] = {
                'camera': (_('Camera Model'),
                           exif.get(0x110, 'Unknown Camera')),
                'lens': (_('Lens Model'), exif.get(0xa434, 'Unknown Lens')),
                'exposure_time': (_('Time of exposure'),
                                  '%d/%d second' % exif[0x829a]),
                'aperture': (_('F Stop'),
                             'f/%.1f' % (exif[0x9202][0] / exif[0x9202][1])),
                'iso': (_('Film/Chip Sensitivity'), '%d' % exif[0x8827]),
            }

        return info

    def get_comments(self):
        """Comments associated to photo."""
        comment_path = os.path.join(
            self.gallery.full_path, 'comments',
            self.filename + '.txt',
        )
        if not os.path.exists(comment_path):
            return None

        with io.open(comment_path, encoding='utf-8') as comment_file:
            return comment_file.read()

    def append_comment(self, comment):
        """Set comments associated to photo."""
        comment_path = os.path.join(
            self.gallery.full_path, 'comments',
            self.filename + '.txt',
        )

        with io.open(comment_path, 'at', encoding='utf-8') as comment_file:
            comment_file.write(comment)

    @property
    def views(self):
        """Number of time photo has been viewed."""
        view_path = os.path.join(
            self.gallery.full_path, 'comments', self.filename + '.log',
        )
        if os.path.exists(view_path):
            with io.open(view_path, encoding='utf-8') as view_file:
                views = view_file.read()
                if views:
                    return int(views)

        return 0

    @views.setter
    def views(self, value):
        """Set number of time photo has been viewed."""
        view_path = os.path.join(
            self.gallery.full_path, 'comments', self.filename + '.log',
        )
        with io.open(view_path, 'wt', encoding='utf-8') as view_file:
            view_file.write(u'{0:d}'.format(value))
