# filename:configs.py
import os
import sys

basedir = os.path.abspath(os.path.dirname(__name__))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqllite:///'
else:
    prefix = 'sqllite:////'


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLAYBLOG_COMMENT_PER_PAGE = 10
    PLAYBLOG_POST_PER_PAGE = 10
    PLAYBLOG_MANAGE_POST_PER_PAGE = 10


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


class TestingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 内存数据库


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
