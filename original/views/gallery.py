# -*- coding: utf-8 -*-

import logging

try:
    from urllib import unquote as urlunquote
except ImportError:
    from urllib.parse import unquote as urlunquote

from flask import render_template, request
from flask_classful import FlaskView

from original.gallery import Gallery, Photo

from ..forms import CommentForm

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

        context = {
            'index': index + 1,
            'gallery': gallery.get_info(),
            'current': current.get_info(),
            'comments': current.get_comments(),
            'form': CommentForm(),
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

        form = CommentForm()
        if not form.validate_on_submit():
            return render_template('comment_failure.html')

        current.append_comment(render_template('comment.html', form=form))

        return self.get(gallery.relative_path, photo)
