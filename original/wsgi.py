# -*- coding: utf-8 -*-

""" Help running application. """

from flask import Flask

app = Flask(__name__.split('.')[0])

from original.views.gallery import GalleryView

GalleryView.register(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
