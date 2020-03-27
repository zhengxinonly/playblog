from flask import Flask
from blog import admin_bp, auth_bp, blog_bp

app = Flask(__name__)

app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(blog_bp)


@app.route('/')
def hello_world():
    return 'Hello World!'
