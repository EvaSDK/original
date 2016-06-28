# -*- coding: utf-8 -*-

import os
import tempfile
import unittest

from original.app import create_app


class TestApp(unittest.TestCase):

    def setUp(self):
        super(TestApp, self).setUp()
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.gallery = tempfile.TemporaryDirectory()
        self.app.config['GALLERY_ROOT'] = self.gallery.name
        self.client = self.app.test_client()

    def tearDown(self):
        self.gallery.cleanup()
        super(TestApp, self).tearDown()

    def test_home(self):
        res = self.client.get('/')
        self.assertEqual(404, res.status_code)

    def test_gallery(self):
        res = self.client.get('/gallery/')
        self.assertEqual(200, res.status_code)
