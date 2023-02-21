from app import create_app
from flask import render_template, request, jsonify, make_response
from flask_login import login_required
from werkzeug.utils import secure_filename
from os import path

from app.db_services import get_workers_resumed_data, get_single_worker_data, set_worker_data
from app.image_services import do_resize_image

app = create_app()

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
    keys = ["name", "last_name", "age", "sex", "birth_date", "curp", "elector_key", "ife", "entry_date", "position",
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
