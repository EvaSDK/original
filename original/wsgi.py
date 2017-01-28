# -*- coding: utf-8 -*-

"""WSGI and debug entry-points."""

from original.app import create_app

app = create_app()
application = app


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'N/A'
    app.run(debug=True)
