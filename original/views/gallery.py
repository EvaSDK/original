# -*- coding: utf-8 -*-

import datetime
import io
import os

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


def read_photo_info(gallery, photo_path):
    """ Read photo information. """
    hires_path = os.path.join(PHOTO_ROOT, gallery, 'hq', photo_path)
    if not os.path.exists(hires_path):
        return None

    im = Image.open(hires_path)

    if im.size[0] > im.size[1]:
        orientation ='landscape'
    else:
        orientation = 'portrait'

    return {
        'hq': os.path.join(gallery, 'hq', photo_path),
        'lq': os.path.join(gallery, 'lq', photo_path),
        'thumb': os.path.join(gallery, 'thumbs', photo_path),
        'orientation': orientation,
        'height': im.size[1],
        'width': im.size[0],
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
            info = read_photo_info(request.args['galerie'], 'img-{}.jpg'.format(idx))
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

            info = read_photo_info(request.args['galerie'], 'img-{}.jpg'.format(idx - 1))
            if info:
                info.update({
                    'index': idx - 1,
                })
                context['prev'] = info

            info = read_photo_info(request.args['galerie'], 'img-{}.jpg'.format(idx + 1))
            if info:
                info.update({
                    'index': idx + 1,
                })
                context['next'] = info

            info = read_photo_info(request.args['galerie'], 'img-{}.jpg'.format(idx))
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
