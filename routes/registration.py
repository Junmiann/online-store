from flask import Flask, render_template, flash, redirect, url_for, request, Blueprint
from db import *
from models.user import User

app = Flask(__name__)

registration_bp = Blueprint('registration', __name__, url_prefix='')

@registration_bp.route("/registration")
def registration():
    return render_template("registration.html")

@registration_bp.route("/register_form", methods=["POST"])
def register_form():
        user = User(
              request.form["firstname"],
              request.form["lastname"],
              request.form["email"],
              request.form["password"],
              request.form["phone"],
              request.form["address"],
              request.form["city"],
              request.form["country"]
        )
        user.save_user_to_db(con)

        flash("Registration successful!\nYou may now log in.")
        return redirect(url_for("login.login"))