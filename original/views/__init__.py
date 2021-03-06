# -*- coding: utf-8 -*-

from flask import current_app as app, request, send_from_directory


def get_locale():
    return request.accept_languages.best_match(['en', 'fr'])


def send_pic(path):
    """Send pictures from picture folder."""
    return send_from_directory(app.config['GALLERY_ROOT'], path)
