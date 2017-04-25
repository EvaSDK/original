# -*- coding: utf-8 -*-

try:
    from tempfile import TemporaryDirectory
except ImportError:
    from backports.tempfile import TemporaryDirectory

import unittest

from original.app import create_app

from .factories import GalleryFactory


class TestViews(unittest.TestCase):

    def setUp(self):
        super(TestViews, self).setUp()
        self.gallery = TemporaryDirectory()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['GALLERY_ROOT'] = self.gallery.name
        self.client = self.app.test_client()

    def tearDown(self):
        self.gallery.cleanup()
        super(TestViews, self).tearDown()

    def test_gallery_index(self):
        with self.app.app_context():
            GalleryFactory.create_batch(2)

        res = self.client.get('/')

        self.assertEqual(res.status_code, 200)
        self.assertIn(b'<!-- listing galleries -->', res.data)
        self.assertIn(b'author', res.data)
