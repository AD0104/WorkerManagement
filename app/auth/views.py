from flask import jsonify, redirect, request, make_response, current_app, url_for, session
from flask_login import login_required, login_user, logout_user
from passlib.hash import sha512_crypt as crypto

from . import auth
from app.db_services import get_user
from app.models import UserData, UserModel


@auth.route("login", methods=["GET","POST"])
def do_login():
    if request.method == "POST":
        request_data = request.get_json()

        for value in request_data.values():
            if value == "":
                return make_json_response("Existen campos vacios", "400")

        db_response = get_user(request_data["usr-name"])
        if not db_response:
            return make_json_response("No se encontró tal usuario", "400")
        if not is_same_password(request_data["usr-passwrd"],db_response["usr-passwrd"]):
            return make_json_response("La contraseña no coincide", "400")

        user_data = UserData(db_response["usr-name"], db_response["usr-passwrd"])
        user_model = UserModel(user_data)
        login_user(user_model)
        session.permanent = True

        return make_json_response(url_for('main_menu'),"200") 
    return redirect(url_for('index'))

@auth.route("logout", methods=["GET","POST"])
@login_required
def do_logout():
    logout_user()
    return redirect(url_for("index"))

def is_same_password(usr_password, db_password) -> bool:
    return crypto.verify(
            usr_password+current_app.config["SALT"],
            db_password
            )
def make_json_response(message: str, status_code: str):
    return make_response(jsonify({
            "result_message":message,
            "status":status_code
        }))
