# -*- coding: utf-8 -*-

from __future__ import print_function

import io
import os

import factory
import six
from flask import current_app as app

from ..gallery import Gallery


class GalleryFactory(factory.Factory):

    class Meta:
        model = Gallery
        inline_args = ('path',)
        exclude = ('author', 'date', 'name')

    author = factory.Faker('name')
    date = factory.Faker('date_object')
    name = factory.Faker('file_name')

    @factory.lazy_attribute
    def path(self):
        data = {
            'name': self.name,
            'author': self.author,
            'date': self.date,
            'folder_name': os.path.join(app.config['GALLERY_ROOT'],
                                        self.name),
        }

        # print('Dumping', data)
        os.mkdir(data['folder_name'])

        with io.open(os.path.join(data['folder_name'], 'info.txt'),
                     'w', encoding='utf-8') as info_txt:
            for key, value in data.items():
                line = '{}|{}\n'.format(key, value)
                info_txt.write(line if six.PY3 else line.decode('utf-8'))

        return data['folder_name']
