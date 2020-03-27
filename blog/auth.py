from flask import Blueprint

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth')
def auth():
    return '登录'
