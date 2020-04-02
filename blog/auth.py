from flask import Blueprint, render_template

from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth')
def auth():
    return '登录'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('auth/login.html', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@auth_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    return '退出成功'
