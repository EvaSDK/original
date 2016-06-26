# -*- coding: utf-8 -*-

"""WSGI and debug entry-points."""

from original.app import create_app

app = create_app()
application = app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)
