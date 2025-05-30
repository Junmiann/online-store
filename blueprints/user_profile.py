from flask import Flask, render_template, redirect, url_for, session, Blueprint
from db import *
from utils import *

app = Flask(__name__)

user_profile_bp = Blueprint('user_profile', __name__, url_prefix='')

@user_profile_bp.route("/user_profile")
def user_profile():
    user = session.get("user")
    if user is None:
        return redirect(url_for("login.login"))
    else:
        order_id = check_order_status()

        cur = con.cursor()
        cur.callproc("customer_orders", [user[0], order_id])
        user_orders = cur.fetchall()
        return render_template("user_profile.html", user=user, user_orders=user_orders)

@user_profile_bp.route("/user_profile/order_details/<int:order_id>")
def user_order_details(order_id):
    user = session.get("user")
    
    cur = con.cursor()
    cur.callproc("get_order_details", [order_id])
    user_orders = cur.fetchall()
    
    cur.callproc("get_order_products", [order_id])
    user_order_products = cur.fetchall()
    
    return render_template("order_details.html", user=user, order_id=order_id, user_orders=user_orders, user_order_products=user_order_products)

@user_profile_bp.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))