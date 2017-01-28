# -*- coding: utf-8 -*-

import hashlib
import logging
import random

try:
    from urllib import unquote as urlunquote
except ImportError:
    from urllib.parse import unquote as urlunquote

from flask import render_template, request
from flask_classy import FlaskView

from original.gallery import Gallery, Photo

LOG = logging.getLogger(__name__)


class GalleryListView(FlaskView):

    route_base = '/'

    def index(self):
        return render_template('gallery_list.html', **{
            'galleries': [gallery.get_info() for gallery in Gallery.all()],
        })


class GalleryDetailView(FlaskView):

    route_base = '/gallery/<string:gallery>/'

    def _get_gallery(self, gallery):
        try:
            gallery = Gallery(urlunquote(gallery))
        except ValueError:
            return render_template('gallery_404.html'), 404

        if gallery.has_credentials:
            creds = request.headers.get('Authorization',
                                        '').encode('iso-8859-1')
            if request.user_agent.browser in ('chrome', 'opera'):
                g_creds = gallery.get_credentials('utf-8')
            else:
                g_creds = gallery.get_credentials('iso-8859-1')

            if g_creds != creds:
                return (
                    render_template('gallery_locked.html'),
                    401,
                    [('WWW-authenticate',
                      'Basic Realm="{}", encoding="ISO-8859-1"'.format(gallery)
                      )]
                )

        return gallery

    def index(self, gallery):
        gallery = self._get_gallery(gallery)
        pictures = sorted(list(gallery.photos), key=lambda pic: pic.filename)

        return render_template('gallery_detail.html', **{
            'pictures': [photo.get_info() for photo in pictures],
            'gallery': gallery.get_info(),
        })

    def get(self, gallery, photo):
        gallery = self._get_gallery(gallery)
        pictures = sorted(list(gallery.photos), key=lambda pic: pic.filename)

        current = None
        for index, pic in enumerate(pictures):
            if pic.filename == photo:
                current = pic
                break
        else:
            return render_template('picture_404.html',
                                   gallery=gallery.get_info()), 404

        # TODO: CommentForm
        code = u'{}'.format(random.randint(1000, 9999))
        code_checksum = hashlib.md5(code.encode('utf-8')).hexdigest()

        context = {
            'index': index + 1,
            'gallery': gallery.get_info(),
            'current': current.get_info(),
            'comments': current.get_comments(),
            'antispam': {
                'code': code,
                'checksum': code_checksum,
            },
        }

        if index > 1:
            context['prev'] = pictures[index - 1].get_info()

        try:
            context['next'] = pictures[index + 1].get_info()
        except IndexError:
            pass

        if request.args.get('show_thumbs') == 'yes':
            context['thumbs'] = [photo.get_info() for photo in pictures]

        current.views += 1

        return render_template('gallery_photo.html', **context)

    def post(self, gallery, photo):
        gallery = self._get_gallery(gallery)
        try:
            current = Photo(gallery, photo)
        except ValueError:
            return render_template('picture_404.html',
                                   gallery=gallery.get_info()), 404

        code = request.form['commentspamcheck'].strip()
        code_checksum = hashlib.md5(code.encode('utf-8')).hexdigest()

        if code_checksum != request.form['commentkolacek']:
            return render_template('comment_failure.html')

        current.append_comment(
            u"""<div class="commententry">
<div class="name">Comment from <em>{commentname}</em></div>
<div class="commentdata">{commentdata}</div>
</div>"""
            .format(
                commentname=request.form['commentname'],
                commentdata=request.form['commentdata']
            ))

        return self.get(gallery.relative_path, photo)
