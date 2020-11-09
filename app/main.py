#!/usr/bin/env python3

from flask import Flask, jsonify, g, url_for, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from os import getenv
from model import db, User
from views import home, terms_of_use, privacy, about, users, user_create, login, logout, user_edit


# GLOBAL CONFIG VARIABLES
ENVIRONMENT = getenv("ENV", "devel")
DB_PATH = getenv('DB_PATH', f"db-{ENVIRONMENT}.db")
DEBUG = getenv("DEBUG", True)
PORT = getenv("PORT", 5000)
HOST = getenv("HOST", "127.0.0.1")

Base = declarative_base()
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY", "pleaseCHANGEmeBEforePRODUCTION")

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# @app.errorhandler(404)
# def not_found():
#     """Page not found."""
#     return make_response("Something is broken!!!", 404)

@app.before_request
def acl():
    pass
    


app.add_url_rule("/", view_func=home)

app.add_url_rule("/terms-of-use", view_func=terms_of_use)

app.add_url_rule("/privacy", view_func=privacy)

app.add_url_rule("/about", view_func=about)

# app.add_url_rule("/posts/", 
#    view_func=views.posts)

# app.add_url_rule("/posts/<slug>", 
#    view_func=views.posts)

app.add_url_rule("/users/login", view_func=login, methods=["GET", "POST"])
app.add_url_rule("/users/logout", view_func=logout, methods=["GET", "POST"])
app.add_url_rule("/users/<email>", view_func=user_edit, methods=["POST", "DELETE"])

app.add_url_rule("/users/", view_func=users, methods=["GET"])
app.add_url_rule("/users/", view_func=user_create, methods=["POST"])



if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=DEBUG, use_reloader=DEBUG, port=PORT, host=HOST)

