from flask import Blueprint, render_template, current_app, request

from forms import CommentForm
from models import Post, Category, Comment

blog_bp = Blueprint('blog', __name__)


@blog_bp.route('/blog')
def blog():
    return '文章内容'


@blog_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PLAYBLOG_POST_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    # posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, pagination=pagination)


@blog_bp.route('/about')
def about():
    return render_template('blog/about.html')


@blog_bp.route('/category/<int:category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PLAYBLOG_POST_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, pagination=pagination, posts=posts)


@blog_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['PLAYBLOG_COMMENT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items

    form = CommentForm()

    return render_template('blog/post.html', post=post, pagination=pagination, comments=comments, form=form)


@blog_bp.route('/reply/comment/<int:comment_id>')
def reply_comment(comment_id):
    pass
