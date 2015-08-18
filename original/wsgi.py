# -*- coding: utf-8 -*-

""" Help running application. """

from flask import Flask, request, send_from_directory
from flask.ext.babel import Babel

app = Flask(__name__.split('.')[0])
babel = Babel(app)

from original import gallery
from original.views.gallery import GalleryView

GalleryView.register(app)


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(['en', 'fr'])


@app.route('/galleries/<path:path>')
def send_pic(path):
    """Send pictures from picture folder."""
    return send_from_directory(gallery.PHOTO_ROOT, path)


def app_factory(global_config, **local_conf):
    """PasteDeploy WSGI application factory entry-point."""
    return app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
