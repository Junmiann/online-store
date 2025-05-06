from flask import Flask, render_template, flash, redirect, url_for, request, session, Blueprint
from db import *

app = Flask(__name__)

login_bp = Blueprint('login', __name__, url_prefix='')

@login_bp.route("/login")
def login():
    return render_template("login.html")

@login_bp.route("/login_form", methods=["POST"])
def login_form():
    email = request.form["email"]
    password = request.form["password"]

    cur = con.cursor()
    cur.callproc("check_account", [email, password])
    account = cur.fetchall()

    if account:
        session["user"] = account[0]
        return redirect(url_for("index"))
    else:
        flash("Invalid credentials, please try again!")
        return redirect(url_for("login.login"))