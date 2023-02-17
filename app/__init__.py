from flask import Flask

from .config import Config
from .auth import auth
from .db_services import conn

def create_app():
    app = Flask(__name__, static_folder="./static/", template_folder="./templates/")
    app.config.from_object(Config)

    conn.init_app(app)

    app.register_blueprint(auth)

    return app
