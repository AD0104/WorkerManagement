from sys import prefix
from app import create_app
from flask import render_template, request, jsonify, make_response
from flask_login import login_required
from werkzeug.utils import secure_filename
from os import path, getenv

from app.db_services import get_workers_resumed_data, get_single_worker_data, \
    get_workers_short_data, set_worker_data, get_workers_short_data, del_worker_data
from app.image_services import do_resize_image
from app.form_services import form_fill_file, form_new_filename, form_new_file
from shutil import copy2

from dotenv import load_dotenv
load_dotenv()

app = create_app()
app.config.update(
    SECRET_KEY=getenv("SECRET_KEY"),
    SALT=getenv("SALT"),
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def make_json_response(message: str, status_code: str):
    return make_response(jsonify({
            "result_message":message,
            "status":status_code
        }))

def is_allowed_filename(filename)->bool:
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

def generate_insert_data(form_dict):
    keys = ["name", "last_name", "age", "sex", "birth_date", "curp", "elector_key", "ine", "entry_date", "position",
        "branch", "minutely_salary", "hourly_salary", "daily_salary", "biweekly_salary", "monthly_salary",
        "vacation_assigned_days"]
    data = []
    for key in keys:
        data.append(form_dict[key])
    return [form_dict[key] for key in keys] 


@app.route("/")
def index():
    return render_template('login.html')

@app.route("/menu")
@login_required 
def main_menu():
    context = {
        "worker_info": get_workers_resumed_data()
            }
    return render_template('index.html', **context)

@app.route("/menu/employee/<int:id>")
@login_required
def single_employee_info(id):
    context = {
        "worker_info": get_single_worker_data(id)
    }
    return render_template("employees/view_data.html", **context)

@app.route("/menu/employee/<int:id>/payment", methods=["GET","POST"])
@login_required
def single_employee_payment(id):
    worker_info = get_single_worker_data(id)
    if request.method == "POST":
        request_json = request.get_json() or {}
        if not request_json:
            return make_json_response("Error JSON vacio", "400")
        # for value in request_json.values():
        #     if value == "":
        #         return make_json_response("Error, existen campos vacios", "400")

        #Create file name and copy base pdf form
        filename = form_new_filename([worker_info['name'], worker_info['last_name']])
        file_path, result = form_new_file(filename) 
        if(result):
            form_fill_file({**worker_info, **request_json}, file_path)

        
        return make_json_response("Ok", "200")
    context = {
        "worker_info": worker_info 
    }
    return render_template("employees/payments.html", **context)
    
@app.route("/employees/add", methods=["GET","POST"])
@login_required
def employee_add():
    if request.method == "POST":
        #File not in received data
        if 'profile_pic' not in request.files:
            return make_json_response("Error, imagen de perfil vacía","400")

        file = request.files['profile_pic']
        #File not empty
        if file.filename == '':
            return make_json_response("Error, imagen de perfil vacía", "400")
        file_url=""
        #File not empty and file has allowed extension
        if file and is_allowed_filename(file.filename):
            filename = secure_filename(str(file.filename))
            # file_url = path.join(app.config["UPLOAD_FOLDER"], filename)
            file_url = path.join("./images/profile_pic_uploads", filename) 
            file_save_url = path.join("./app/static/images/profile_pic_uploads",filename)
            file.save(file_save_url)
            do_resize_image(file_save_url)
        else:
            return make_json_response("""Formato de imagen no valido.
                            Los formatos validos son: PNG, JPG, JPEG""","400")

        for value in request.form.values():
            if value == "":
                return make_json_response("Error, existen campos vacíos!", "400")
        data = generate_insert_data(request.form)
        data.append(file_url)
        if not set_worker_data(data):
            return make_json_response("""Error, algo salió mal al registrar. 
                                      Intentalo más tarde""","400")
        return make_json_response("Done post", "200")
    return render_template("employees/add_data.html")

@app.route("/employees/remove")
@login_required
def employee_remove():
    context = {
        "workers": get_workers_short_data()
        }
    return render_template("employees/delete_data.html", **context)

@app.route("/employees/remove/<int:id>", methods=["DELETE"])
def employees_do_remove(id):
    if del_worker_data(id):
        return make_json_response("Ok", "200")
    return make_json_response("Ocurrió un error al eliminar, intentalo de nuevo más tarde","400")
