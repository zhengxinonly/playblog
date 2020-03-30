import random
from sqlite3 import IntegrityError

from faker import Faker

from extensions import db
from models import Admin, Category, Post, Comment, Link

# 创建中文虚假数据
fake = Faker('zh-cn')


def fake_admin():
    """创建管理员"""
    admin = Admin(
        username='admin',
        password_hash='123456',
        blog_title='PlayBlog',
        blog_sub_title="编写一个个人博客",
        name='PlayBlog',
        about='我是一个利用 flask 编写的轻量级博客网站'
    )
    db.session.add(admin)
    db.session.commit()


def fake_categories(count=10):
    """创建类别数据"""
    category = Category(name='Default')
    db.session.add(category)

    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


def fake_posts(count=50):
    """创建文章数据"""
    for i in range(count):
        post = Post(
            title=fake.sentence(),
            body=fake.text(2000),
            auth_id=Admin.query.get(1).id,
            category=Category.query.get(random.randint(1, Category.query.count())),
            timestamp=fake.date_time_this_year()
        )

        db.session.add(post)
    db.session.commit()


def fake_comments(count=500):
    """创建评论数据"""
    for i in range(count):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

    salt = int(count * 0.1)
    for i in range(salt):
        # 为审查的评论
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=False,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)

        # 管理员的评论
        comment = Comment(
            author='Mima Kirigoe',
            email='mima@example.com',
            site='example.com',
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            from_admin=True,
            reviewed=True,
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()

    # 回复
    for i in range(salt):
        comment = Comment(
            author=fake.name(),
            email=fake.email(),
            site=fake.url(),
            body=fake.sentence(),
            timestamp=fake.date_time_this_year(),
            reviewed=True,
            replied=Comment.query.get(random.randint(1, Comment.query.count())),
            post=Post.query.get(random.randint(1, Post.query.count()))
        )
        db.session.add(comment)
    db.session.commit()


def fake_links():
    github = Link(name='github', url='#')
    bilibili = Link(name='bilibili', url='#')
    weibo = Link(name='微博', url='#')
    weixin = Link(name='微信公众号', url='#')
    db.session.add_all([github, bilibili, weibo, weixin])
    db.session.commit()
