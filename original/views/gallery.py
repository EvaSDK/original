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
            code = u'{}'.format(random.randint(1000, 9999))
            code_checksum = hashlib.md5(code.encode('utf-8')).hexdigest()

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

            current.views += 1

            return render_template('gallery_photo.html', **context)

        elif request.args.get('galerie'):
            gallery = Gallery(request.args['galerie'])
            creds = gallery.credentials
            if creds is not None:
                if creds != request.headers.get('Authorization', '').encode('utf-8'):
                    return (
                        render_template('gallery_locked.html'),
                        401,
                        [('WWW-authenticate',
                          'Basic Realm=' + request.args['galerie'])]
                    )

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

    def post(self):

        if request.args.get('photo'):
            index = int(request.args.get('photo'))
            gallery = Gallery(request.args['galerie'])
            current = Photo(gallery, index)
            code = request.form['commentspamcheck'].strip()
            code_checksum = hashlib.md5(code.encode('utf-8')).hexdigest()

            if code_checksum != request.form['commentkolacek']:
                return render_template('comment_failure.html')

            current.append_comment(u"""<div class="commententry">
<div class="name">Comment from<em>{commentname}</em></div>
<div class="commentdata">{commentdata}</div>
</div>""".format(
    commentname=request.form['commentname'],
    commentdata=request.form['commentdata']
))

        return self.index()
