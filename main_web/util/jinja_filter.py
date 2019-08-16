import os
from flask import session, request


def register_jinja_filters(app):
    @app.template_filter()
    def getenv(text):
        return os.getenv(text)
