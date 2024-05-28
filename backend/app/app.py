import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://administrador:NCPgatauFcE4HfYylftN8tX7YAyfNbSv@dpg-cp74hngl6cac7386tmmg-a.oregon-postgres.render.com/ferremas_6a85'
db = SQLAlchemy(app)



@app.route("/flask", methods=['GET'])
def index():
    return "Flask server"

if __name__ == "__main__":
    app.run(port=500, debug=True)