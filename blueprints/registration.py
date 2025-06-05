from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from db import *
from werkzeug.security import generate_password_hash

app = Flask(__name__)

registration_bp = Blueprint('registration', __name__, url_prefix='')

@registration_bp.route("/registration")
def registration():
    return render_template("registration.html")

@registration_bp.route("/register_form", methods=["POST"])
def register_form():
        user_firstname = request.form["firstname"]
        user_lastname = request.form["lastname"]
        user_email = request.form["email"]
        user_password = request.form["password"]
        user_phone = request.form["phone"]
        user_address = request.form["address"]
        user_city = request.form["city"]
        user_country = request.form["country"]

        hashed_password = generate_password_hash(user_password)

        cur = con.cursor()
        cur.callproc("register_account", [user_firstname, user_lastname, user_email, hashed_password, user_phone, user_address, user_city, user_country])
        con.commit()
        cur.close()

        flash("Registration successful!\nYou may now log in.")
        return redirect(url_for("login.login"))