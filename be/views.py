from flask import Flask, jsonify, session, url_for, redirect, render_template, request, flash, make_response
from model import db, User, AuditLog
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import joinedload
from datetime import datetime
from json import loads, dumps


def menu():
    print(session.get("user"))
    default = (
        dict(title="Home", url="/"),
        dict(title="Terms of Use", url="/terms-of-use"),
        dict(title="Privacy", url="/privacy"),
        dict(title="About Us", url="/about")
    )
    cust_menu = (
        dict(title="Login", url="/users/login"),
    )
    try:
        if session["user"]["group"] == "admins":
            cust_menu = (
                dict(title="Kanban", url="/kanban/"),
                dict(title="Admin", url="/users/"),
                dict(title="Logout", url="/users/logout"),
            )
        else:
            cust_menu = (
                dict(title="Kanban", url="/kanban/"),
                dict(title="Logout", url="/users/logout"),
            )
    except KeyError:
        # keep logout in menu
        pass

    return cust_menu + default


def home():
    return render_template("home.html", 
            page_title = "Where are you!",
            main_menu = menu()
        )

def terms_of_use():
    return render_template("terms_of_use.html",
            page_title = "Terms of use",
            main_menu = menu()
            )

def privacy():
    return render_template("privacy.html",
            page_title = "Privacy",
            main_menu = menu()
            )

def about():
    return render_template("about.html",
            page_title = "About Us",
            main_menu = menu()
            )

def kanban():
    return render_template("kanban.html",
            page_title = "Personal Kanban board",
            main_menu = menu()
            )


def kanban_api():
    email = ""
    try:
        email = session["user"]["email"]
    except KeyError:
        print("User is not loged in")

    data = loads(db.session.execute(
                        f"select tasks from users where email = '{email}';"
                    ).fetchone()[0])

    if len(data) == 0:
        # initialize task data structure
        data = dict(todo=[], wip=[], check=[], done=[])

    if request.method == "POST":
        print("Add new task")
        data['todo'].append(request.get_json())
        _data = dumps(data)
        Q = f"UPDATE users SET tasks = '{_data}' WHERE email = '{email}';"
        print(Q)
        db.session.execute(Q)
        db.session.commit()


    if request.method in ["UPDATE", "PATCH"]:
        print("update data")
        _data = dumps(request.get_json())
        Q = f"UPDATE users SET tasks = '{_data}' WHERE email = '{email}';"
        print(Q)
        db.session.execute(Q)
        db.session.commit()
    

    print("Get tasks from DB")
    data = loads(db.session.execute(f"select tasks from users where email = '{email}';").fetchone()[0])
    print(data)

    r = make_response(jsonify(data), 200)
    r.headers.add("Access-Control-Allow-Origin", "*")
    r.headers.add('Access-Control-Allow-Headers', "*")
    r.headers.add('Access-Control-Allow-Methods', "*")
    r.content_type = "application/json"

    return r


def login():
    msg = "You've not been authorized yet"
    if session.get("user"):
        msg = "User %s is already loged in!" % session["user"]["email"]

    if request.method == "POST":
        try:
            usr = User.query.filter_by(
                            email=request.form["email"], 
                            password=request.form["password"]
                        ).first()

            session["user"] = dict(
                            email=usr.email, 
                            enabled=usr.enabled,
                            group=usr.group
                        )

            AuditLog.create(
                            email=usr.email,
                            status="ok", 
                            activity="login", 
                            message="Successfully loged in"
                        )
            msg = "Great, your login and password is valid!!!"
            return redirect(url_for("home"))

        except AttributeError:
            AuditLog.create(
                            email=request.form["email"],
                            status="fail", 
                            activity="login", 
                            message="Failed login with email %s" % request.form["email"]
                        )
            
            msg = "I am so sorry, there is nothing for your eyes. But you can try it again with another login and password"

    return render_template("login.html",
            page_title = "Login page",
            message = msg,
            main_menu = menu()
            )


def logout():
    if session.get("user"):
        usr = session.get("user")
        session.pop("user")

        AuditLog.create(
                    email=usr["email"],
                    status="ok", 
                    activity="logout", 
                    message="Successfully loged out"
                )
    
        flash('You were successfully logged out')
    
    return redirect(url_for("login"))



def posts(slug=None):
    print(f"Posts page {slug}")
    return render_template("blog.html", 
            page_title = "Blog posts",
            main_menu = menu(),
            data = blog_pages()
            )

def post_view(id=None):
    if id in blog_pages:
        app.logger.info("find page: ", id)
        return render_template("blog_article.html",
                page_title="Blog posts",
                main_menu = menu(),
                data=blog_pages[id]
                )

    else:
        return render_template("blog.html", 
            page_title = "Invalid blog post, please choose from posts bellow",
            main_menu = menu(),
            data = blog_pages()
            )


def user_edit(email=None):
    action = request.method
    print(f"Do {action} with {email}")

    # if not session.get("user"):
    #     flash("Login is required!!!")
    #     return redirect(url_for("login"))

    # if session["user"]["group"] != "admins":
    #     flash("You don't have required privileges, try another user!!!")
    #     return redirect(url_for("login"))

    if action == "DELETE":
        User.query.filter_by(email=email).delete()
        db.session.commit()

    return render_template("ok.html", 
            page_title = "User has been deleted",
            main_menu = menu(),
            message = "User has been deleted"
            )



def users():
    if not session.get("user"):
        flash('Login is required!!!')
        return redirect(url_for("login"))
    message = ""
    users = []

    if session["user"]["group"] == "admins":        
        #### NOT nice way

        today_logins = f"""
        select 
            count(*)
        from 
            audit_log 
        where 
            activity = 'login' and time LIKE '""" + datetime.now().strftime("%F") + """% and where email = {}' 
        group by email;
        """

        today = datetime.now().strftime("%F")
        users = []
        for usr in User.query.all():
            #_usr = dict(usr)
            new_u = usr.__dict__
            email = new_u["email"]
            new_u.pop("_sa_instance_state")
            new_u.pop("password")
            today_logins = f"""
                select 
                    count(*) as count
                from 
                    audit_log 
                where 
                    activity = 'login' and time LIKE '{today}%' and email = '{email}' 
                group by email;
                """
            all_logins = f"""
                select 
                    count(*) as count
                from 
                    audit_log 
                where 
                    activity = 'login' and email = '{email}' 
                group by email;
                """

            new_u["all_logins"] = 0
            new_u["today_logins"] = 0
            try:
                new_u["all_logins"] = db.session.execute(all_logins).fetchone()[0]
                new_u["today_logins"] = db.session.execute(today_logins).fetchone()[0]
            except TypeError:
                pass
            
            users.append(new_u)

    else:
        message = "You are not authorized to this page!"

    return render_template("users.html",
            message="",
            page_title = "User management",
            users=users,
            user=session["user"],
            main_menu=menu()
    )


def user_create():
    """
        CREATE user
    """
    msg = str()
    try:
        email = request.form.get("email") 
        password = request.form.get("password")
        group = request.form.get("group")
        print("POST: ", email, " - ", group)

        if len(email) * len(password) * len(group) == 0:
            raise IndexError("Missing one of the input arguments, please check all fields!")


        if User.create(email=email, password=password, group=group, enabled=1):
            msg = f"New user with email {email} has been added."
        
        else:
            msg = f"Error ocured during adding user with email {email}. Maybe it already exists."

    except IOError:
        msg = "No data received"

    finally:
        return render_template(
            "user_create.html",
            main_menu = menu(),
            message = msg,

        )