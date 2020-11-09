#!/usr/bin/env python3

from sqlalchemy.ext.declarative import declarative_base
from model import db, User
from main import app, DB_PATH
from lib import generate_password
from sqlalchemy.exc import IntegrityError
from os import getenv, path



with app.test_request_context():
    db.init_app(app)
    if path.exists(DB_PATH):
        print("Database has been already initialized...")
        exit(0)


    db.create_all()

    print("Init admin user")
    admin_pass = getenv("ADMIN_PASSWORD", default=generate_password(15))
    admin_email = getenv("ADMIN_EMAIL", default="admin@test.com")
    try:
        admin = User(password=admin_pass, email=admin_email, group="admins")
        db.session.add(admin)
        db.session.commit()
        print(f"""
Admin has been created:
 email:     {admin_email}
 password:  {admin_pass}
        """)
    except IntegrityError as err:
        print("ERR (Already exists): ", err)
