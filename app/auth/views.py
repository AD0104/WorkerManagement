from flask import request, make_response
from flask_login import login_user
from werkzeug.security import generate_password_hash

from . import auth
from app.db_services import get_user


@auth.route("login", methods=["POST"])
def do_login():
    request_data = request.get_json()
    if(request_data["usr-name"] == "" or request_data["usr-passwrd"] == ""):
        return make_response("Existen campos vacios", 400)

    db_response = get_user(request_data["usr-name"])
    print(db_response)


    return "200"
