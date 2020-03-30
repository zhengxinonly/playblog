import os

import click
from flask import Flask
from configs import config
from extensions import db
from models import Admin, Post, Category, Comment

from .auth import auth_bp
from .admin import admin_bp
from .blog import blog_bp


def create_app(config_name=None):
    app = Flask(__name__)

    if not config_name:
        config_name = os.getenv('FLASK_CONFIG', 'development')
    app.config.from_object(config[config_name])

    register_blueprint(app)
    register_extensions(app)
    register_commands(app)
    register_shell_context(app)

    return app


def register_blueprint(app):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(blog_bp)


def register_extensions(app):
    db.init_app(app)


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='删除并创建数据库.')
    def initdb(drop):
        """初始化数据库."""
        if drop:
            click.confirm('这个步骤将删除数据库，是否继续?', abort=True)
            db.drop_all()
            click.echo('删除数据表')
        db.create_all()
        click.echo('初始化数据库.')

    @app.cli.command()
    @click.option('--category', default=10, help='分类的数据， 默认为 10.')
    @click.option('--post', default=50, help='文章的数量, 默认为 50.')
    @click.option('--comment', default=500, help='评论的数据, 默认为 500.')
    def forge(category, post, comment):
        """生成虚假数据."""
        from fake import fake_admin, fake_categories, fake_posts, fake_comments, fake_links

        db.drop_all()
        db.create_all()

        click.echo('生成超级管理员...')
        fake_admin()

        click.echo('正在生成 %d 分类...' % category)
        fake_categories(category)

        click.echo('正在生成 %d 文章...' % post)
        fake_posts(post)

        click.echo('正在生成 %d 评论...' % comment)
        fake_comments(comment)

        click.echo('正在生成 链接...')
        fake_links()

        click.echo('完成.')


def register_shell_context(app):
    """配置命令行上下文"""

    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, Admin=Admin, Post=Post, Category=Category, Comment=Comment)