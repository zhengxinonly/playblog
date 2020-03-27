from flask import Blueprint

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/blog')
def blog():
    return '文章内容'
