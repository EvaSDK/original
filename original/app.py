# -*- coding: utf-8 -*-

"""Application factory."""

import datetime
import os

from babel.dates import get_timezone
from flask import Flask
from flask_babel import Babel, format_date, format_datetime

import original
from original.views import get_locale, send_pic
from original.views.gallery import (
    GalleryDetailView,
    GalleryListView,
)


def create_app(config=None):
    app = Flask(__name__.split('.')[0])
    app_config = {  # Defaults
        'GALLERY_ROOT': os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'gallery'
        )),
        'REDIS_URL': 'redis://localhost:6379/0',
    }

    if config is not None:
        app_config.update({key.upper(): value
                           for key, value in config.items()})
        if 'DEBUG' in app_config:
            if app_config['DEBUG'] in ('0', 'n', 'no', 'False', 'false'):
                app_config.update({'DEBUG': False})
            else:
                app_config.update({'DEBUG': True})

    app.config.update(app_config)

    app.add_url_rule('/media/<path:path>', endpoint='media',
                     view_func=send_pic, methods=['GET'])

    babel = Babel(app)
    babel.localeselector(get_locale)
    app.jinja_env.filters['date'] = format_date
    app.jinja_env.filters['datetime'] = format_datetime

    app.context_processor(app_context_processor)

    GalleryListView.register(app)
    GalleryDetailView.register(app)

    return app


def app_factory(global_config, **local_conf):
    """PasteDeploy WSGI application factory entry-point."""
    app = create_app(config=local_conf)
    return app


def app_context_processor():
    """Extend context with some application data."""
    return {
        'now': datetime.datetime.now(tz=get_timezone()),
        'version': original.__version__,
    }
