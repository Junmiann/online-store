from flask import Flask, render_template, flash, redirect, url_for, request, session, Blueprint
from db import *
from werkzeug.security import check_password_hash

app = Flask(__name__)

login_bp = Blueprint('login', __name__, url_prefix='')

@login_bp.route("/login")
def login():
    return render_template("/auth/login.html")

@login_bp.route("/login_form", methods=["POST"])
def login_form():
    user_email = request.form["email"]
    user_password = request.form["password"]

    cur = con.cursor()
    cur.callproc("get_user_by_email", [user_email.strip().lower()])
    user = cur.fetchone()

    if user and check_password_hash(user[4] , user_password):
        session["user"] = user
        if user[9] is False:
            return redirect(url_for("index"))
        else:
            return redirect(url_for("admin_dashboard.admin_dashboard", section="orders"))

    else:
        flash("Invalid credentials, please try again!")
        return redirect(url_for("login.login"))