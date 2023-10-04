from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from .models import db, User
db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

from flask_login import LoginManager
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

login_manager.login_view = 'login_page'

from . import routes