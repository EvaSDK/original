# -*- coding: utf-8 -*-

"""Application factory."""

from flask import Flask
from flask.ext.babel import Babel

from original.views import get_locale, send_pic
from original.views.gallery import GalleryView


def create_app():
    app = Flask(__name__.split('.')[0])

    app.add_url_rule('/galleries/<path:path>', send_pic, methods=['GET'])

    babel = Babel(app)
    babel.localeselector = get_locale

    GalleryView.register(app)
    return app


def app_factory(global_config, **local_conf):
    """PasteDeploy WSGI application factory entry-point."""
    app = create_app()
    return app
