import os

from flask import Flask
from blog import admin_bp, auth_bp, blog_bp
from configs import config

app = Flask(__name__)

config_name = os.getenv('FLASK_CONFIG', 'development')
app.config.from_object(config[config_name])

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(blog_bp)


@app.route('/')
def hello_world():
    return 'Hello World!'
