# -*- coding: utf-8 -*-

import hashlib
import random

from flask import render_template, request
from flask_classy import FlaskView

from original.gallery import Gallery, Photo


class GalleryView(FlaskView):

    def index(self):
        if request.args.get('photo'):
            index = int(request.args.get('photo'))
            gallery = Gallery(request.args['galerie'])
            current = Photo(gallery, index)
            code = str(random.randint(1000, 9999))
            code_checksum = hashlib.md5(code).hexdigest()

            context = {
                'gallery': gallery.get_info(),
                'current': current.get_info(),
                'comments': current.get_comments(),
                'antispam': {
                    'code': code,
                    'checksum': code_checksum,
                },
            }

            try:
                context['prev'] = Photo(gallery, index - 1).get_info()
            except ValueError:
                pass

            try:
                context['next'] = Photo(gallery, index + 1).get_info()
            except ValueError:
                pass

            if request.args.get('show_thumbs') == 'yes':
                context['thumbs'] = [photo.get_info()
                                     for photo in gallery.photos]

            return render_template('gallery_photo.html', **context)

        elif request.args.get('galerie'):
            gallery = Gallery(request.args['galerie'])
            context = {
                'pictures': [photo.get_info() for photo in gallery.photos],
                'gallery': gallery.get_info(),
            }
            return render_template('gallery_detail.html', **context)

        else:
            context = {
                'galleries': [gallery.get_info() for gallery in Gallery.all()],
            }
            return render_template('gallery_list.html', **context)
