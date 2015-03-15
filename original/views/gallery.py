# -*- coding: utf-8 -*-

import datetime
import hashlib
import io
import os
import random

from flask import render_template, request
from flask_classy import FlaskView
from PIL import Image

PHOTO_ROOT = '/mnt/data/www/galleries/'


def read_info_file(path):
    """ Read gallery information file. """

    with io.open(path, encoding='utf-8') as info_fd:
        info = dict([line.strip().split('|')
                     for line in info_fd.readlines()])
        info['date'] = datetime.datetime.strptime(info['date'].strip(),
                                                  '%Y-%m-%d').date()
        info['folder_name'] = info.pop('folder-name')
   
    return info


def read_photo_info(gallery, index):
    """ Read photo information. """
    hires_path = os.path.join(
        PHOTO_ROOT, gallery, 'hq', 'img-{}.jpg'.format(index)
    )
    if not os.path.exists(hires_path):
        return None

    im = Image.open(hires_path)

    if im.size[0] > im.size[1]:
        orientation ='landscape'
    else:
        orientation = 'portrait'

    view_path = os.path.join(
        PHOTO_ROOT, gallery, 'comments', 'log_{}.txt'.format(index)
    )
    with io.open(view_path, encoding='utf-8') as view_file:
        views = view_file.read()

    return {
        'hq': os.path.join(gallery, 'hq', 'img-{}.jpg'.format(index)),
        'lq': os.path.join(gallery, 'lq', 'img-{}.jpg'.format(index)),
        'thumb': os.path.join(gallery, 'thumbs', 'img-{}.jpg'.format(index)),
        'orientation': orientation,
        'height': im.size[1],
        'width': im.size[0],
        'views': int(views),
    }


def list_thumbnails(gallery):
    """ List thumbnails for `gallery`. """
    pictures = []

    idx = 0
    while True:
        idx = idx + 1
        rel_path = os.path.join(request.args['galerie'], 'thumbs', 'img-{}.jpg'.format(idx))
        thumb = os.path.join(PHOTO_ROOT, rel_path)

        if os.path.isfile(thumb):
            info = read_photo_info(request.args['galerie'], idx)
            info.update({
                'path': rel_path,
                'index': idx,
            })
            pictures.append(info)
        else:
            break

    return pictures


class GalleryView(FlaskView):

    def index(self):
        top = PHOTO_ROOT

        if request.args.get('photo'):
            idx = int(request.args.get('photo'))
            prev = os.path.join(request.args['galerie'], 'thumbs', 'img-{}.jpg'.format(idx - 1))
            next = os.path.join(request.args['galerie'], 'thumbs', 'img-{}.jpg'.format(idx + 1))
            rel_path = os.path.join(request.args['galerie'], 'thumbs', 'img-{}.jpg'.format(idx))
            current = os.path.join(top, rel_path)

            context = {}

            info = read_photo_info(request.args['galerie'], idx - 1)
            if info:
                info.update({
                    'index': idx - 1,
                })
                context['prev'] = info

            info = read_photo_info(request.args['galerie'], idx + 1)
            if info:
                info.update({
                    'index': idx + 1,
                })
                context['next'] = info

            info = read_photo_info(request.args['galerie'], idx)
            info.update({
                'path': '',
                'index': idx,
            })
            context['current'] = info
            context['gallery'] = read_info_file(
                os.path.join(top, request.args['galerie'], 'info.txt')
            )
            #print(context)

            if request.args.get('show_thumbs') == 'yes':
                context['thumbs'] = list_thumbnails(request.args['galerie'])

            comment_path = os.path.join(
                PHOTO_ROOT, request.args['galerie'], 'comments',
                'user_{}.txt'.format(idx)
            )
            if os.path.exists(comment_path):
                with io.open(comment_path, encoding='utf-8') as comment_file:
                    context['comments'] = comment_file.read()

            code = str(random.randint(1000, 9999))
            code_checksum = hashlib.md5(code).hexdigest()
            context['antispam'] = {
                'code': code,
                'checksum': code_checksum,
            }

            return render_template('gallery_photo.html', **context)

        elif request.args.get('galerie'):

            info = read_info_file(os.path.join(top, request.args['galerie'], 'info.txt'))
            context = {
                'pictures': list_thumbnails(request.args['galerie']),
                'gallery': info,
            }

            return render_template('gallery_detail.html', **context)

        else:
            galleries = []
            for dirname in os.listdir(top):

                info_txt = os.path.join(top, dirname, 'info.txt')
                if not os.path.exists(info_txt):
                    continue

                galleries.append(read_info_file(info_txt))

            context = {'galleries': galleries}

            return render_template('gallery_list.html', **context)
