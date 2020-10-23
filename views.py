from flask import Flask, jsonify, session, url_for, redirect, render_template, request, flash
from model import db, User


def main_menu():
    return (
        dict(title="Home", url="/"),
        dict(title="Terms of Use", url="/terms-of-use"),
        dict(title="Privacy", url="/privacy"),
        dict(title="Login", url="/users/login"),
        #dict(title="Blog", url="/blog/"),
        dict(title="About Us", url="/about")
    )

def users_menu():
    u_menu = (
        dict(title="Home", url="/"),
        dict(title="List users", url="/users/"),
        dict(title="Create user", url="/users/add"),
        dict(title="Logout", url="/users/logout")
    )
    return u_menu + main_menu()


def home():
    return render_template("home.html", 
            page_title = "Where are you!",
            main_menu = main_menu()
        )

def terms_of_use():
    return render_template("terms_of_use.html",
            page_title = "Terms of use",
            main_menu = main_menu()
            )

def privacy():
    return render_template("privacy.html",
            page_title = "Privacy",
            main_menu = main_menu()
            )

def about():
    return render_template("about.html",
            page_title = "About Us",
            main_menu = main_menu()
            )



def login():
    message = ""
    if session.get("user"):
        message = "User %s is already loged in!" % session["user"]["email"]

    if request.method == "POST":
        try:
            usr = User.query.filter_by(email=request.form["email"], password=request.form["password"]).first()
            session["user"] = dict(email=usr.email, enabled=usr.enabled)

            return redirect(url_for("user_dashboard"))

        except AttributeError:
            pass
            message = "Wrong login or password"


    return render_template("login.html",
            page_title = "Login page",
            message = message,
            main_menu = users_menu()
            )

def logout():
    if session.get("user"):
        session.pop("user")
        flash('You were successfully logged out')
    
    return redirect(url_for("login"))


def user_dashboard():
    if not session.get("user"):
        flash('Login is required!!!')
        return redirect(url_for("login"))

    return render_template("user_dashboard.html",
                page_title = "",
                user=session["user"],
                main_menu = users_menu())



def posts(slug=None):
    print(f"Posts page {slug}")
    return render_template("blog.html", 
            page_title = "Blog posts",
            main_menu = main_menu(),
            data = blog_pages()
            )

def post_view(id=None):
    if id in blog_pages:
        app.logger.info("find page: ", id)
        return render_template("blog_article.html",
                page_title="Blog posts",
                main_menu = main_menu(),
                data=blog_pages[id]
                )

    else:
        return render_template("blog.html", 
            page_title = "Invalid blog post, please choose from posts bellow",
            main_menu = main_menu(),
            data = blog_pages()
            )

def users_list(uid=None):
    if not session.get("user"):
        flash('Login is required!!!')
        return redirect(url_for("login"))

    if isinstance(uid, int):
        users = User.query.filter_by(uid=uid).first()
    
    else:
        users = User.query.all()

    return render_template("users.html",
        message="",
        users=users,
        main_menu=users_menu()
        )

def users_add():
    # if not session.get("user"):
    #     flash('Login is required!!!')
    #     return redirect(url_for("login"))

    if request.method == "GET":
        #users = ", ".join(usr.email for usr in model.User.query.all())
        return render_template(
                "user_register.html",
                main_menu = users_menu(),
                message = ""
                )
    else:
        email = request.form.get("email")
        password = request.form.get("password")
        
        # User.create(email=email, password=password)

        if len(email) > 1 and len(password) > 1:

            if User.create(email=email, password=password, enabled=1) == True:
                msg = f"New user with email {email} has been added."
            else:
                msg = f"Error ocured during adding user with email {email}. Maybe it already exists."

            return render_template(
                "user_register.html",
                main_menu = users_menu(),
                message = msg
            )

        else:
            return render_template(
                "user_register.html",
                main_menu = users_menu(),
                message="Something went wrong!"
                )

