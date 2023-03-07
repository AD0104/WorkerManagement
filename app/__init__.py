from flask import Flask
from flask_login import LoginManager

from .config import Config
from .auth import auth
from .db_services import conn
from .models import UserModel

login_mng = LoginManager()
login_mng.login_view = 'auth.do_login' 

@login_mng.user_loader
def load_user(user_name):
    return UserModel.query(user_name)

def create_app():
    app = Flask(__name__, static_folder="./static/", template_folder="./templates/")
    app.config.from_object(Config)

    login_mng.init_app(app)

    app.register_blueprint(auth)

    return app
