import os

from flask import Flask
from configs import config

from .auth import auth_bp
from .admin import admin_bp
from .blog import blog_bp


def create_app(config_name=None):
    app = Flask(__name__)

    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app.config.from_object(config[config_name])

    register_blueprint(app)

    return app


def register_blueprint(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)
