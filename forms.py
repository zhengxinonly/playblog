from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, SelectField, TextAreaField, ValidationError,
                     BooleanField, PasswordField)
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from models import Category


class LoginForm(FlaskForm):
    """登录表单"""
    username = StringField('用户名：', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码：', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('记住我')
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    """注册表单"""
    username = StringField('用户名：', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('密码：', validators=[DataRequired(), Length(1, 128)])
    email = StringField('邮箱', validators=[DataRequired(), Email(), Length(1, 254)])
    submit = SubmitField('注册')


class PostForm(FlaskForm):
    """文章表单"""
    title = StringField('标题', [DataRequired(), Length(max=255)])
    body = TextAreaField('内容')
    categories = SelectField('文章种类', choices=[], coerce=int)
    submit = SubmitField("提交")

    # 保证数据与数据库同步
    def __init__(self):
        super(PostForm, self).__init__()
        self.categories.choices = [(c.id, c.name) for c in Category.query.order_by('id')]


class CategoryForm(FlaskForm):
    """分类表单"""
    name = StringField('类别名', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField('确认')

    @staticmethod
    def validate_name(field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('此分类早就存在')


class CommentForm(FlaskForm):
    """评论表单"""
    body = TextAreaField('给作者留言', validators=[DataRequired()])
    submit = SubmitField("提交")
