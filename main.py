from app import create_app
from flask import render_template
from flask_login import login_required

from app.db_services import get_workers

app = create_app()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/menu")
@login_required 
def main_menu():
    context = {
        "worker_info": get_workers()
            }
    return render_template('main.html', **context)
