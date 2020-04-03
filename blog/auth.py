from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user

from extensions import db
from forms import LoginForm, RegisterForm
from models import Admin

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth')
def auth():
    return '登录'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember = form.remember.data
        admin = Admin.query.filter_by(username=username).first()
        if admin:
            # 验证用户名和密码
            if username == admin.username and admin.validate_password(password):
                login_user(admin, remember)  # 登入用户
                flash('欢迎回来.', 'info')
                return redirect(url_for('blog.index'))
            flash('用户名或者密码错误.', 'warning')
        else:
            flash('没有此账号', 'warning')
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('blog.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        admin = Admin.query.filter_by(username=username).first()
        if not admin:
            admin = Admin(
                username=username,
                password_hash=password,
                email=email)
            db.session.add(admin)
            db.session.commit()
            flash('注册成功，请登录', 'info')
            return redirect(url_for('auth.login'))

        else:
            flash('用户已经存在.', 'info')
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    flash('退出成功', 'info')
    return redirect(url_for('blog.index'))
