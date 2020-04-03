from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    user = Admin.query.get(int(user_id))
    return user
