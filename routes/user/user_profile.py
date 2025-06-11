from flask import Flask, render_template, redirect, url_for, session, Blueprint
from db import *
from utils import *
from models.userOrder import UserOrder

app = Flask(__name__)

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='')

@user_profile_bp.route("/user_profile")
def user_profile():
    user = session.get("user")
    if user is None:
        return redirect(url_for("login.login"))
    else:
        order_id = check_order_status()
        user_orders = UserOrder.get_user_orders(con, user[0], order_id)
        return render_template("/user/user_profile.html", user=user, user_orders=user_orders)

@user_profile_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))