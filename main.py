from app import create_app
from flask import render_template
from flask_login import login_required

from app.db_services import get_workers_resumed_data, get_single_worker_data

app = create_app()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/menu")
@login_required 
def main_menu():
    context = {
        "worker_info": get_workers_resumed_data()
            }
    return render_template('main.html', **context)

@app.route("/menu/employee/<int:id>")
@login_required
def single_employee_info(id):
    context = {
        "worker_info": get_single_worker_data(id)
    }
    return render_template("employee.html", **context)
    
