# -*- coding: utf-8 -*-

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory

import io
import os
import unittest

from original.app import create_app


class TestApp(unittest.TestCase):

    def setUp(self):
        super(TestApp, self).setUp()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.gallery = TemporaryDirectory()
        self.app.config['GALLERY_ROOT'] = self.gallery.name
        self.client = self.app.test_client()

    def tearDown(self):
        self.gallery.cleanup()
        super(TestApp, self).tearDown()

    def test_home(self):
        res = self.client.get('/')
        self.assertEqual(200, res.status_code)

    def test_media(self):
        with io.open(os.path.join(self.gallery.name, 'test.txt'), 'w') as fd:
            fd.write(u'fakecontent')

        res = self.client.get('/media/test.txt')
        self.assertEqual(200, res.status_code)
