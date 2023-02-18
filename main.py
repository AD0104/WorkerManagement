from app import create_app
from flask import render_template
from flask_login import login_required

app = create_app()

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/menu")
@login_required 
def main_menu():
    return render_template('main.html')
